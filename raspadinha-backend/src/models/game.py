from src.models.user import db
from datetime import datetime
from decimal import Decimal
import json
import random

class ScratchCardCategory(db.Model):
    __tablename__ = 'scratch_card_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    max_prize = db.Column(db.Numeric(10, 2), nullable=False)
    symbols = db.Column(db.JSON)  # Lista de símbolos possíveis
    win_rules = db.Column(db.JSON)  # Regras de vitória
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ScratchCardCategory {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'theme': self.theme,
            'description': self.description,
            'price': float(self.price),
            'max_prize': float(self.max_prize),
            'symbols': self.symbols,
            'win_rules': self.win_rules,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class ScratchCard(db.Model):
    __tablename__ = 'scratch_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('scratch_card_categories.id'), nullable=False)
    symbols = db.Column(db.JSON, nullable=False)  # Símbolos da carta específica
    winning_combination = db.Column(db.JSON)  # Combinação vencedora se houver
    prize_amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    probability = db.Column(db.Numeric(8, 6), nullable=False)
    is_winner = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    category = db.relationship('ScratchCardCategory', backref='cards')

    def __repr__(self):
        return f'<ScratchCard {self.id} Winner:{self.is_winner}>'

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'symbols': self.symbols,
            'winning_combination': self.winning_combination,
            'prize_amount': float(self.prize_amount),
            'probability': float(self.probability),
            'is_winner': self.is_winner,
            'created_at': self.created_at.isoformat(),
            'category': self.category.to_dict() if self.category else None
        }

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scratch_card_id = db.Column(db.Integer, db.ForeignKey('scratch_cards.id'), nullable=False)
    amount_paid = db.Column(db.Numeric(8, 2), nullable=False)
    prize_won = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    is_bonus_game = db.Column(db.Boolean, default=False)
    game_data = db.Column(db.JSON)  # Dados específicos do jogo
    status = db.Column(db.String(20), default='completed')
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    scratch_card = db.relationship('ScratchCard', backref='games')

    def __repr__(self):
        return f'<Game {self.id} User:{self.user_id} Prize:{self.prize_won}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'scratch_card_id': self.scratch_card_id,
            'amount_paid': float(self.amount_paid),
            'prize_won': float(self.prize_won),
            'is_bonus_game': self.is_bonus_game,
            'game_data': self.game_data,
            'status': self.status,
            'played_at': self.played_at.isoformat(),
            'scratch_card': self.scratch_card.to_dict() if self.scratch_card else None
        }

class GameEngine:
    """Engine para geração e processamento de jogos"""
    
    @staticmethod
    def generate_scratch_card(category_id, user_id=None):
        """Gera uma nova raspadinha baseada na categoria"""
        category = ScratchCardCategory.query.get(category_id)
        if not category:
            raise ValueError("Categoria não encontrada")
        
        # Símbolos disponíveis
        symbols = category.symbols
        if not symbols:
            symbols = ['🍀', '💎', '💰', '⭐', '🎯', '🏆', '🎁', '🔥']
        
        # Gera grid 3x3 de símbolos
        card_symbols = []
        for i in range(9):
            card_symbols.append(random.choice(symbols))
        
        # Determina se é vencedora baseado em probabilidades
        win_probability = GameEngine._calculate_win_probability(category, user_id)
        is_winner = random.random() < win_probability
        
        prize_amount = Decimal('0.00')
        winning_combination = None
        
        if is_winner:
            # Determina o prêmio
            prize_amount = GameEngine._determine_prize(category)
            
            # Força uma combinação vencedora
            winning_symbol = random.choice(symbols)
            winning_positions = random.sample(range(9), 3)
            
            for pos in winning_positions:
                card_symbols[pos] = winning_symbol
            
            winning_combination = {
                'symbol': winning_symbol,
                'positions': winning_positions,
                'rule': '3_of_a_kind'
            }
        
        # Cria a raspadinha
        scratch_card = ScratchCard(
            category_id=category_id,
            symbols=card_symbols,
            winning_combination=winning_combination,
            prize_amount=prize_amount,
            probability=win_probability,
            is_winner=is_winner
        )
        
        db.session.add(scratch_card)
        db.session.commit()
        
        return scratch_card
    
    @staticmethod
    def _calculate_win_probability(category, user_id=None):
        """Calcula probabilidade de vitória dinâmica"""
        base_probability = 0.15  # 15% base
        
        # Ajusta baseado no valor da categoria
        price = float(category.price)
        if price >= 10:
            base_probability = 0.20  # 20% para categorias premium
        
        # TODO: Implementar ajustes baseados no histórico do usuário
        # - Usuários novos: probabilidade ligeiramente maior
        # - Usuários que perderam muito: probabilidade de recuperação
        # - Balanceamento de margem de lucro
        
        return base_probability
    
    @staticmethod
    def _determine_prize(category):
        """Determina o valor do prêmio baseado na categoria"""
        max_prize = float(category.max_prize)
        price = float(category.price)
        
        # Distribuição de prêmios
        prize_distribution = [
            (price, 0.60),          # Recupera o investimento (60%)
            (price * 2.5, 0.25),   # 2.5x o valor (25%)
            (price * 5, 0.10),     # 5x o valor (10%)
            (price * 10, 0.04),    # 10x o valor (4%)
            (max_prize, 0.01)      # Prêmio máximo (1%)
        ]
        
        rand = random.random()
        cumulative = 0
        
        for prize, probability in prize_distribution:
            cumulative += probability
            if rand <= cumulative:
                return Decimal(str(prize))
        
        return Decimal(str(price))  # Fallback

