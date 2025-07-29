from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime, date
import re

from src.models.user import db, User
from src.models.wallet import Wallet
from src.models.bonus import BonusService

auth_bp = Blueprint('auth', __name__)

# Schemas de validação
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    phone = fields.Str(validate=validate.Length(min=10, max=20))
    birth_date = fields.Date(required=True)
    cpf = fields.Str(required=True, validate=validate.Length(min=11, max=14))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação dos dígitos verificadores
    def calculate_digit(cpf_digits, weights):
        total = sum(int(digit) * weight for digit, weight in zip(cpf_digits, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Primeiro dígito verificador
    first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
    if int(cpf[9]) != first_digit:
        return False
    
    # Segundo dígito verificador
    second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
    if int(cpf[10]) != second_digit:
        return False
    
    return True

def calculate_age(birth_date):
    """Calcula idade baseada na data de nascimento"""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de novo usuário"""
    try:
        # Validação dos dados
        schema = RegisterSchema()
        data = schema.load(request.json)
        
        # Validações adicionais
        if not validate_cpf(data['cpf']):
            return jsonify({'error': 'CPF inválido'}), 400
        
        if calculate_age(data['birth_date']) < 18:
            return jsonify({'error': 'Usuário deve ser maior de idade'}), 400
        
        # Verifica se email já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Verifica se CPF já existe
        cpf_clean = re.sub(r'[^0-9]', '', data['cpf'])
        if User.query.filter_by(cpf=cpf_clean).first():
            return jsonify({'error': 'CPF já cadastrado'}), 400
        
        # Cria o usuário
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            birth_date=data['birth_date'],
            cpf=cpf_clean
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()  # Para obter o ID do usuário
        
        # Cria carteira do usuário
        wallet = Wallet(user_id=user.id)
        db.session.add(wallet)
        
        # Cria bônus de boas-vindas
        welcome_bonus = BonusService.create_welcome_bonus(user.id)
        
        # Cria missões diárias
        daily_missions = BonusService.create_daily_missions(user.id)
        
        db.session.commit()
        
        # Gera tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'user': user.to_dict(),
            'wallet': wallet.to_dict(),
            'welcome_bonus': welcome_bonus.to_dict() if welcome_bonus else None,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Dados inválidos', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login do usuário"""
    try:
        # Validação dos dados
        schema = LoginSchema()
        data = schema.load(request.json)
        
        # Busca o usuário
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Email ou senha incorretos'}), 401
        
        if user.status != 'active':
            return jsonify({'error': 'Conta desativada'}), 401
        
        # Atualiza último login
        user.last_login = datetime.utcnow()
        
        # Verifica bônus diário
        daily_bonus = BonusService.create_daily_bonus(user.id)
        
        # Cria missões diárias se necessário
        daily_missions = BonusService.create_daily_missions(user.id)
        
        db.session.commit()
        
        # Gera tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login realizado com sucesso!',
            'user': user.to_dict(),
            'wallet': user.wallet.to_dict() if user.wallet else None,
            'daily_bonus': daily_bonus.to_dict() if daily_bonus else None,
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Dados inválidos', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovação do token de acesso"""
    try:
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro ao renovar token'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obter perfil do usuário"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'wallet': user.wallet.to_dict() if user.wallet else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualizar perfil do usuário"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.json
        
        # Campos que podem ser atualizados
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso!',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Alterar senha do usuário"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        if not user.check_password(current_password):
            return jsonify({'error': 'Senha atual incorreta'}), 401
        
        if len(new_password) < 8:
            return jsonify({'error': 'Nova senha deve ter pelo menos 8 caracteres'}), 400
        
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Senha alterada com sucesso!'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout do usuário"""
    # TODO: Implementar blacklist de tokens se necessário
    return jsonify({
        'message': 'Logout realizado com sucesso!'
    }), 200

