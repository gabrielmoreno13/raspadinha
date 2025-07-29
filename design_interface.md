# Design de Interface e Experiência do Usuário - Sistema Raspadinha Online

## 1. PRINCÍPIOS DE DESIGN

### 1.1 Filosofia de Design

O design da plataforma de raspadinha online deve transmitir **confiança, diversão e simplicidade**. A interface precisa ser intuitiva o suficiente para que qualquer usuário, independente de sua familiaridade com tecnologia, possa navegar e jogar facilmente.

**Princípios Fundamentais:**

**Clareza Visual**: Hierarquia clara de informações, com destaque para elementos importantes como saldo, botões de ação e resultados de jogos.

**Feedback Imediato**: Toda ação do usuário deve ter uma resposta visual ou sonora imediata, especialmente durante a raspagem das cartas.

**Confiabilidade**: Design profissional que transmita segurança, especialmente importante para transações financeiras.

**Gamificação Sutil**: Elementos lúdicos que aumentem o engajamento sem comprometer a seriedade da plataforma.

**Acessibilidade**: Interface que funcione bem em diferentes dispositivos e seja acessível para usuários com necessidades especiais.

### 1.2 Paleta de Cores

**Cores Primárias:**
- **Verde Principal**: #2ECC71 (confiança, dinheiro, sucesso)
- **Verde Escuro**: #27AE60 (botões hover, elementos secundários)
- **Dourado**: #F1C40F (prêmios, elementos premium, destaques)

**Cores Secundárias:**
- **Azul Confiança**: #3498DB (links, informações)
- **Vermelho Alerta**: #E74C3C (avisos, erros)
- **Cinza Neutro**: #95A5A6 (textos secundários)
- **Branco**: #FFFFFF (backgrounds, cards)
- **Preto Suave**: #2C3E50 (textos principais)

**Gradientes:**
- **Sucesso**: Linear gradient de #2ECC71 para #27AE60
- **Premium**: Linear gradient de #F1C40F para #F39C12
- **Neutro**: Linear gradient de #ECF0F1 para #BDC3C7

### 1.3 Tipografia

**Fonte Principal**: Inter (Google Fonts)
- Excelente legibilidade em telas
- Suporte completo a caracteres especiais
- Variações de peso disponíveis

**Hierarquia Tipográfica:**
- **H1**: 32px, weight 700 (títulos principais)
- **H2**: 24px, weight 600 (subtítulos)
- **H3**: 20px, weight 600 (seções)
- **Body**: 16px, weight 400 (texto padrão)
- **Small**: 14px, weight 400 (textos secundários)
- **Caption**: 12px, weight 500 (legendas, labels)

## 2. LAYOUT E ESTRUTURA

### 2.1 Header Principal

**Elementos do Header:**
```
[LOGO] [Início] [Jogos] [Promoções] [Suporte]     [Saldo: R$ 150,00] [Perfil ▼] [Notificações 🔔]
```

**Especificações:**
- Altura: 70px
- Background: Branco com sombra sutil
- Logo: 180px de largura
- Saldo destacado em verde com ícone de carteira
- Notificações com badge para itens não lidos

**Versão Mobile:**
```
[☰] [LOGO]                    [Saldo] [👤]
```

### 2.2 Sidebar de Navegação (Desktop)

**Menu Principal:**
- 🏠 Início
- 🎮 Jogar Agora
- 🏆 Meus Jogos
- 💰 Carteira
- 🎁 Bônus
- 📊 Estatísticas
- ⚙️ Configurações

**Seção de Status:**
- Nível atual do usuário
- Progresso para próximo nível
- Pontos de fidelidade
- Missões ativas

### 2.3 Área Principal de Conteúdo

**Layout Grid:**
```
┌─────────────────────────────────────────────────┐
│                 HERO BANNER                     │
│            (Promoção Principal)                 │
├─────────────────────────────────────────────────┤
│  FEED GANHADORES  │    CATEGORIAS RASPADINHA    │
│     (Sidebar)     │        (Grid 2x2)           │
│                   │                             │
│   João G. ganhou  │  [Raspa Sorte] [Raspa Ouro] │
│     R$ 500!       │                             │
│                   │  [Raspa Animal][Raspa Sport]│
│   Maria S. ganhou │                             │
│     R$ 1.200!     │                             │
├─────────────────────────────────────────────────┤
│              ESTATÍSTICAS RÁPIDAS               │
│   Total Jogadores: 15.847 | Prêmios Hoje: R$ 45.230 │
└─────────────────────────────────────────────────┘
```

## 3. COMPONENTES ESPECÍFICOS

### 3.1 Card de Raspadinha

