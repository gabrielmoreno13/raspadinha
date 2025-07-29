# 🖥️ GUIA PASSO A PASSO - CONSOLE DIGITAL OCEAN

## 🎯 **COMO ACESSAR O CONSOLE DO SEU DROPLET**

### **PASSO 1: Entrar no Digital Ocean**
1. Abra seu navegador
2. Vá para: https://cloud.digitalocean.com
3. Faça login com seu email e senha
4. Você verá o painel principal do Digital Ocean

### **PASSO 2: Encontrar Seu Droplet**
1. No menu lateral esquerdo, clique em **"Droplets"**
2. Você verá uma lista dos seus servidores
3. Encontre o droplet que você quer usar
4. Clique no **nome do droplet** (não nos botões, no nome mesmo)

### **PASSO 3: Abrir o Console**
1. Você estará na página de detalhes do droplet
2. No topo da página, procure as abas/botões
3. Clique em **"Console"** (ícone de terminal/tela preta)
4. Uma nova janela ou aba vai abrir com uma tela preta

### **PASSO 4: Fazer Login no Console**
1. Na tela preta, você verá algo como:
   ```
   Ubuntu 22.04.3 LTS droplet-name tty1
   droplet-name login:
   ```
2. Digite: **root** (e pressione Enter)
3. Digite sua senha (não aparecerá nada na tela, é normal)
4. Pressione Enter

### **PASSO 5: Confirmar que Está Logado**
Quando der certo, você verá algo assim:
```
root@droplet-name:~#
```

**🎉 Pronto! Agora você está no console do seu servidor!**

---

## 📋 **COMANDOS BÁSICOS PARA COMEÇAR**

### **Verificar se está tudo funcionando:**
```bash
# Ver onde você está
pwd

# Ver arquivos na pasta atual
ls -la

# Ver informações do sistema
uname -a

# Ver espaço em disco
df -h
```

### **Se algo der errado:**
- **Console não abre**: Tente atualizar a página e clicar em Console novamente
- **Login não funciona**: Verifique se digitou "root" corretamente
- **Senha não aceita**: Tente digitar devagar, lembre que não aparece nada na tela
- **Tela fica preta**: Pressione Enter algumas vezes

---

## 🚀 **PRÓXIMOS PASSOS**

Agora que você está no console, pode seguir o **GUIA_DEPLOY_DIGITAL_OCEAN.md** para instalar o sistema completo!

### **Primeiro comando para executar:**
```bash
apt update && apt upgrade -y
```

**⚠️ IMPORTANTE:** 
- Copie e cole os comandos exatamente como estão no guia
- Aguarde cada comando terminar antes de executar o próximo
- Se aparecer perguntas, geralmente é só pressionar Enter ou digitar "y"

---

## 🆘 **PROBLEMAS COMUNS**

### **"Permission denied"**
- Certifique-se que está logado como "root"
- Se não estiver, digite: `sudo su -`

### **"Command not found"**
- Verifique se digitou o comando corretamente
- Execute primeiro: `apt update`

### **Console travou**
- Pressione Ctrl+C para cancelar comando atual
- Se não funcionar, feche e abra o console novamente

### **Perdeu a conexão**
- Feche a aba do console
- Volte para a página do droplet
- Clique em Console novamente

---

## 📞 **DICAS IMPORTANTES**

1. **Copiar e Colar**: Use Ctrl+C para copiar e Ctrl+V para colar
2. **Comandos Longos**: Execute um por vez, não todos juntos
3. **Aguardar**: Alguns comandos demoram, seja paciente
4. **Backup**: Anote o IP do seu droplet para referência
5. **Senhas**: Quando digitar senhas, não aparece nada na tela (é normal)

**🎯 Agora você está pronto para instalar o sistema de raspadinha!**

