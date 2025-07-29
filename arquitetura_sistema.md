# Arquitetura Técnica - Sistema de Raspadinha Online

## 1. VISÃO GERAL DA ARQUITETURA

### 1.1 Arquitetura Geral do Sistema

O sistema de raspadinha online será desenvolvido seguindo uma arquitetura moderna de microserviços com separação clara entre frontend e backend. A escolha por esta arquitetura permite escalabilidade, manutenibilidade e facilita futuras expansões do sistema.

**Componentes Principais:**
- **Frontend**: React.js com TypeScript para interface do usuário
- **Backend**: Flask (Python) com APIs RESTful
- **Banco de Dados**: PostgreSQL para dados transacionais + Redis para cache
- **Pagamentos**: Integração com gateways PIX e cartão de crédito
- **Infraestrutura**: Docker containers com deploy em cloud

### 1.2 Princípios Arquiteturais

**Segurança por Design**: Todas as comunicações criptografadas, autenticação robusta e auditoria completa de transações financeiras.

**Escalabilidade Horizontal**: Componentes stateless que podem ser replicados conforme demanda.

**Resiliência**: Tratamento de falhas, circuit breakers e fallbacks para garantir disponibilidade.

**Observabilidade**: Logs estruturados, métricas e tracing distribuído para monitoramento proativo.

## 2. ARQUITETURA DE BACKEND

### 2.1 Estrutura da API Flask

```
raspadinha-backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   ├── game.py
│   │   ├── transaction.py
│   │   ├── bonus.py
│   │   └── scratch_card.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── games.py
│   │   ├── payments.py
│   │   ├── admin.py
│   │   └── bonus.py
│   ├── services/
│   │   ├── game_engine.py
│   │   ├── payment_service.py
│   │   ├── bonus_service.py
│   │   ├── notification_service.py
│   │   └── analytics_service.py
│   ├── utils/
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config.py
├── migrations/
├── tests/
├── requirements.txt
└── docker-compose.yml
```

### 2.2 Endpoints Principais da API

**Autenticação e Usuários:**
```
POST /api/auth/register - Registro de usuário
POST /api/auth/login - Login
POST /api/auth/logout - Logout
POST /api/auth/forgot-password - Recuperação de senha
GET /api/user/profile - Perfil do usuário
PUT /api/user/profile - Atualizar perfil
GET /api/user/history - Histórico de jogos
```

**Jogos e Raspadinhas:**
```
GET /api/games/categories - Listar categorias
GET /api/games/available - Raspadinhas disponíveis
POST /api/games/play - Jogar raspadinha
GET /api/games/result/{game_id} - Resultado do jogo
GET /api/games/leaderboard - Ranking de ganhadores
```

**Pagamentos e Carteira:**
```
GET /api/wallet/balance - Saldo da carteira
POST /api/payments/deposit - Fazer depósito
POST /api/payments/withdraw - Solicitar saque
GET /api/payments/history - Histórico financeiro
POST /api/payments/pix - Pagamento via PIX
```

**Bônus e Promoções:**
```
GET /api/bonus/available - Bônus disponíveis
POST /api/bonus/claim - Resgatar bônus
GET /api/bonus/history - Histórico de bônus
GET /api/missions/daily - Missões diárias
POST /api/missions/complete - Completar missão
```

**Administração:**
```
GET /api/admin/users - Listar usuários
GET /api/admin/analytics - Analytics do sistema
PUT /api/admin/game-config - Configurar jogos
GET /api/admin/transactions - Transações financeiras
POST /api/admin/promotions - Criar promoções
```

### 2.3 Modelo de Dados

**Tabela Users:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    cpf VARCHAR(14) UNIQUE,
    status VARCHAR(20) DEFAULT 'active',
    loyalty_level VARCHAR(20) DEFAULT 'bronze',
    loyalty_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT FALSE
);
```

**Tabela Wallets:**
```sql
CREATE TABLE wallets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    balance DECIMAL(10,2) DEFAULT 0.00,
    bonus_balance DECIMAL(10,2) DEFAULT 0.00,
    total_deposited DECIMAL(10,2) DEFAULT 0.00,
    total_withdrawn DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabela Scratch_Cards:**
