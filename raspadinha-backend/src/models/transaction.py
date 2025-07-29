from src.models.user import db
from datetime import datetime
from decimal import Decimal

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, game_cost, prize_payout
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    payment_method = db.Column(db.String(50))  # pix, credit_card, bonus
    external_transaction_id = db.Column(db.String(255))  # ID do gateway de pagamento
    description = db.Column(db.Text)
    extra_data = db.Column(db.JSON)  # Dados adicionais específicos do tipo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Transaction {self.id} {self.type} {self.amount}>'

    def mark_as_completed(self):
        """Marca a transação como concluída"""
        self.status = 'completed'
        self.processed_at = datetime.utcnow()

    def mark_as_failed(self, reason=None):
        """Marca a transação como falhada"""
        self.status = 'failed'
        self.processed_at = datetime.utcnow()
        if reason:
            if not self.extra_data:
                self.extra_data = {}
            self.extra_data['failure_reason'] = reason

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': float(self.amount),
            'status': self.status,
            'payment_method': self.payment_method,
            'external_transaction_id': self.external_transaction_id,
            'description': self.description,
            'metadata': self.extra_data,
            'created_at': self.created_at.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }

class PaymentService:
    """Serviço para processamento de pagamentos"""
    
    @staticmethod
    def create_deposit(user_id, amount, payment_method='pix'):
        """Cria uma transação de depósito"""
        transaction = Transaction(
            user_id=user_id,
            type='deposit',
            amount=Decimal(str(amount)),
            payment_method=payment_method,
            description=f'Depósito via {payment_method.upper()}'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        # TODO: Integrar com gateway de pagamento real
        # Por enquanto, simula aprovação automática para PIX
        if payment_method == 'pix':
            PaymentService._simulate_pix_payment(transaction)
        
        return transaction
    
    @staticmethod
    def create_withdrawal(user_id, amount, pix_key):
        """Cria uma transação de saque"""
        from src.models.wallet import Wallet
        
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet or not wallet.can_withdraw(amount):
            raise ValueError("Saldo insuficiente para saque")
        
        transaction = Transaction(
            user_id=user_id,
            type='withdrawal',
            amount=Decimal(str(amount)),
            payment_method='pix',
            description=f'Saque via PIX',
            extra_data={'pix_key': pix_key}
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        # TODO: Integrar com gateway de pagamento real
        # Por enquanto, simula processamento automático
        PaymentService._process_withdrawal(transaction)
        
        return transaction
    
    @staticmethod
    def create_game_transaction(user_id, amount, game_id, is_bonus=False):
        """Cria uma transação de custo de jogo"""
        transaction = Transaction(
            user_id=user_id,
            type='game_cost',
            amount=Decimal(str(amount)),
            payment_method='bonus' if is_bonus else 'wallet',
            description=f'Jogo de raspadinha #{game_id}',
            extra_data={'game_id': game_id, 'is_bonus': is_bonus}
        )
        
        db.session.add(transaction)
        transaction.mark_as_completed()
        db.session.commit()
        
        return transaction
    
    @staticmethod
    def create_prize_transaction(user_id, amount, game_id):
        """Cria uma transação de pagamento de prêmio"""
        transaction = Transaction(
            user_id=user_id,
            type='prize_payout',
            amount=Decimal(str(amount)),
            payment_method='wallet',
            description=f'Prêmio do jogo #{game_id}',
            extra_data={'game_id': game_id}
        )
        
        db.session.add(transaction)
        transaction.mark_as_completed()
        db.session.commit()
        
        return transaction
    
    @staticmethod
    def _simulate_pix_payment(transaction):
        """Simula processamento de pagamento PIX"""
        import time
        import threading
        
        def process_payment():
            # Simula delay de processamento
            time.sleep(2)
            
            # Atualiza saldo do usuário
            from src.models.wallet import Wallet
            wallet = Wallet.query.filter_by(user_id=transaction.user_id).first()
            if wallet:
                wallet.add_balance(float(transaction.amount))
                wallet.total_deposited += transaction.amount
                transaction.mark_as_completed()
                db.session.commit()
        
        # Processa em background
        thread = threading.Thread(target=process_payment)
        thread.start()
    
    @staticmethod
    def _process_withdrawal(transaction):
        """Processa saque"""
        from src.models.wallet import Wallet
        
        try:
            wallet = Wallet.query.filter_by(user_id=transaction.user_id).first()
            if wallet and wallet.can_withdraw(float(transaction.amount)):
                wallet.subtract_balance(float(transaction.amount), use_bonus_first=False)
                wallet.total_withdrawn += transaction.amount
                transaction.mark_as_completed()
                db.session.commit()
            else:
                transaction.mark_as_failed("Saldo insuficiente")
                db.session.commit()
        except Exception as e:
            transaction.mark_as_failed(str(e))
            db.session.commit()

