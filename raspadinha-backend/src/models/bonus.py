from src.models.user import db
from datetime import datetime, timedelta
from decimal import Decimal
import json

class Bonus(db.Model):
    __tablename__ = 'bonuses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # welcome, reload, daily, referral, mission
    amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    free_games = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, claimed, expired
    expires_at = db.Column(db.DateTime)
    claimed_at = db.Column(db.DateTime)
    extra_data = db.Column(db.JSON)  # Dados específicos do bônus
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Bonus {self.id} {self.type} User:{self.user_id}>'

    def is_expired(self):
        """Verifica se o bônus expirou"""
        return self.expires_at and datetime.utcnow() > self.expires_at

    def claim(self):
        """Resgata o bônus"""
        if self.status != 'active':
            raise ValueError("Bônus não está ativo")
        
        if self.is_expired():
            self.status = 'expired'
            raise ValueError("Bônus expirado")
        
        self.status = 'claimed'
        self.claimed_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': float(self.amount),
            'free_games': self.free_games,
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'metadata': self.extra_data,
            'created_at': self.created_at.isoformat(),
            'is_expired': self.is_expired()
        }

class Mission(db.Model):
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # daily, weekly, achievement
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_value = db.Column(db.Integer, nullable=False)  # Valor alvo para completar
    current_value = db.Column(db.Integer, default=0)  # Progresso atual
    reward_type = db.Column(db.String(20))  # points, free_games, bonus_money
    reward_value = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='active')  # active, completed, claimed
    expires_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Mission {self.id} {self.name} User:{self.user_id}>'

    def update_progress(self, increment=1):
        """Atualiza o progresso da missão"""
        if self.status != 'active':
            return False
        
        self.current_value += increment
        
        if self.current_value >= self.target_value:
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
            return True
        
        return False

    def claim_reward(self):
        """Resgata a recompensa da missão"""
        if self.status != 'completed':
            raise ValueError("Missão não foi completada")
        
        self.status = 'claimed'
        return {
            'type': self.reward_type,
            'value': float(self.reward_value) if self.reward_value else 0
        }

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'progress_percentage': (self.current_value / self.target_value * 100) if self.target_value > 0 else 0,
            'reward_type': self.reward_type,
            'reward_value': float(self.reward_value) if self.reward_value else 0,
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat()
        }