```sql
CREATE TABLE scratch_cards (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    theme VARCHAR(50) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    symbols JSONB NOT NULL,
    winning_combination JSONB,
    prize_amount DECIMAL(10,2),
    probability DECIMAL(8,6) NOT NULL,
    is_winner BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabela Games:**
```sql
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    scratch_card_id INTEGER REFERENCES scratch_cards(id),
    amount_paid DECIMAL(8,2) NOT NULL,
    prize_won DECIMAL(10,2) DEFAULT 0.00,
    is_bonus_game BOOLEAN DEFAULT FALSE,
    game_data JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Tabela Transactions:**
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(20) NOT NULL, -- deposit, withdrawal, game_cost, prize_payout
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    external_transaction_id VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);
```

**Tabela Bonuses:**
```sql
CREATE TABLE bonuses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(50) NOT NULL, -- welcome, reload, daily, referral
    amount DECIMAL(10,2),
    free_games INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    expires_at TIMESTAMP,
    claimed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 Serviços Especializados

**Game Engine Service:**
Responsável pela lógica central dos jogos, incluindo geração de raspadinhas, cálculo de probabilidades e determinação de prêmios.

```python
class GameEngine:
    def generate_scratch_card(self, category, user_id):
        # Gera uma nova raspadinha baseada na categoria
        # Aplica probabilidades configuradas
        # Considera histórico do usuário para balanceamento
        
    def calculate_win_probability(self, user_data, category):
        # Calcula probabilidade dinâmica baseada em:
        # - Histórico de jogos do usuário
        # - Margem de lucro desejada
        # - Configurações administrativas
        
    def process_game_result(self, game_id, revealed_symbols):
        # Processa resultado da raspagem
        # Valida símbolos revelados
        # Calcula prêmio e atualiza carteira
```

**Payment Service:**
Gerencia todas as transações financeiras, integrações com gateways de pagamento e processamento de PIX.

```python
class PaymentService:
    def process_pix_payment(self, user_id, amount):
        # Integração com API PIX
        # Geração de QR Code
        # Webhook para confirmação
        
    def process_withdrawal(self, user_id, amount, pix_key):
        # Validações de segurança
        # Processamento de saque via PIX
        # Notificações ao usuário
        
    def handle_payment_webhook(self, payment_data):
        # Processa confirmações de pagamento
        # Atualiza saldo do usuário
        # Dispara notificações
```

**Bonus Service:**
Controla todo o sistema de bônus, missões e programa de fidelidade.

```python
class BonusService:
    def check_daily_bonus(self, user_id):
        # Verifica elegibilidade para bônus diário
        # Aplica bônus automaticamente
        
    def process_loyalty_points(self, user_id, amount_spent):
        # Calcula pontos de fidelidade
        # Verifica mudanças de nível
        # Aplica benefícios automáticos
        
    def evaluate_missions(self, user_id, action):
        # Avalia progresso em missões
        # Completa missões automaticamente
        # Distribui recompensas
```

## 3. ARQUITETURA DE FRONTEND

### 3.1 Estrutura do Projeto React

