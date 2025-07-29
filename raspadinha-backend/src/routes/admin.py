from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import func, and_, or_

from src.models.user import db, User
from src.models.wallet import Wallet
from src.models.game import ScratchCardCategory, ScratchCard, Game
from src.models.transaction import Transaction
from src.models.bonus import Bonus, Mission

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator para verificar se o usuário é admin"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        # Por simplicidade, vamos considerar que usuários com ID 1 são admins
        # Em produção, haveria um campo 'role' na tabela users
        if not user or user.id != 1:
            return jsonify({'error': 'Acesso negado - Apenas administradores'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard():
    """Dashboard principal com estatísticas gerais"""
    try:
        # Período para análise (últimos 30 dias)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        # Usuários
        total_users = User.query.filter_by(status='active').count()
        new_users_today = User.query.filter(
            func.date(User.created_at) == today
        ).count()
        new_users_month = User.query.filter(
            User.created_at >= thirty_days_ago
        ).count()
        
        # Jogos
        total_games = Game.query.count()
        games_today = Game.query.filter(
            func.date(Game.played_at) == today
        ).count()
        games_yesterday = Game.query.filter(
            func.date(Game.played_at) == yesterday
        ).count()
        
        # Receita
        total_revenue = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'game_cost',
            Transaction.status == 'completed'
        ).scalar() or 0
        
        revenue_today = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'game_cost',
            Transaction.status == 'completed',
            func.date(Transaction.created_at) == today
        ).scalar() or 0
        
        revenue_month = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'game_cost',
            Transaction.status == 'completed',
            Transaction.created_at >= thirty_days_ago
        ).scalar() or 0
        
        # Prêmios distribuídos
        total_prizes = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'prize_payout',
            Transaction.status == 'completed'
        ).scalar() or 0
        
        prizes_today = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'prize_payout',
            Transaction.status == 'completed',
            func.date(Transaction.created_at) == today
        ).scalar() or 0
        
        # Margem de lucro
        profit_margin = ((float(total_revenue) - float(total_prizes)) / float(total_revenue) * 100) if total_revenue > 0 else 0
        
        # Depósitos e saques
        total_deposits = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'deposit',
            Transaction.status == 'completed'
        ).scalar() or 0
        
        total_withdrawals = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'withdrawal',
            Transaction.status == 'completed'
        ).scalar() or 0
        
        # Transações pendentes
        pending_withdrawals = Transaction.query.filter_by(
            type='withdrawal',
            status='pending'
        ).count()
        
        return jsonify({
            'dashboard': {
                'users': {
                    'total': total_users,
                    'new_today': new_users_today,
                    'new_month': new_users_month
                },
                'games': {
                    'total': total_games,
                    'today': games_today,
                    'yesterday': games_yesterday,
                    'growth': ((games_today - games_yesterday) / games_yesterday * 100) if games_yesterday > 0 else 0
                },
                'revenue': {
                    'total': float(total_revenue),
                    'today': float(revenue_today),
                    'month': float(revenue_month)
                },
                'prizes': {
                    'total': float(total_prizes),
                    'today': float(prizes_today)
                },
                'profit_margin': round(profit_margin, 2),
                'financial': {
                    'total_deposits': float(total_deposits),
                    'total_withdrawals': float(total_withdrawals),
                    'pending_withdrawals': pending_withdrawals
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Listar usuários com filtros"""
    try:
        # Parâmetros de filtro
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status')
        search = request.args.get('search')
        
        # Query base
        query = User.query
        
        # Aplicar filtros
        if status:
            query = query.filter_by(status=status)
        
        if search:
            query = query.filter(
                or_(
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%')
                )
            )
        
        # Ordenar por data de criação (mais recentes primeiro)
        query = query.order_by(User.created_at.desc())
        
        # Paginação
        users_paginated = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Adicionar dados da carteira para cada usuário
        users_data = []
        for user in users_paginated.items:
            user_dict = user.to_dict()
            user_dict['wallet'] = user.wallet.to_dict() if user.wallet else None
            
            # Estatísticas do usuário
            total_games = Game.query.filter_by(user_id=user.id).count()
            total_spent = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user.id,
                Transaction.type == 'game_cost',
                Transaction.status == 'completed'
            ).scalar() or 0
            total_won = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user.id,
                Transaction.type == 'prize_payout',
                Transaction.status == 'completed'
            ).scalar() or 0
            
            user_dict['stats'] = {
                'total_games': total_games,
                'total_spent': float(total_spent),
                'total_won': float(total_won)
            }
            
            users_data.append(user_dict)
        
        return jsonify({
            'users': users_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users_paginated.total,
                'pages': users_paginated.pages,
                'has_next': users_paginated.has_next,
                'has_prev': users_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user_details(user_id):
    """Obter detalhes completos de um usuário"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Dados básicos
        user_data = user.to_dict()
        user_data['wallet'] = user.wallet.to_dict() if user.wallet else None
        
        # Últimos jogos
        recent_games = Game.query.filter_by(user_id=user_id).order_by(
            Game.played_at.desc()
        ).limit(10).all()
        
        # Últimas transações
        recent_transactions = Transaction.query.filter_by(user_id=user_id).order_by(
            Transaction.created_at.desc()
        ).limit(10).all()
        
        # Bônus ativos
        active_bonuses = Bonus.query.filter_by(
            user_id=user_id,
            status='active'
        ).all()
        
        # Estatísticas detalhadas
        stats = {
            'total_games': Game.query.filter_by(user_id=user_id).count(),
            'total_wins': Game.query.filter(
                Game.user_id == user_id,
                Game.prize_won > 0
            ).count(),
            'biggest_win': db.session.query(func.max(Game.prize_won)).filter_by(user_id=user_id).scalar() or 0,
            'total_deposited': user.wallet.total_deposited if user.wallet else 0,
            'total_withdrawn': user.wallet.total_withdrawn if user.wallet else 0
        }
        
        return jsonify({
            'user': user_data,
            'recent_games': [game.to_dict() for game in recent_games],
            'recent_transactions': [transaction.to_dict() for transaction in recent_transactions],
            'active_bonuses': [bonus.to_dict() for bonus in active_bonuses],
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_status(user_id):
    """Atualizar status do usuário (ativar/desativar)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.json
        new_status = data.get('status')
        
        if new_status not in ['active', 'inactive', 'suspended']:
            return jsonify({'error': 'Status inválido'}), 400
        
        user.status = new_status
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': f'Status do usuário atualizado para {new_status}',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/transactions', methods=['GET'])
@jwt_required()
@admin_required
def get_all_transactions():
    """Listar todas as transações"""
    try:
        # Parâmetros de filtro
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        transaction_type = request.args.get('type')
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        
        # Query base
        query = Transaction.query
        
        # Aplicar filtros
        if transaction_type:
            query = query.filter_by(type=transaction_type)
        if status:
            query = query.filter_by(status=status)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Ordenar por data (mais recentes primeiro)
        query = query.order_by(Transaction.created_at.desc())
        
        # Paginação
        transactions_paginated = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Adicionar dados do usuário para cada transação
        transactions_data = []
        for transaction in transactions_paginated.items:
            transaction_dict = transaction.to_dict()
            transaction_dict['user'] = transaction.user.to_dict() if transaction.user else None
            transactions_data.append(transaction_dict)
        
        return jsonify({
            'transactions': transactions_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': transactions_paginated.total,
                'pages': transactions_paginated.pages,
                'has_next': transactions_paginated.has_next,
                'has_prev': transactions_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/categories', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_categories():
    """Listar categorias para administração"""
    try:
        categories = ScratchCardCategory.query.all()
        
        # Adicionar estatísticas para cada categoria
        categories_data = []
        for category in categories:
            category_dict = category.to_dict()
            
            # Estatísticas da categoria
            total_games = Game.query.join(ScratchCard).filter(
                ScratchCard.category_id == category.id
            ).count()
            
            total_revenue = db.session.query(func.sum(Game.amount_paid)).join(ScratchCard).filter(
                ScratchCard.category_id == category.id
            ).scalar() or 0
            
            total_prizes = db.session.query(func.sum(Game.prize_won)).join(ScratchCard).filter(
                ScratchCard.category_id == category.id
            ).scalar() or 0
            
            category_dict['stats'] = {
                'total_games': total_games,
                'total_revenue': float(total_revenue),
                'total_prizes': float(total_prizes),
                'profit_margin': ((float(total_revenue) - float(total_prizes)) / float(total_revenue) * 100) if total_revenue > 0 else 0
            }
            
            categories_data.append(category_dict)
        
        return jsonify({
            'categories': categories_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/categories/<int:category_id>/toggle', methods=['PUT'])
@jwt_required()
@admin_required
def toggle_category_status(category_id):
    """Ativar/desativar categoria"""
    try:
        category = ScratchCardCategory.query.get(category_id)
        if not category:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        
        category.is_active = not category.is_active
        db.session.commit()
        
        status = 'ativada' if category.is_active else 'desativada'
        
        return jsonify({
            'message': f'Categoria {status} com sucesso',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@admin_bp.route('/analytics/revenue', methods=['GET'])
@jwt_required()
@admin_required
def get_revenue_analytics():
    """Analytics de receita por período"""
    try:
        # Parâmetros
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Receita por dia
        daily_revenue = db.session.query(
            func.date(Transaction.created_at).label('date'),
            func.sum(Transaction.amount).label('revenue')
        ).filter(
            Transaction.type == 'game_cost',
            Transaction.status == 'completed',
            Transaction.created_at >= start_date
        ).group_by(func.date(Transaction.created_at)).all()
        
        # Prêmios por dia
        daily_prizes = db.session.query(
            func.date(Transaction.created_at).label('date'),
            func.sum(Transaction.amount).label('prizes')
        ).filter(
            Transaction.type == 'prize_payout',
            Transaction.status == 'completed',
            Transaction.created_at >= start_date
        ).group_by(func.date(Transaction.created_at)).all()
        
        # Converter para dicionários para facilitar o merge
        revenue_dict = {str(item.date): float(item.revenue) for item in daily_revenue}
        prizes_dict = {str(item.date): float(item.prizes) for item in daily_prizes}
        
        # Combinar dados
        analytics_data = []
        current_date = start_date.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            date_str = str(current_date)
            revenue = revenue_dict.get(date_str, 0)
            prizes = prizes_dict.get(date_str, 0)
            
            analytics_data.append({
                'date': date_str,
                'revenue': revenue,
                'prizes': prizes,
                'profit': revenue - prizes
            })
            
            current_date += timedelta(days=1)
        
        return jsonify({
            'analytics': analytics_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

