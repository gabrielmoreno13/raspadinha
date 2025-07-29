# Mecanismos de Bônus e Engajamento - Sistema Raspadinha Online

## 1. SISTEMA DE BÔNUS PRINCIPAL

### 1.1 Bônus de Boas-Vindas
**Objetivo**: Converter visitantes em jogadores ativos
**Mecânica**: 
- Primeiro depósito de R$ 50+ = 3 raspadinhas grátis
- Primeiro depósito de R$ 100+ = 5 raspadinhas grátis + 1 raspadinha premium
- Validade: 7 dias após registro

**Implementação Técnica**:
```
- Flag no banco: first_deposit_bonus_used
- Trigger automático no primeiro depósito
- Raspadinhas creditadas na carteira virtual
```

### 1.2 Bônus de Recarga
**Objetivo**: Incentivar depósitos maiores e frequentes
**Mecânica**:
- Depósito R$ 100-199: +10% em raspadinhas grátis
- Depósito R$ 200-499: +15% em raspadinhas grátis  
- Depósito R$ 500+: +20% em raspadinhas grátis

**Exemplo**: Depósito de R$ 200 = 20 raspadinhas + 3 grátis (15%)

### 1.3 Raspadinha Diária Grátis
**Objetivo**: Manter usuários engajados diariamente
**Mecânica**:
- 1 raspadinha grátis por dia para usuários ativos
- Usuário ativo = login + pelo menos 1 jogo nos últimos 7 dias
- Reset às 00:00 (horário de Brasília)
- Prêmios limitados: máximo R$ 50

## 2. PROGRAMA DE FIDELIDADE

### 2.1 Sistema de Pontos
**Conversão**: 1 real gasto = 10 pontos
**Resgate**: 1000 pontos = 1 raspadinha grátis

**Níveis de Fidelidade**:
- **Bronze** (0-999 pontos): Bônus padrão
- **Prata** (1000-4999 pontos): +5% pontos extras
- **Ouro** (5000-19999 pontos): +10% pontos + 1 raspadinha grátis/semana
- **Diamante** (20000+ pontos): +15% pontos + 2 raspadinhas grátis/semana + suporte prioritário

### 2.2 Benefícios por Nível
**Bronze**: Acesso básico
**Prata**: 
- Notificações prioritárias de promoções
- Acesso antecipado a novas categorias

**Ouro**:
- Cashback de 2% em perdas mensais
- Convites para eventos especiais
- Limites de saque aumentados

**Diamante**:
- Gerente de conta dedicado
- Bônus personalizados
- Beta tester de novos jogos

## 3. MISSÕES E DESAFIOS

### 3.1 Missões Diárias
**Renovação**: Todo dia às 00:00
**Exemplos**:
- "Jogue 3 raspadinhas hoje" → Recompensa: 50 pontos
- "Ganhe pelo menos 1 prêmio hoje" → Recompensa: 1 raspadinha grátis
- "Faça login por 3 dias consecutivos" → Recompensa: 100 pontos

### 3.2 Desafios Semanais
**Renovação**: Toda segunda-feira
**Exemplos**:
- "Ganhe R$ 100 em prêmios esta semana" → Recompensa: 3 raspadinhas grátis
- "Jogue 20 raspadinhas esta semana" → Recompensa: 1 raspadinha premium
- "Convide 2 amigos que façam depósito" → Recompensa: R$ 50 em créditos

### 3.3 Conquistas Especiais
**Permanentes**: Uma vez desbloqueadas, ficam no perfil
**Exemplos**:
- "Primeira Vitória": Ganhe seu primeiro prêmio
- "Sortudo": Ganhe 3 prêmios em sequência
- "Milionário": Acumule R$ 1000 em ganhos totais
- "Fiel": Jogue por 30 dias consecutivos
- "Influencer": Convide 10 amigos que se registrem

## 4. PROMOÇÕES ESPECIAIS

### 4.1 Promoções Sazonais
**Carnaval** (Fevereiro/Março):
- Raspadinhas temáticas com prêmios dobrados
- "Bloco da Sorte": 5 raspadinhas pelo preço de 4

**Festa Junina** (Junho):
- "Quadrilha da Sorte": Prêmios especiais em raspadinhas temáticas
- Bônus de 25% em todos os depósitos

**Black Friday** (Novembro):
- 50% de desconto em pacotes de raspadinhas
- Mega sorteio com prêmio de R$ 10.000

**Natal/Ano Novo** (Dezembro):
- "Calendário do Advento": 1 surpresa por dia
- Raspadinhas especiais com prêmios únicos

