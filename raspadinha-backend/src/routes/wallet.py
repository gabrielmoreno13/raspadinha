from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime, timedelta
from decimal import Decimal
import uuid
import re

from src.models.user import db, User
from src.models.wallet import Wallet
from src.models.transaction import Transaction, PaymentService
from src.models.bonus import BonusService

wallet_bp = Blueprint('wallet', __name__)

# Schemas de validação
class DepositSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=10, max=10000))
    payment_method = fields.Str(load_default='pix', validate=validate.OneOf(['pix', 'credit_card']))

class WithdrawSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=20, max=50000))
    pix_key = fields.Str(required=True, validate=validate.Length(min=11, max=255))
    pix_key_type = fields.Str(required=True, validate=validate.OneOf(['cpf', 'email', 'phone', 'random']))

def validate_pix_key(pix_key, pix_key_type):
    """Valida chave PIX baseada no tipo"""
    if pix_key_type == 'cpf':
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', pix_key)
        return len(cpf) == 11
    elif pix_key_type == 'email':
        # Validação básica de email
        return '@' in pix_key and '.' in pix_key
    elif pix_key_type == 'phone':
        # Remove caracteres não numéricos
        phone = re.sub(r'[^0-9]', '', pix_key)
        return len(phone) >= 10
    elif pix_key_type == 'random':
        # Chave aleatória tem formato específico
        return len(pix_key) >= 32
    
    return False

@wallet_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    """Obter saldo da carteira"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        wallet = user.wallet
        if not wallet:
            # Cria carteira se não existir
            wallet = Wallet(user_id=current_user_id)
            db.session.add(wallet)
            db.session.commit()
        
        return jsonify({
            'wallet': wallet.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@wallet_bp.route('/deposit', methods=['POST'])
@jwt_required()
def create_deposit():
    """Criar depósito"""
    try:
        # Validação dos dados
        schema = DepositSchema()
        data = schema.load(request.json)
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        amount = data['amount']
        payment_method = data['payment_method']
        
        # Cria a transação de depósito
        transaction = PaymentService.create_deposit(current_user_id, amount, payment_method)
        
        # Verifica se há bônus de recarga
        reload_bonus = BonusService.create_reload_bonus(current_user_id, amount)
        
        # Simula dados do PIX (em produção, viria do gateway)
        pix_data = None
        if payment_method == 'pix':
            pix_data = {
                'qr_code': f"00020126580014br.gov.bcb.pix0136{uuid.uuid4()}5204000053039865802BR5925RASPADINHA ONLINE LTDA6009SAO PAULO62070503***6304",
                'pix_key': f"{uuid.uuid4()}",
                'expires_at': (datetime.utcnow() + timedelta(minutes=15)).isoformat(),
                'amount': amount
            }
        
        return jsonify({
            'message': 'Depósito criado com sucesso!',
            'transaction': transaction.to_dict(),
            'reload_bonus': reload_bonus.to_dict() if reload_bonus else None,
            'pix_data': pix_data
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Dados inválidos', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@wallet_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def create_withdrawal():
    """Criar saque"""
    try:
        # Validação dos dados
        schema = WithdrawSchema()
        data = schema.load(request.json)
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        amount = data['amount']
        pix_key = data['pix_key']
        pix_key_type = data['pix_key_type']
        
        # Valida chave PIX
        if not validate_pix_key(pix_key, pix_key_type):
            return jsonify({'error': 'Chave PIX inválida'}), 400
        
        # Verifica se tem saldo suficiente
        wallet = user.wallet
        if not wallet or not wallet.can_withdraw(amount):
            return jsonify({'error': 'Saldo insuficiente para saque'}), 400
        
        # Verifica limite diário de saque (exemplo: R$ 5.000)
        today = datetime.utcnow().date()
        today_withdrawals = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.type == 'withdrawal',
            Transaction.status.in_(['pending', 'completed']),
            db.func.date(Transaction.created_at) == today
        ).scalar() or 0
        
        daily_limit = 5000
        if float(today_withdrawals) + amount > daily_limit:
            return jsonify({'error': f'Limite diário de saque excedido (R$ {daily_limit})'}), 400
        
        # Cria a transação de saque
        transaction = PaymentService.create_withdrawal(current_user_id, amount, pix_key)
        
        return jsonify({
            'message': 'Saque solicitado com sucesso!',
            'transaction': transaction.to_dict(),
            'estimated_time': '2-24 horas'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Dados inválidos', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@wallet_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Obter histórico de transações"""
    try:
        current_user_id = get_jwt_identity()
        
        # Parâmetros de filtro
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        transaction_type = request.args.get('type')  # deposit, withdrawal, game_cost, prize_payout
        status = request.args.get('status')  # pending, completed, failed
        
        # Query base
        query = Transaction.query.filter_by(user_id=current_user_id)
        
        # Aplicar filtros
        if transaction_type:
            query = query.filter_by(type=transaction_type)
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar por data (mais recentes primeiro)
        query = query.order_by(Transaction.created_at.desc())
        
        # Paginação
        transactions_paginated = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'transactions': [transaction.to_dict() for transaction in transactions_paginated.items],
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

