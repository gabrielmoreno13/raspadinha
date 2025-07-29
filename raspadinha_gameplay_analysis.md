# Análise Detalhada do Gameplay - Raspadinha Sorte

## 🎮 **Mecânica do Jogo Observada**

### **Fluxo do Jogo:**
1. **Seleção da Raspadinha**: Usuário clica em "Jogar" em uma categoria
2. **Modal de Confirmação**: Mostra preço, prêmio máximo e tabela de prêmios
3. **Confirmação de Compra**: Botão verde "Jogar por R$ X,XX"
4. **Tela de Jogo**: Interface de raspadinha com 9 quadradinhos (3x3)
5. **Mecânica de Raspar**: "Raspe os 9 quadradinhos, encontre 3 símbolos iguais e ganhe um prêmio"
6. **Opção de Revelar**: Botão "REVELAR TUDO" para mostrar resultado instantaneamente

### **Interface do Jogo:**
- **Layout**: Grid 3x3 com 9 quadradinhos para raspar
- **Instrução**: "Raspe os 9 quadradinhos, encontre 3 símbolos iguais e ganhe um prêmio"
- **Saldo**: Mostrado no canto superior direito (R$ 9,00 após jogar R$ 1,00)
- **Botões**: "REVELAR TUDO" (azul) e "Fechar" (cinza)
- **Feedback Visual**: Animação de "RASPOU ACHOU GANHOU" com texto "ACHE 3 IGUAIS | GANHE NA HORA!"

### **Categorias Disponíveis:**
1. **Raspa da Esperança** - R$ 1,00 (Prêmios até R$ 1.000,00)
2. **Raspa da Alegria** - R$ 2,00 (Prêmios até R$ 5.000,00)
3. **Raspa da Emoção** - R$ 5,00 (Prêmios até R$ 10.000,00)
4. **Raspa do Bixo** - R$ 15,00 (Prêmios até R$ 50.000,00)

### **Sistema de Prêmios:**
- **Tabela de Prêmios**: Cada categoria mostra os prêmios possíveis com imagens
- **Prêmio Máximo**: Claramente destacado
- **Mecânica**: 3 símbolos iguais = prêmio correspondente

### **Interface do Usuário:**
- **Header**: Logo, navegação (Início, Raspadinhas, Prêmios), botões de ação (Depositar, Sacar)
- **Perfil**: Nome do usuário e saldo atual sempre visível
- **Feed AO VIVO**: Ganhadores recentes com nomes parcialmente ocultos
- **Design**: Fundo escuro, cores vibrantes (verde, amarelo), visual moderno

### **Funcionalidades Observadas:**
- **Sistema de Login**: Funcional e integrado
- **Saldo em Tempo Real**: Atualiza automaticamente após cada jogo
- **Modal de Confirmação**: Transparência nos custos e prêmios
- **Opção de Revelar**: Para jogadores impacientes
- **Feed de Ganhadores**: Cria senso de urgência e possibilidade

## 🎯 **Elementos Chave para Replicar:**

### **1. Interface de Jogo:**
- Grid 3x3 interativo
- Animação de raspar com mouse/toque
- Símbolos variados por categoria
- Feedback visual imediato

### **2. Sistema de Prêmios:**
- Tabela clara de prêmios por categoria
- Diferentes valores de entrada
- Prêmios escalonados

### **3. UX/UI:**
- Modal de confirmação antes do jogo
- Saldo sempre visível
- Botão "Revelar Tudo" para conveniência
- Design dark com cores vibrantes

### **4. Gamificação:**
- Feed de ganhadores em tempo real
- Animações de vitória
- Múltiplas categorias temáticas
- Progressão de valores

### **5. Sistema Financeiro:**
- Integração com saldo do usuário
- Débito automático ao jogar
- Crédito automático ao ganhar
- Transparência nos valores

## 📝 **Próximos Passos:**
1. Implementar grid 3x3 interativo
2. Criar sistema de símbolos por categoria
3. Desenvolver animações de raspar
4. Implementar lógica de 3 símbolos iguais
5. Criar tabelas de prêmios dinâmicas
6. Integrar com sistema financeiro
7. Adicionar feed de ganhadores em tempo real