**Design Visual:**
- Dimensões: 300x200px (desktop), 280x180px (mobile)
- Border radius: 12px
- Box shadow: 0 4px 12px rgba(0,0,0,0.1)
- Hover effect: Elevação sutil + escala 1.02

**Elementos do Card:**
```
┌─────────────────────────────────┐
│  🍀 RASPA DA SORTE             │
│                                 │
│     [Área de Raspagem]         │
│        ? ? ? ? ?               │
│        ? ? ? ? ?               │
│        ? ? ? ? ?               │
│                                 │
│  Prêmio: Até R$ 5.000          │
│  [JOGAR - R$ 10,00]            │
└─────────────────────────────────┘
```

**Estados do Card:**
- **Disponível**: Cores vibrantes, botão ativo
- **Jogando**: Animação de loading, botão desabilitado
- **Concluído**: Resultado visível, opção de jogar novamente

### 3.2 Interface de Raspagem

**Área de Jogo:**
```
┌─────────────────────────────────────────┐
│              RASPA DA SORTE             │
├─────────────────────────────────────────┤
│  Encontre 3 símbolos iguais para ganhar │
├─────────────────────────────────────────┤
│                                         │
│    [🍀] [💎] [🍀]  ← Área Raspável     │
│    [💰] [🍀] [⭐]                      │
│    [🎯] [💎] [🍀]                      │
│                                         │
├─────────────────────────────────────────┤
│  Progresso: ████████░░ 80%             │
│                                         │
│  [REVELAR TUDO] [JOGAR NOVAMENTE]       │
└─────────────────────────────────────────┘
```

**Mecânica de Raspagem:**
- Cursor personalizado (moeda ou dedo)
- Efeito de "raspagem" com partículas
- Som de raspagem realístico
- Vibração no mobile (se suportado)
- Animação de revelação progressiva

### 3.3 Feed de Ganhadores

**Design do Feed:**
```
┌─────────────────────────────┐
│      🏆 GANHADORES AO VIVO  │
├─────────────────────────────┤
│ 🎉 João S*** ganhou R$ 500  │
│    há 2 minutos             │
├─────────────────────────────┤
│ 💰 Maria L*** ganhou R$ 150 │
│    há 5 minutos             │
├─────────────────────────────┤
│ 🔥 Pedro M*** ganhou R$ 2.5K│
│    há 8 minutos             │
├─────────────────────────────┤
│ ⚡ Ana C*** ganhou R$ 75    │
│    há 12 minutos            │
└─────────────────────────────┘
```

**Animações:**
- Entrada suave de novos ganhadores (slide down)
- Highlight temporário para prêmios grandes
- Auto-scroll com pausa no hover
- Efeitos de confete para prêmios acima de R$ 1.000

### 3.4 Carteira Digital

**Interface da Carteira:**
```
┌─────────────────────────────────────────┐
│              💰 MINHA CARTEIRA          │
├─────────────────────────────────────────┤
│  Saldo Principal: R$ 150,00             │
│  Saldo Bônus: R$ 25,00                  │
│  Total Disponível: R$ 175,00            │
├─────────────────────────────────────────┤
│  [DEPOSITAR]  [SACAR]  [HISTÓRICO]      │
├─────────────────────────────────────────┤
│  Últimas Transações:                    │
│  ↗️ Depósito PIX    +R$ 100,00  Hoje    │
│  🎮 Jogo Raspadinha -R$ 10,00   Hoje    │
│  🏆 Prêmio Ganho    +R$ 50,00   Ontem   │
│  ↗️ Depósito PIX    +R$ 50,00   Ontem   │
└─────────────────────────────────────────┘
```

### 3.5 Modal de Depósito PIX

**Interface PIX:**
```
┌─────────────────────────────────────────┐
│           💳 DEPÓSITO VIA PIX           │
├─────────────────────────────────────────┤
│  Valor: R$ [____100,00____]             │
│                                         │
│  Bônus: +R$ 10,00 (10% extra)          │
│  Total a receber: R$ 110,00             │
├─────────────────────────────────────────┤
│           [QR CODE AQUI]                │
│                                         │
│  Chave PIX: 12345678901234567890        │
│  [COPIAR CHAVE]                         │
├─────────────────────────────────────────┤
│  ⏱️ Aguardando pagamento...             │
│  Tempo limite: 14:58                    │
│                                         │
│  [CANCELAR]    [JÁ PAGUEI]              │
└─────────────────────────────────────────┘
```

## 4. FLUXOS DE USUÁRIO

### 4.1 Fluxo de Primeiro Acesso