@wallet_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    """Obter detalhes de uma transação específica"""
    try:
        current_user_id = get_jwt_identity()
        
        transaction = Transaction.query.filter_by(
            id=transaction_id,
            user_id=current_user_id
        ).first()
        
        if not transaction:
            return jsonify({'error': 'Transação não encontrada'}), 404
        
        return jsonify({
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@wallet_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_wallet_summary():
    """Obter resumo da carteira"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        wallet = user.wallet
        if not wallet:
            return jsonify({'error': 'Carteira não encontrada'}), 404
        
        # Estatísticas do mês atual
        current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Depósitos do mês
        month_deposits = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.type == 'deposit',
            Transaction.status == 'completed',
            Transaction.created_at >= current_month
        ).scalar() or 0
        
        # Saques do mês
        month_withdrawals = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.type == 'withdrawal',
            Transaction.status == 'completed',
            Transaction.created_at >= current_month
        ).scalar() or 0
        
        # Gastos em jogos do mês
        month_games = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.type == 'game_cost',
            Transaction.status == 'completed',
            Transaction.created_at >= current_month
        ).scalar() or 0
        
        # Prêmios ganhos do mês
        month_prizes = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user_id,
            Transaction.type == 'prize_payout',
            Transaction.status == 'completed',
            Transaction.created_at >= current_month
        ).scalar() or 0
        
        return jsonify({
            'wallet': wallet.to_dict(),
            'monthly_summary': {
                'deposits': float(month_deposits),
                'withdrawals': float(month_withdrawals),
                'games_spent': float(month_games),
                'prizes_won': float(month_prizes),
                'net_result': float(month_prizes) - float(month_games)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Webhook simulado para confirmação de pagamentos PIX
@wallet_bp.route('/webhook/pix', methods=['POST'])
def pix_webhook():
    """Webhook para confirmação de pagamentos PIX (simulado)"""
    try:
        data = request.json
        
        # Em produção, validaria a assinatura do webhook
        transaction_id = data.get('transaction_id')
        status = data.get('status')  # 'approved', 'rejected'
        
        if not transaction_id or not status:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transação não encontrada'}), 404
        
        if status == 'approved' and transaction.status == 'pending':
            # Processa o pagamento
            if transaction.type == 'deposit':
                wallet = Wallet.query.filter_by(user_id=transaction.user_id).first()
                if wallet:
                    wallet.add_balance(float(transaction.amount))
                    wallet.total_deposited += transaction.amount
                    transaction.mark_as_completed()
                    db.session.commit()
        elif status == 'rejected':
            transaction.mark_as_failed('Pagamento rejeitado')
            db.session.commit()
        
        return jsonify({'message': 'Webhook processado'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

