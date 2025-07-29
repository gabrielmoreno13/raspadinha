# 📁 ESTRUTURA COMPLETA DO SISTEMA RASPADINHA

## 🎯 **VISÃO GERAL**
Sistema completo de raspadinha online com 3 componentes principais:
1. **Site Principal** - Jogo de raspadinha para usuários
2. **Dashboard Admin** - Gestão completa do sistema
3. **Landing Page Afiliados** - Captação de influenciadores

---

## 📂 **ESTRUTURA DE ARQUIVOS**

```
raspadinha-completo/
├── raspadinha-backend/          # 🔧 Backend Flask (API)
├── raspadinha-sorte-clone/      # 🎮 Site Principal + Admin
├── afiliados-raspadinha/        # 🔗 Landing Page Afiliados
├── documentacao/                # 📚 Documentação
└── scripts/                     # 🛠️ Scripts de deploy
```

---

## 🔧 **BACKEND (raspadinha-backend/)**

### **Estrutura:**
```
raspadinha-backend/
├── src/
│   ├── main.py                  # Arquivo principal da API
│   ├── models/                  # Modelos de dados
│   │   ├── user.py             # Modelo de usuário
│   │   ├── wallet.py           # Modelo de carteira
│   │   ├── game.py             # Modelo de jogos
│   │   ├── transaction.py      # Modelo de transações
│   │   └── bonus.py            # Modelo de bônus
│   └── routes/                  # Rotas da API
│       ├── auth.py             # Autenticação
│       ├── games.py            # Jogos e raspadinhas
│       ├── wallet.py           # Carteira e transações
│       └── admin.py            # Administração
├── requirements.txt             # Dependências Python
└── .env.example                # Exemplo de configuração
```

### **Funcionalidades:**
- ✅ Sistema de autenticação JWT
- ✅ Gestão de usuários e carteiras
- ✅ Engine de jogos com probabilidades (2% vitória)
- ✅ Sistema de bônus e gamificação
- ✅ Dashboard administrativo
- ✅ Sistema de afiliados completo
- ✅ API RESTful completa

### **Endpoints Principais:**
- `POST /api/auth/register` - Registro de usuários
- `POST /api/auth/login` - Login
- `GET /api/games/categories` - Categorias de jogos
- `POST /api/games/play` - Jogar raspadinha
- `GET /api/wallet/balance` - Saldo da carteira
- `POST /api/wallet/deposit` - Depósito
- `GET /api/admin/stats` - Estatísticas admin

---

## 🎮 **SITE PRINCIPAL (raspadinha-sorte-clone/)**

### **Estrutura:**
```
raspadinha-sorte-clone/
├── src/
│   ├── App.jsx                  # Componente principal
│   ├── components/              # Componentes reutilizáveis
│   │   ├── Header.jsx          # Cabeçalho
│   │   ├── LoginModal.jsx      # Modal de login
│   │   └── ScratchCard.jsx     # Componente de raspadinha
│   ├── pages/                   # Páginas do sistema
│   │   ├── Home.jsx            # Página inicial
│   │   ├── Login.jsx           # Login
│   │   ├── Game.jsx            # Jogo principal
│   │   ├── AffiliateDashboard.jsx  # Dashboard afiliado
│   │   └── AdminDashboard.jsx  # Dashboard admin
│   └── utils/                   # Utilitários
│       └── affiliateSystem.js  # Sistema de afiliados
├── index.html                   # HTML principal
├── package.json                 # Dependências Node.js
└── vite.config.js              # Configuração Vite
```

### **Páginas e Funcionalidades:**

#### **🏠 Página Inicial (Home)**
- Banner principal com premiação
- Feed AO VIVO de ganhadores
- 4 categorias de raspadinha:
  - Raspa da Esperança - R$ 1,00 (até R$ 1.000)
  - Raspa da Alegria - R$ 2,00 (até R$ 5.000)
  - Raspa da Emoção - R$ 5,00 (até R$ 10.000)
  - Raspa do Bixo - R$ 15,00 (até R$ 50.000)

#### **🎮 Jogo de Raspadinha (Game)**
- Grid 3x3 interativo
- Regra: "Ache 3 símbolos iguais"
- Botão "REVELAR TUDO"
- Probabilidade: 2% vitória, 98% derrota
- Prêmio: 20x o valor apostado quando ganha

#### **🛡️ Dashboard Admin**
- Gestão de usuários
- Controle de transações
- Gestão de afiliados
- Relatórios e estatísticas
- Exportação de dados CSV

#### **🔗 Dashboard Afiliado**
- Estatísticas em tempo real
- Link personalizado
- Histórico de conversões
- Solicitação de pagamentos

### **Credenciais de Teste:**
- **Usuário Demo**: demo@raspadinha.com / demo123456
- **Admin**: Senha admin123