```
raspadinha-frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── assets/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── Modal.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ForgotPassword.tsx
│   │   ├── games/
│   │   │   ├── ScratchCard.tsx
│   │   │   ├── GameBoard.tsx
│   │   │   ├── CategorySelector.tsx
│   │   │   └── WinnersFeed.tsx
│   │   ├── wallet/
│   │   │   ├── Balance.tsx
│   │   │   ├── DepositForm.tsx
│   │   │   ├── WithdrawForm.tsx
│   │   │   └── TransactionHistory.tsx
│   │   └── admin/
│   │       ├── Dashboard.tsx
│   │       ├── UserManagement.tsx
│   │       ├── GameConfig.tsx
│   │       └── Analytics.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Games.tsx
│   │   ├── Profile.tsx
│   │   ├── Wallet.tsx
│   │   └── Admin.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useWallet.ts
│   │   ├── useGames.ts
│   │   └── useWebSocket.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── games.ts
│   │   └── payments.ts
│   ├── store/
│   │   ├── authSlice.ts
│   │   ├── gamesSlice.ts
│   │   ├── walletSlice.ts
│   │   └── store.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── validators.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── components.css
│   │   └── animations.css
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

### 3.2 Componentes Principais

**ScratchCard Component:**
Componente central que renderiza a raspadinha interativa com animações de raspagem.

```typescript
interface ScratchCardProps {
  cardData: ScratchCardData;
  onReveal: (symbols: string[]) => void;
  onComplete: (result: GameResult) => void;
}

const ScratchCard: React.FC<ScratchCardProps> = ({
  cardData,
  onReveal,
  onComplete
}) => {
  // Canvas para renderização da raspagem
  // Detecção de mouse/touch para interação
  // Animações de revelação
  // Efeitos sonoros e visuais
};
```

**GameBoard Component:**
Área principal onde o usuário seleciona e joga raspadinhas.

```typescript
const GameBoard: React.FC = () => {
  // Estado do jogo atual
  // Seleção de categoria
  // Histórico de jogos recentes
  // Feed de ganhadores em tempo real
};
```

**WinnersFeed Component:**
Feed em tempo real mostrando ganhadores recentes.

```typescript
const WinnersFeed: React.FC = () => {
  // WebSocket connection para updates em tempo real
  // Animações de entrada para novos ganhadores
  // Filtros por valor de prêmio
};
```

### 3.3 Gerenciamento de Estado

Utilizando Redux Toolkit para gerenciamento de estado global:

**Auth Slice:**
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => { state.loading = true; },
    loginSuccess: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
      state.loading = false;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    }
  }
});
```

**Games Slice:**
```typescript
interface GamesState {
  currentGame: Game | null;
  availableCards: ScratchCard[];
  gameHistory: Game[];
  winnersFeed: Winner[];
  categories: Category[];
}
```

**Wallet Slice:**
```typescript
interface WalletState {
  balance: number;
  bonusBalance: number;
  transactions: Transaction[];
  pendingDeposits: Deposit[];
}
```

### 3.4 Integração com APIs

**API Service:**
```typescript
class ApiService {
  private baseURL = process.env.REACT_APP_API_URL;
  private token = localStorage.getItem('token');

  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    // Interceptor para adicionar token de autenticação
    // Tratamento de erros global
    // Retry automático para falhas de rede
  }

  // Métodos específicos para cada endpoint
  async playGame(cardId: string): Promise<GameResult> { }
  async getWalletBalance(): Promise<WalletData> { }
  async processDeposit(amount: number): Promise<DepositResult> { }
}
```

## 4. SEGURANÇA E COMPLIANCE

### 4.1 Autenticação e Autorização

**JWT (JSON Web Tokens):**
- Tokens com expiração de 24 horas
- Refresh tokens para renovação automática
- Blacklist de tokens revogados

**Autenticação Multifator (2FA):**
- TOTP (Time-based One-Time Password)
- SMS como fallback
- Obrigatório para transações acima de R$ 500

**Controle de Acesso:**
```python
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated_function
```

### 4.2 Proteção de Dados

**Criptografia:**
- TLS 1.3 para todas as comunicações
- AES-256 para dados sensíveis em repouso
- Hashing bcrypt para senhas (cost factor 12)

**Validação de Entrada:**
```python
from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    cpf = fields.Str(required=True, validate=validate_cpf)
    birth_date = fields.Date(required=True)
    
    @validates('birth_date')
    def validate_age(self, value):
        if calculate_age(value) < 18:
            raise ValidationError('Usuário deve ser maior de idade')
```

**Auditoria:**
```python
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    resource = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.JSON)
```