class BonusService:
    """Serviço para gerenciamento de bônus e gamificação"""
    
    @staticmethod
    def create_welcome_bonus(user_id):
        """Cria bônus de boas-vindas"""
        bonus = Bonus(
            user_id=user_id,
            type='welcome',
            free_games=3,
            expires_at=datetime.utcnow() + timedelta(days=7),
            extra_data={'description': 'Bônus de boas-vindas - 3 jogos grátis'}
        )
        
        db.session.add(bonus)
        db.session.commit()
        return bonus
    
    @staticmethod
    def create_daily_bonus(user_id):
        """Cria bônus diário"""
        # Verifica se já recebeu hoje
        today = datetime.utcnow().date()
        existing = Bonus.query.filter_by(
            user_id=user_id,
            type='daily'
        ).filter(
            db.func.date(Bonus.created_at) == today
        ).first()
        
        if existing:
            return None
        
        bonus = Bonus(
            user_id=user_id,
            type='daily',
            free_games=1,
            expires_at=datetime.utcnow() + timedelta(hours=24),
            extra_data={'description': 'Jogo grátis diário'}
        )
        
        db.session.add(bonus)
        db.session.commit()
        return bonus
    
    @staticmethod
    def create_reload_bonus(user_id, deposit_amount):
        """Cria bônus de recarga baseado no depósito"""
        bonus_percentage = 0
        
        if deposit_amount >= 500:
            bonus_percentage = 0.20  # 20%
        elif deposit_amount >= 200:
            bonus_percentage = 0.15  # 15%
        elif deposit_amount >= 100:
            bonus_percentage = 0.10  # 10%
        
        if bonus_percentage > 0:
            bonus_amount = deposit_amount * bonus_percentage
            
            bonus = Bonus(
                user_id=user_id,
                type='reload',
                amount=Decimal(str(bonus_amount)),
                expires_at=datetime.utcnow() + timedelta(days=30),
                extra_data={
                    'description': f'Bônus de recarga {int(bonus_percentage*100)}%',
                    'deposit_amount': float(deposit_amount)
                }
            )
            
            db.session.add(bonus)
            db.session.commit()
            return bonus
        
        return None
    
    @staticmethod
    def create_daily_missions(user_id):
        """Cria missões diárias para o usuário"""
        today = datetime.utcnow().date()
        
        # Verifica se já tem missões para hoje
        existing = Mission.query.filter_by(
            user_id=user_id,
            type='daily'
        ).filter(
            db.func.date(Mission.created_at) == today
        ).first()
        
        if existing:
            return []
        
        missions = [
            {
                'name': 'Jogue 3 raspadinhas',
                'description': 'Jogue 3 raspadinhas hoje',
                'target_value': 3,
                'reward_type': 'points',
                'reward_value': 50
            },
            {
                'name': 'Ganhe um prêmio',
                'description': 'Ganhe pelo menos um prêmio hoje',
                'target_value': 1,
                'reward_type': 'free_games',
                'reward_value': 1
            }
        ]
        
        created_missions = []
        for mission_data in missions:
            mission = Mission(
                user_id=user_id,
                type='daily',
                name=mission_data['name'],
                description=mission_data['description'],
                target_value=mission_data['target_value'],
                reward_type=mission_data['reward_type'],
                reward_value=Decimal(str(mission_data['reward_value'])),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            
            db.session.add(mission)
            created_missions.append(mission)
        
        db.session.commit()
        return created_missions
    
    @staticmethod
    def update_user_missions(user_id, action, value=1):
        """Atualiza progresso das missões do usuário"""
        active_missions = Mission.query.filter_by(
            user_id=user_id,
            status='active'
        ).all()
        
        completed_missions = []
        
        for mission in active_missions:
            # Mapeia ações para tipos de missão
            if action == 'game_played' and 'jogue' in mission.name.lower():
                if mission.update_progress(value):
                    completed_missions.append(mission)
            elif action == 'prize_won' and 'ganhe' in mission.name.lower():
                if mission.update_progress(value):
                    completed_missions.append(mission)
        
        if completed_missions:
            db.session.commit()
        
        return completed_missions
    
    @staticmethod
    def update_loyalty_points(user_id, amount_spent):
        """Atualiza pontos de fidelidade do usuário"""
        from src.models.user import User
        
        user = User.query.get(user_id)
        if not user:
            return
        
        # 1 real = 10 pontos
        points_earned = int(float(amount_spent) * 10)
        user.loyalty_points += points_earned
        
        # Verifica mudança de nível
        old_level = user.loyalty_level
        new_level = BonusService._calculate_loyalty_level(user.loyalty_points)
        
        if new_level != old_level:
            user.loyalty_level = new_level
            # Cria bônus de upgrade de nível
            BonusService._create_level_up_bonus(user_id, new_level)
        
        db.session.commit()
        return points_earned
    
    @staticmethod
    def _calculate_loyalty_level(points):
        """Calcula nível de fidelidade baseado nos pontos"""
        if points >= 20000:
            return 'diamond'
        elif points >= 5000:
            return 'gold'
        elif points >= 1000:
            return 'silver'
        else:
            return 'bronze'
    
    @staticmethod
    def _create_level_up_bonus(user_id, new_level):
        """Cria bônus de upgrade de nível"""
        level_bonuses = {
            'silver': {'free_games': 2, 'amount': 10},
            'gold': {'free_games': 5, 'amount': 25},
            'diamond': {'free_games': 10, 'amount': 50}
        }
        
        if new_level in level_bonuses:
            bonus_data = level_bonuses[new_level]
            
            bonus = Bonus(
                user_id=user_id,
                type='level_up',
                amount=Decimal(str(bonus_data['amount'])),
                free_games=bonus_data['free_games'],
                expires_at=datetime.utcnow() + timedelta(days=30),
                extra_data={
                    'description': f'Parabéns! Você alcançou o nível {new_level.title()}!',
                    'level': new_level
                }
            )
            
            db.session.add(bonus)
            db.session.commit()
            return bonus
        
        return None