### 4.2 Promoções Flash
**Duração**: 2-6 horas
**Frequência**: 1-2 vezes por semana
**Exemplos**:
- "Happy Hour": Dobro de pontos das 18h às 20h
- "Madrugada da Sorte": Raspadinhas grátis das 2h às 4h
- "Almoço Premiado": Bônus especial das 12h às 14h

### 4.3 Torneios e Competições
**Torneio Semanal**:
- Ranking de maiores ganhos da semana
- Top 10 ganham prêmios especiais
- 1º lugar: R$ 500 + título "Campeão da Semana"

**Liga Mensal**:
- Pontuação baseada em frequência e ganhos
- Divisões: Bronze, Prata, Ouro, Diamante
- Promoção/rebaixamento entre divisões

## 5. SISTEMA DE INDICAÇÃO

### 5.1 Programa "Convide e Ganhe"
**Para o Indicador**:
- R$ 10 em créditos quando amigo faz primeiro depósito
- 5% de comissão vitalícia nos jogos do amigo (máximo R$ 100/mês)
- Bônus especial a cada 5 amigos indicados

**Para o Indicado**:
- 2 raspadinhas grátis ao se registrar via link
- Bônus de boas-vindas aumentado em 50%

### 5.2 Programa de Afiliados
**Para Influencers/Sites**:
- Comissão de 10-15% sobre receita líquida
- Material promocional personalizado
- Dashboard com métricas detalhadas
- Pagamentos mensais via PIX

## 6. MECÂNICAS PSICOLÓGICAS

### 6.1 Efeito de Quase-Ganho
**Implementação**:
- 15% das raspadinhas perdedoras mostram "2 de 3" símbolos iguais
- Mensagem: "Quase lá! Tente novamente!"
- Oferta imediata: "Jogue mais 3 por R$ 25"

### 6.2 Celebração de Vitórias
**Prêmios Pequenos** (R$ 10-50):
- Animação simples + som de moedas
- Mensagem: "Parabéns! Você ganhou!"

**Prêmios Médios** (R$ 100-500):
- Animação elaborada + fogos de artifício
- Compartilhamento automático no feed
- Oferta: "Está com sorte! Jogue mais!"

**Prêmios Grandes** (R$ 1000+):
- Animação épica + música triunfal
- Notificação para todos os usuários online
- Entrevista opcional para o blog do site

### 6.3 Urgência e Escassez
**Ofertas Limitadas**:
- "Apenas 100 raspadinhas especiais disponíveis!"
- Timer regressivo em promoções
- "Últimas 2 horas para aproveitar!"

**Estoque Dinâmico**:
- "Restam apenas 23 raspadinhas desta categoria hoje"
- Reposição automática baseada na demanda

## 7. NOTIFICAÇÕES E COMUNICAÇÃO

### 7.1 Push Notifications
**Engajamento**:
- "Sua raspadinha diária está disponível!"
- "João ganhou R$ 1.000! Será que é sua vez?"
- "Promoção especial termina em 1 hora!"

**Reativação**:
- "Sentimos sua falta! Volte e ganhe 2 raspadinhas grátis"
- "Seus pontos de fidelidade expiram em 3 dias"

### 7.2 Email Marketing
**Boas-vindas**: Sequência de 5 emails explicando o sistema
**Newsletters**: Semanais com novidades e promoções
**Reativação**: Para usuários inativos há 7+ dias
**Aniversário**: Email especial com bônus personalizado

### 7.3 SMS (Opcional)
**Ganhos Importantes**: "Parabéns! Você ganhou R$ 500!"
**Saques**: "Seu saque de R$ 200 foi processado"
**Segurança**: "Login detectado de novo dispositivo"

## 8. ANÁLISE E OTIMIZAÇÃO

### 8.1 Métricas de Bônus
- **Taxa de conversão** de bônus em depósitos
- **Lifetime Value** de usuários com vs sem bônus
- **Custo de aquisição** por canal de bônus
- **Retenção** por tipo de bônus recebido

### 8.2 A/B Testing
**Testes Contínuos**:
- Valores de bônus (10% vs 15% vs 20%)
- Timing de ofertas (imediato vs 24h vs 7 dias)
- Formatos de notificação (popup vs banner vs email)
- Mecânicas de gamificação (pontos vs badges vs níveis)

### 8.3 Personalização
**Segmentação de Usuários**:
- **Novatos**: Foco em educação e primeiros ganhos
- **Regulares**: Fidelização e aumento de frequência
- **VIPs**: Experiência premium e atendimento especial
- **Inativos**: Campanhas de reativação agressivas

**Ofertas Personalizadas**:
- Baseadas no histórico de jogo
- Horários preferenciais de jogo
- Categorias favoritas de raspadinha
- Padrões de depósito e saque