### 4.3 Prevenção de Fraudes

**Rate Limiting:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@app.route('/api/games/play')
@limiter.limit("10 per minute")
def play_game():
    # Máximo 10 jogos por minuto por IP
```

**Detecção de Padrões Suspeitos:**
```python
class FraudDetection:
    def analyze_user_behavior(self, user_id):
        # Análise de padrões de jogo
        # Detecção de múltiplas contas
        # Verificação de dispositivos suspeitos
        
    def check_transaction_risk(self, transaction):
        # Análise de risco em tempo real
        # Verificação de listas negras
        # Scoring baseado em ML
```

## 5. INFRAESTRUTURA E DEPLOY

### 5.1 Containerização

**Dockerfile Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Dockerfile Frontend:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/raspadinha
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: raspadinha
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 5.2 Monitoramento e Observabilidade

**Logging Estruturado:**
```python
import structlog

logger = structlog.get_logger()

@app.route('/api/games/play')
def play_game():
    logger.info(
        "game_started",
        user_id=current_user.id,
        card_category=request.json.get('category'),
        amount=request.json.get('amount')
    )
```

**Métricas com Prometheus:**
```python
from prometheus_client import Counter, Histogram, generate_latest

GAMES_PLAYED = Counter('games_played_total', 'Total games played', ['category'])
GAME_DURATION = Histogram('game_duration_seconds', 'Game duration')
REVENUE = Counter('revenue_total', 'Total revenue', ['payment_method'])

@app.route('/metrics')
def metrics():
    return generate_latest()
```

**Health Checks:**
```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'payment_gateway': check_payment_gateway()
    }
    
    status = 'healthy' if all(checks.values()) else 'unhealthy'
    return {'status': status, 'checks': checks}
```

### 5.3 Backup e Recuperação

**Backup Automatizado:**
```bash
#!/bin/bash
# backup_script.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup do PostgreSQL
pg_dump $DATABASE_URL > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de arquivos estáticos
tar -czf $BACKUP_DIR/static_backup_$DATE.tar.gz /app/static

# Upload para S3
aws s3 cp $BACKUP_DIR/ s3://raspadinha-backups/ --recursive
```

**Plano de Recuperação:**
1. **RTO (Recovery Time Objective)**: 4 horas
2. **RPO (Recovery Point Objective)**: 1 hora
3. **Backup incremental**: A cada hora
4. **Backup completo**: Diário às 2h da manhã
5. **Teste de recuperação**: Mensal

## 6. PERFORMANCE E ESCALABILIDADE

### 6.1 Otimizações de Performance

**Cache Strategy:**
```python
import redis
from functools import wraps

redis_client = redis.Redis(host='redis', port=6379, db=0)

def cache_result(expiration=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            
            if cached_result:
                return json.loads(cached_result)
            
            result = f(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return decorated_function
    return decorator

@cache_result(expiration=600)
def get_game_categories():
    return Category.query.all()
```

**Database Optimization:**
```sql
-- Índices para consultas frequentes
CREATE INDEX idx_games_user_id_created ON games(user_id, created_at DESC);
CREATE INDEX idx_transactions_user_status ON transactions(user_id, status);
CREATE INDEX idx_users_email_status ON users(email, status);

-- Particionamento por data para tabelas grandes
CREATE TABLE games_2024 PARTITION OF games
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

**Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### 6.2 Estratégia de Escalabilidade

**Load Balancing:**
```nginx
upstream backend {
    server backend1:5000 weight=3;
    server backend2:5000 weight=3;
    server backend3:5000 weight=2;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Auto Scaling:**
```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: raspadinha-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: raspadinha-backend
  template:
    spec:
      containers:
      - name: backend
        image: raspadinha/backend:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: raspadinha-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: raspadinha-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Esta arquitetura técnica fornece uma base sólida para o desenvolvimento do sistema de raspadinha online, garantindo escalabilidade, segurança e performance adequadas para suportar milhares de usuários simultâneos e transações financeiras seguras.