**Etapa 1: Landing Page**
- Hero banner com proposta de valor clara
- Demonstração visual de como funciona
- Depoimentos de ganhadores
- CTA principal: "COMEÇAR A JOGAR"

**Etapa 2: Registro**
```
┌─────────────────────────────────────────┐
│            🎮 CRIAR CONTA               │
├─────────────────────────────────────────┤
│  Nome Completo: [________________]      │
│  E-mail: [_______________________]      │
│  CPF: [___.___.___-__]                  │
│  Data Nascimento: [__/__/____]          │
│  Celular: [(__) _____-____]             │
│  Senha: [_______________________]       │
│  Confirmar Senha: [______________]      │
├─────────────────────────────────────────┤
│  ☑️ Li e aceito os Termos de Uso        │
│  ☑️ Sou maior de 18 anos                │
│  ☐ Quero receber promoções por email    │
├─────────────────────────────────────────┤
│           [CRIAR CONTA]                 │
│                                         │
│  Já tem conta? [Fazer Login]            │
└─────────────────────────────────────────┘
```

**Etapa 3: Verificação de Email**
- Tela de confirmação com instruções
- Reenvio de email se necessário
- Redirecionamento automático após verificação

**Etapa 4: Onboarding**
- Tour guiado pela interface (3-4 passos)
- Explicação dos tipos de raspadinha
- Demonstração do sistema de bônus
- Primeira raspadinha grátis de boas-vindas

### 4.2 Fluxo de Jogo

**Etapa 1: Seleção de Categoria**
- Grid visual com todas as categorias
- Filtros por preço e prêmio máximo
- Preview das regras de cada categoria

**Etapa 2: Confirmação de Compra**
```
┌─────────────────────────────────────────┐
│         🎮 CONFIRMAR COMPRA             │
├─────────────────────────────────────────┤
│  Raspadinha: Raspa da Sorte             │
│  Preço: R$ 10,00                        │
│  Prêmio Máximo: R$ 5.000                │
│                                         │
│  Saldo Atual: R$ 150,00                 │
│  Saldo Após: R$ 140,00                  │
├─────────────────────────────────────────┤
│  [CANCELAR]      [CONFIRMAR]            │
└─────────────────────────────────────────┘
```

**Etapa 3: Jogo**
- Interface de raspagem interativa
- Barra de progresso
- Opção de revelação automática
- Efeitos sonoros e visuais

**Etapa 4: Resultado**
```
┌─────────────────────────────────────────┐
│              🎉 PARABÉNS!               │
├─────────────────────────────────────────┤
│         VOCÊ GANHOU R$ 50,00!           │
│                                         │
│    [Símbolos Vencedores Destacados]     │
│                                         │
│  Seu saldo foi atualizado para:         │
│            R$ 190,00                    │
├─────────────────────────────────────────┤
│  [JOGAR NOVAMENTE] [VER CARTEIRA]       │
│                                         │
│  [COMPARTILHAR VITÓRIA] 📱              │
└─────────────────────────────────────────┘
```

### 4.3 Fluxo de Saque

**Etapa 1: Solicitação**
```
┌─────────────────────────────────────────┐
│            💸 SOLICITAR SAQUE           │
├─────────────────────────────────────────┤
│  Saldo Disponível: R$ 350,00            │
│  Valor Mínimo: R$ 20,00                 │
│                                         │
│  Valor do Saque: R$ [_______]           │
│  Taxa: R$ 0,00 (Grátis via PIX)         │
│  Você Receberá: R$ [_______]            │
├─────────────────────────────────────────┤
│  Chave PIX: [_____________________]     │
│  Tipo: ( ) CPF ( ) Email ( ) Celular    │
├─────────────────────────────────────────┤
│  [CANCELAR]      [SOLICITAR]            │
└─────────────────────────────────────────┘
```

**Etapa 2: Confirmação**
- Resumo da solicitação
- Tempo estimado para processamento
- Número de protocolo para acompanhamento

**Etapa 3: Processamento**
- Status em tempo real
- Notificações por email/SMS
- Histórico de saques na carteira

## 5. RESPONSIVIDADE E MOBILE

### 5.1 Breakpoints

**Desktop**: 1200px+
- Layout completo com sidebar
- Grid de 4 colunas para categorias
- Feed lateral de ganhadores

**Tablet**: 768px - 1199px
- Menu colapsável
- Grid de 3 colunas
- Feed integrado ao conteúdo principal

**Mobile**: 320px - 767px
- Menu hambúrguer
- Grid de 1-2 colunas
- Interface otimizada para touch

### 5.2 Adaptações Mobile

**Header Mobile:**
```
┌─────────────────────────────────┐
│ ☰  RASPADINHA ONLINE    R$ 150  │
└─────────────────────────────────┘
```

