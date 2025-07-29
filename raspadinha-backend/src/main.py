import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Importar todos os modelos
from src.models.user import db, User
from src.models.wallet import Wallet
from src.models.game import ScratchCardCategory, ScratchCard, Game
from src.models.transaction import Transaction
from src.models.bonus import Bonus, Mission

# Importar todas as rotas
from src.routes.auth import auth_bp
from src.routes.games import games_bp
from src.routes.wallet import wallet_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = 'raspadinha-secret-key-2024'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-raspadinha'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
jwt = JWTManager(app)
CORS(app, origins="*")  # Permitir CORS para desenvolvimento

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(games_bp, url_prefix='/api/games')
app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Criar tabelas e dados iniciais
with app.app_context():
    db.create_all()
    
    # Criar categorias de raspadinha se não existirem
    if ScratchCardCategory.query.count() == 0:
        categories = [
            {
                'name': 'Raspa da Sorte',
                'theme': 'classic',
                'description': 'A clássica raspadinha da sorte com símbolos tradicionais',
                'price': 10.00,
                'max_prize': 5000.00,
                'symbols': ['🍀', '💎', '💰', '⭐', '🎯', '🏆', '🎁', '🔥'],
                'win_rules': {'type': '3_of_a_kind', 'description': 'Encontre 3 símbolos iguais'}
            },
            {
                'name': 'Raspa do Tesouro',
                'theme': 'pirate',
                'description': 'Encontre o tesouro escondido dos piratas',
                'price': 10.00,
                'max_prize': 10000.00,
                'symbols': ['🏴‍☠️', '💰', '🗺️', '⚓', '💎', '🏆', '⚔️', '🦜'],
                'win_rules': {'type': '3_of_a_kind', 'description': 'Encontre 3 símbolos iguais'}
            },
            {
                'name': 'Raspa Animal',
                'theme': 'nature',
                'description': 'Forme famílias de animais da sorte',
                'price': 10.00,
                'max_prize': 7500.00,
                'symbols': ['🐘', '🦁', '🐯', '🐼', '🦊', '🐺', '🐨', '🦘'],
                'win_rules': {'type': '3_of_a_kind', 'description': 'Encontre 3 animais iguais'}
            },
            {
                'name': 'Raspa Esporte',
                'theme': 'sports',
                'description': 'Monte seu time vencedor',
                'price': 10.00,
                'max_prize': 15000.00,
                'symbols': ['⚽', '🏆', '🥅', '👕', '⚡', '🔥', '💪', '🎯'],
                'win_rules': {'type': '3_of_a_kind', 'description': 'Encontre 3 símbolos iguais'}
            }
        ]
        
        for cat_data in categories:
            category = ScratchCardCategory(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        print("Categorias de raspadinha criadas!")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return {
        'status': 'healthy',
        'message': 'Raspadinha API está funcionando!',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
