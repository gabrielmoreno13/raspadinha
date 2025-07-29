from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from datetime import datetime, timedelta
from decimal import Decimal

from src.models.user import db, User
from src.models.wallet import Wallet
from src.models.game import ScratchCardCategory, ScratchCard, Game, GameEngine
from src.models.transaction import Transaction, PaymentService
from src.models.bonus import Bonus, BonusService

games_bp = Blueprint('games', __name__)

# Schemas de validação
class PlayGameSchema(Schema):
    category_id = fields.Int(required=True)
    use_bonus = fields.Bool(load_default=False)

@games_bp.route('/categories', methods=['GET'])
def get_categories():
    """Listar todas as categorias de raspadinha"""
    try:
        categories = ScratchCardCategory.query.filter_by(is_active=True).all()
        
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Obter detalhes de uma categoria específica"""
    try:
        category = ScratchCardCategory.query.get(category_id)
        
        if not category or not category.is_active:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        return jsonify({
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/play', methods=['POST'])
@jwt_required()
def play_game():
    """Jogar uma raspadinha"""
    try:
        # Validação dos dados
        schema = PlayGameSchema()
        data = schema.load(request.json)
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Busca a categoria
        category = ScratchCardCategory.query.get(data['category_id'])
        if not category or not category.is_active:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        # Verifica se vai usar bônus
        use_bonus = data.get('use_bonus', False)
        game_cost = float(category.price)
        
        # Verifica saldo
        wallet = user.wallet
        if not wallet:
            return jsonify({'error': 'Carteira não encontrada'}), 404
        
        if use_bonus:
            # Verifica se tem jogos grátis disponíveis
            available_bonus = Bonus.query.filter_by(
                user_id=current_user_id,
                status='active'
            ).filter(
                Bonus.free_games > 0
            ).filter(
                db.or_(Bonus.expires_at.is_(None), Bonus.expires_at > datetime.utcnow())
            ).first()
            
            if not available_bonus:
                return jsonify({'error': 'Nenhum jogo grátis disponível'}), 400
        else:
            # Verifica saldo suficiente
            if wallet.get_total_balance() < game_cost:
                return jsonify({'error': 'Saldo insuficiente'}), 400
        
        # Gera a raspadinha
        scratch_card = GameEngine.generate_scratch_card(category.id, current_user_id)
        
        # Cria o jogo
        game = Game(
            user_id=current_user_id,
            scratch_card_id=scratch_card.id,
            amount_paid=Decimal(str(game_cost)),
            prize_won=scratch_card.prize_amount,
            is_bonus_game=use_bonus
        )
        
        db.session.add(game)
        db.session.flush()  # Para obter o ID do jogo
        
        # Processa pagamento
        if use_bonus:
            # Usa jogo grátis
            available_bonus.free_games -= 1
            if available_bonus.free_games <= 0:
                available_bonus.status = 'claimed'
                available_bonus.claimed_at = datetime.utcnow()
            
            # Cria transação de jogo grátis
            PaymentService.create_game_transaction(
                current_user_id, 0, game.id, is_bonus=True
            )
        else:
            # Debita da carteira
            wallet.subtract_balance(game_cost, use_bonus_first=True)
            
            # Cria transação de custo do jogo
            PaymentService.create_game_transaction(
                current_user_id, game_cost, game.id, is_bonus=False
            )
        
        # Se ganhou, credita o prêmio
        if scratch_card.is_winner and scratch_card.prize_amount > 0:
            wallet.add_balance(float(scratch_card.prize_amount))
            
            # Cria transação de prêmio
            PaymentService.create_prize_transaction(
                current_user_id, float(scratch_card.prize_amount), game.id
            )
        
        # Atualiza pontos de fidelidade (apenas para jogos pagos)
        if not use_bonus:
            BonusService.update_loyalty_points(current_user_id, game_cost)
        
        # Atualiza missões
        completed_missions = BonusService.update_user_missions(current_user_id, 'game_played')
        
        if scratch_card.is_winner:
            prize_missions = BonusService.update_user_missions(current_user_id, 'prize_won')
            completed_missions.extend(prize_missions)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Jogo realizado com sucesso!',
            'game': game.to_dict(),
            'scratch_card': scratch_card.to_dict(),
            'wallet': wallet.to_dict(),
            'completed_missions': [mission.to_dict() for mission in completed_missions]
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Dados inválidos', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/history', methods=['GET'])
@jwt_required()
def get_game_history():
    """Obter histórico de jogos do usuário"""
    try:
        current_user_id = get_jwt_identity()
        
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Busca jogos do usuário
        games_query = Game.query.filter_by(user_id=current_user_id).order_by(Game.played_at.desc())
        
        # Paginação
        games_paginated = games_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'games': [game.to_dict() for game in games_paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': games_paginated.total,
                'pages': games_paginated.pages,
                'has_next': games_paginated.has_next,
                'has_prev': games_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/winners-feed', methods=['GET'])
def get_winners_feed():
    """Feed de ganhadores recentes"""
    try:
        # Busca jogos vencedores das últimas 24 horas
        since = datetime.utcnow() - timedelta(hours=24)
        
        winners = db.session.query(Game, User).join(User).filter(
            Game.prize_won > 0,
            Game.played_at >= since
        ).order_by(Game.played_at.desc()).limit(50).all()
        
        winners_data = []
        for game, user in winners:
            # Oculta parte do nome para privacidade
            name_parts = user.first_name.split()
            if len(name_parts) > 0:
                hidden_name = name_parts[0][:2] + "***"
                if len(name_parts) > 1:
                    hidden_name += " " + name_parts[-1][:1] + "***"
            else:
                hidden_name = "Usuário***"
            
            winners_data.append({
                'id': game.id,
                'winner_name': hidden_name,
                'prize_amount': float(game.prize_won),
                'category_name': game.scratch_card.category.name if game.scratch_card and game.scratch_card.category else 'Raspadinha',
                'played_at': game.played_at.isoformat(),
                'time_ago': _calculate_time_ago(game.played_at)
            })
        
        return jsonify({
            'winners': winners_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Estatísticas gerais do sistema"""
    try:
        # Total de jogadores únicos
        total_players = User.query.filter_by(status='active').count()
        
        # Prêmios distribuídos hoje
        today = datetime.utcnow().date()
        today_prizes = db.session.query(db.func.sum(Game.prize_won)).filter(
            db.func.date(Game.played_at) == today,
            Game.prize_won > 0
        ).scalar() or 0
        
        # Jogos jogados hoje
        today_games = Game.query.filter(
            db.func.date(Game.played_at) == today
        ).count()
        
        # Maior prêmio da semana
        week_ago = datetime.utcnow() - timedelta(days=7)
        biggest_prize = db.session.query(db.func.max(Game.prize_won)).filter(
            Game.played_at >= week_ago,
            Game.prize_won > 0
        ).scalar() or 0
        
        return jsonify({
            'statistics': {
                'total_players': total_players,
                'today_prizes': float(today_prizes),
                'today_games': today_games,
                'biggest_prize_week': float(biggest_prize)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@games_bp.route('/bonuses', methods=['GET'])
@jwt_required()
def get_user_bonuses():
    """Obter bônus disponíveis do usuário"""
    try:
        current_user_id = get_jwt_identity()
        
        # Busca bônus ativos
        active_bonuses = Bonus.query.filter_by(
            user_id=current_user_id,
            status='active'
        ).filter(
            db.or_(Bonus.expires_at.is_(None), Bonus.expires_at > datetime.utcnow())
        ).all()
        
        return jsonify({
            'bonuses': [bonus.to_dict() for bonus in active_bonuses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

def _calculate_time_ago(played_at):
    """Calcula tempo decorrido desde o jogo"""
    now = datetime.utcnow()
    diff = now - played_at
    
    if diff.days > 0:
        return f"há {diff.days} dia{'s' if diff.days > 1 else ''}"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"há {hours} hora{'s' if hours > 1 else ''}"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"há {minutes} minuto{'s' if minutes > 1 else ''}"
    else:
        return "há poucos segundos"