**Navegação Mobile:**
- Bottom navigation bar
- Ícones grandes para fácil toque
- Swipe gestures para navegação

**Raspadinha Mobile:**
- Área de toque otimizada
- Feedback tátil (vibração)
- Orientação portrait/landscape
- Zoom automático na área de jogo

### 5.3 Progressive Web App (PWA)

**Características:**
- Instalável na tela inicial
- Funcionamento offline limitado
- Push notifications
- Splash screen personalizada
- Ícones adaptativos

**Manifest.json:**
```json
{
  "name": "Raspadinha Online",
  "short_name": "Raspadinha",
  "description": "Jogue raspadinha online e ganhe prêmios incríveis!",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#2ECC71",
  "theme_color": "#27AE60",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## 6. ANIMAÇÕES E MICROINTERAÇÕES

### 6.1 Animações de Entrada

**Page Transitions:**
- Fade in suave (300ms)
- Slide up para modais (250ms)
- Scale in para cards (200ms)

**Loading States:**
- Skeleton screens para conteúdo
- Spinner personalizado com logo
- Progress bars para uploads/downloads

### 6.2 Feedback Visual

**Hover Effects:**
- Elevação sutil em cards
- Mudança de cor em botões
- Escala ligeira em elementos clicáveis

**Click Feedback:**
- Ripple effect em botões
- Bounce em ícones importantes
- Color flash para confirmações

### 6.3 Animações de Jogo

**Raspagem:**
- Partículas que "caem" durante raspagem
- Revelação progressiva com easing
- Shake animation para quase-acertos

**Vitória:**
- Confete animado
- Pulse effect no valor do prêmio
- Celebração com fogos de artifício

**CSS Animations:**
```css
@keyframes scratch-reveal {
  0% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 0.5; transform: scale(1.1); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes prize-celebration {
  0% { transform: scale(1); }
  25% { transform: scale(1.2) rotate(-5deg); }
  50% { transform: scale(1.1) rotate(5deg); }
  75% { transform: scale(1.15) rotate(-2deg); }
  100% { transform: scale(1) rotate(0deg); }
}

.scratch-symbol {
  animation: scratch-reveal 0.5s ease-out;
}

.prize-amount {
  animation: prize-celebration 1s ease-in-out;
}
```

## 7. ACESSIBILIDADE

### 7.1 Padrões WCAG 2.1

**Nível AA Compliance:**
- Contraste mínimo de 4.5:1 para texto normal
- Contraste mínimo de 3:1 para texto grande
- Navegação por teclado completa
- Screen reader compatibility

**Implementações:**
```html
<!-- Botões com labels descritivos -->
<button aria-label="Jogar raspadinha da sorte por R$ 10,00">
  JOGAR - R$ 10,00
</button>

<!-- Landmarks para navegação -->
<main role="main" aria-label="Área principal de jogos">
<nav role="navigation" aria-label="Menu principal">
<aside role="complementary" aria-label="Feed de ganhadores">

<!-- Estados de loading -->
<div aria-live="polite" aria-busy="true">
  Carregando jogo...
</div>
```

### 7.2 Suporte a Tecnologias Assistivas

**Screen Readers:**
- Descrições detalhadas de imagens
- Anúncios de mudanças de estado
- Navegação por headings estruturada

**Navegação por Teclado:**
- Tab order lógico
- Focus indicators visíveis
- Atalhos de teclado para ações principais

**Alto Contraste:**
- Modo de alto contraste opcional
- Indicadores visuais alternativos
- Redução de animações para sensibilidade

### 7.3 Configurações de Acessibilidade

**Painel de Configurações:**
```
┌─────────────────────────────────────────┐
│         ⚙️ ACESSIBILIDADE               │
├─────────────────────────────────────────┤
│  ☐ Modo Alto Contraste                  │
│  ☐ Reduzir Animações                    │
│  ☐ Aumentar Tamanho da Fonte            │
│  ☐ Desabilitar Sons                     │
│  ☐ Modo Simplificado                    │
├─────────────────────────────────────────┤
│  Tamanho da Fonte:                      │
│  ○ Pequeno  ●Médio  ○ Grande            │
│                                         │
│  Velocidade de Animação:                │
│  ○ Lenta  ● Normal  ○ Rápida            │
├─────────────────────────────────────────┤
│           [SALVAR CONFIGURAÇÕES]        │
└─────────────────────────────────────────┘
```

Este design de interface garante uma experiência de usuário excepcional, combinando elementos visuais atraentes com funcionalidade robusta e acessibilidade universal, criando uma plataforma que será tanto envolvente quanto inclusiva para todos os usuários.