---

## 🔗 **LANDING PAGE AFILIADOS (afiliados-raspadinha/)**

### **Estrutura:**
```
afiliados-raspadinha/
├── src/
│   ├── App.jsx                  # Aplicação principal
│   ├── components/              # Componentes
│   │   ├── CadastroForm.jsx    # Formulário de cadastro
│   │   └── ui/                 # Componentes UI
│   └── App.css                 # Estilos
├── index.html                   # HTML principal
└── package.json                # Dependências
```

### **Funcionalidades:**
- ✅ Landing page otimizada para conversão
- ✅ Formulário completo de cadastro
- ✅ Informações sobre comissões (50%)
- ✅ Depoimentos e cases de sucesso
- ✅ FAQ completo
- ✅ Design responsivo

### **Seções da Landing Page:**
1. **Hero Section** - "Ganhe 50% de Comissão Real"
2. **Benefícios** - 6 principais vantagens
3. **Depoimentos** - Histórias de sucesso
4. **Como Funciona** - 4 passos simples
5. **FAQ** - Perguntas frequentes
6. **Formulário** - Cadastro completo

---

## 🔄 **FLUXO DO SISTEMA**

### **1. Usuário Final:**
1. Acessa raspadinhacomsorte.com
2. Faz login ou cadastro
3. Deposita dinheiro via PIX
4. Escolhe categoria de raspadinha
5. Joga e pode ganhar prêmios

### **2. Afiliado/Influenciador:**
1. Acessa raspadinhacomsorte.com/afiliados
2. Preenche formulário de cadastro
3. Recebe link personalizado
4. Divulga nas redes sociais
5. Ganha 50% de cada depósito dos indicados

### **3. Administrador:**
1. Acessa dashboard admin
2. Monitora usuários e transações
3. Gerencia afiliados
4. Processa pagamentos
5. Exporta relatórios

---

## 💰 **SISTEMA DE COMISSÕES**

### **Como Funciona:**
- **Comissão**: 50% sobre cada depósito
- **Tracking**: Por link personalizado (?ref=CODIGO)
- **Pagamento**: PIX em até 24h
- **Mínimo**: R$ 50,00 para saque

### **Exemplo:**
- Indicado deposita R$ 100
- Afiliado ganha R$ 50
- Acompanha tudo em tempo real
- Solicita pagamento quando quiser

---

## 🎯 **PROBABILIDADES E PRÊMIOS**

### **Sistema de Jogos:**
- **Chance de vitória**: 2% (conforme solicitado)
- **Chance de derrota**: 98%
- **Prêmio quando ganha**: 20x o valor apostado
- **Garantia**: Nunca mostra 3 símbolos iguais quando perde

### **Categorias:**
1. **R$ 1,00** → Prêmio máximo R$ 20,00
2. **R$ 2,00** → Prêmio máximo R$ 40,00
3. **R$ 5,00** → Prêmio máximo R$ 100,00
4. **R$ 15,00** → Prêmio máximo R$ 300,00

---

## 🔒 **SEGURANÇA**

### **Medidas Implementadas:**
- ✅ Autenticação JWT
- ✅ Criptografia de senhas (bcrypt)
- ✅ Validação de dados (Marshmallow)
- ✅ CORS configurado
- ✅ Auditoria de transações
- ✅ Controle de acesso por roles

---

## 📊 **ANALYTICS E RELATÓRIOS**

### **Dashboard Admin:**
- KPIs principais em tempo real
- Gráficos de receita e usuários
- Relatórios de afiliados
- Exportação CSV
- Monitoramento de jogos

### **Dashboard Afiliado:**
- Conversões em tempo real
- Histórico de ganhos
- Performance mensal
- Links de divulgação

---

## 🚀 **TECNOLOGIAS UTILIZADAS**

### **Backend:**
- Python 3.11
- Flask (API REST)
- SQLite (banco de dados)
- JWT (autenticação)
- Bcrypt (criptografia)

### **Frontend:**
- React 18
- Vite (build tool)
- Tailwind CSS
- Lucide Icons
- React Router

### **Deploy:**
- Nginx (servidor web)
- PM2 (gerenciador de processos)
- Certbot (SSL)
- Ubuntu 22.04

---

## 📞 **SUPORTE E MANUTENÇÃO**

### **Logs Importantes:**
- Backend: `pm2 logs raspadinha-backend`
- Nginx: `/var/log/nginx/error.log`
- Sistema: `journalctl -u nginx`

### **Comandos de Manutenção:**
```bash
# Reiniciar backend
pm2 restart raspadinha-backend

# Reiniciar Nginx
systemctl restart nginx

# Backup banco
cp raspadinha.db backup/

# Ver status
pm2 status
systemctl status nginx
```

---

**🎉 Sistema completo e pronto para produção!**

