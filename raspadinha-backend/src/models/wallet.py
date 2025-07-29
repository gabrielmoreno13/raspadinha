from src.models.user import db
from datetime import datetime
from decimal import Decimal

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    bonus_balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    total_deposited = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    total_withdrawn = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Wallet User:{self.user_id} Balance:{self.balance}>'

    def get_total_balance(self):
        """Retorna o saldo total (principal + bônus)"""
        return float(self.balance) + float(self.bonus_balance)

    def add_balance(self, amount, is_bonus=False):
        """Adiciona saldo à carteira"""
        if is_bonus:
            self.bonus_balance += Decimal(str(amount))
        else:
            self.balance += Decimal(str(amount))
        self.updated_at = datetime.utcnow()

    def subtract_balance(self, amount, use_bonus_first=True):
        """Remove saldo da carteira, usando bônus primeiro se especificado"""
        amount = Decimal(str(amount))
        
        if use_bonus_first and self.bonus_balance > 0:
            if self.bonus_balance >= amount:
                self.bonus_balance -= amount
                amount = Decimal('0')
            else:
                amount -= self.bonus_balance
                self.bonus_balance = Decimal('0')
        
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
            else:
                raise ValueError("Saldo insuficiente")
        
        self.updated_at = datetime.utcnow()

    def can_withdraw(self, amount):
        """Verifica se é possível sacar o valor (apenas saldo principal)"""
        return float(self.balance) >= float(amount)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': float(self.balance),
            'bonus_balance': float(self.bonus_balance),
            'total_balance': self.get_total_balance(),
            'total_deposited': float(self.total_deposited),
            'total_withdrawn': float(self.total_withdrawn),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

