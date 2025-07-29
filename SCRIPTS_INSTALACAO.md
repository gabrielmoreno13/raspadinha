# 🛠️ SCRIPTS DE INSTALAÇÃO AUTOMATIZADA

## 📋 **SCRIPT 1: INSTALAÇÃO INICIAL DO SERVIDOR**

### **Copie e cole este script no console do droplet:**

```bash
#!/bin/bash
echo "🚀 Iniciando instalação do sistema Raspadinha Com Sorte..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
apt update && apt upgrade -y

# Instalar Node.js 20
echo "📦 Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt-get install -y nodejs

# Instalar Python e dependências
echo "🐍 Instalando Python..."
apt install -y python3 python3-pip python3-venv

# Instalar Nginx
echo "🌐 Instalando Nginx..."
apt install -y nginx

# Instalar PM2
echo "⚙️ Instalando PM2..."
npm install -g pm2

# Instalar outras dependências
echo "📦 Instalando dependências extras..."
apt install -y git curl wget unzip

# Configurar firewall
echo "🔒 Configurando firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw allow 80
ufw allow 443
ufw --force enable

# Criar estrutura de diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p /var/www/raspadinha
mkdir -p /var/log/raspadinha
mkdir -p /var/log/pm2

# Configurar permissões
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html

echo "✅ Instalação inicial concluída!"
echo "📋 Próximo passo: fazer upload dos arquivos do sistema"
```

---

## 📋 **SCRIPT 2: CONFIGURAÇÃO DO BACKEND**

### **Execute após fazer upload dos arquivos:**

```bash
#!/bin/bash
echo "🔧 Configurando backend Flask..."

# Ir para diretório do backend
cd /var/www/raspadinha/raspadinha-backend

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install flask flask-cors flask-jwt-extended bcrypt marshmallow python-dotenv

# Copiar arquivo de configuração
echo "⚙️ Configurando ambiente..."
cp /var/www/raspadinha/.env.production .env

# Testar backend
echo "🧪 Testando backend..."
python src/main.py &
BACKEND_PID=$!
sleep 5
kill $BACKEND_PID

echo "✅ Backend configurado com sucesso!"
```

---

## 📋 **SCRIPT 3: BUILD E DEPLOY DO FRONTEND**

### **Execute para fazer build dos sites:**

```bash
#!/bin/bash
echo "🎨 Fazendo build do frontend..."

# Build do site principal
echo "🏠 Build do site principal..."
cd /var/www/raspadinha/raspadinha-sorte-clone
npm install
npm run build
cp -r dist/* /var/www/html/

# Build do site de afiliados
echo "🔗 Build do site de afiliados..."
cd /var/www/raspadinha/afiliados-raspadinha
npm install
npm run build
mkdir -p /var/www/html/afiliados
cp -r dist/* /var/www/html/afiliados/

# Configurar permissões
echo "🔒 Configurando permissões..."
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html

echo "✅ Frontend deployado com sucesso!"
```

---

## 📋 **SCRIPT 4: CONFIGURAÇÃO NGINX E PM2**

### **Execute para configurar servidor web:**

```bash
#!/bin/bash
echo "🌐 Configurando Nginx e PM2..."

# Configurar Nginx
echo "⚙️ Configurando Nginx..."
cp /var/www/raspadinha/nginx-raspadinha.conf /etc/nginx/sites-available/raspadinha
ln -sf /etc/nginx/sites-available/raspadinha /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testar configuração Nginx
nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Configuração Nginx válida"
    systemctl reload nginx
else
    echo "❌ Erro na configuração Nginx"
    exit 1
fi

# Configurar PM2
echo "⚙️ Configurando PM2..."
cd /var/www/raspadinha
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo "✅ Nginx e PM2 configurados!"
```

---

## 📋 **SCRIPT 5: INSTALAÇÃO SSL (HTTPS)**

### **Execute após configurar DNS:**

```bash
#!/bin/bash
echo "🔒 Configurando SSL/HTTPS..."

# Instalar Certbot
echo "📦 Instalando Certbot..."
apt install -y certbot python3-certbot-nginx

# Aguardar DNS propagar
echo "⏳ Aguardando DNS propagar..."
echo "Certifique-se que raspadinhacomsorte.com está apontando para este servidor"
read -p "Pressione Enter quando o DNS estiver funcionando..."

# Obter certificado SSL
echo "🔐 Obtendo certificado SSL..."
certbot --nginx -d raspadinhacomsorte.com -d www.raspadinhacomsorte.com --non-interactive --agree-tos --email seu_email@gmail.com

# Configurar renovação automática
echo "🔄 Configurando renovação automática..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

echo "✅ SSL configurado com sucesso!"
echo "🌐 Seu site agora está disponível em: https://raspadinhacomsorte.com"
```

---

## 📋 **SCRIPT 6: VERIFICAÇÃO COMPLETA**

### **Execute para verificar se tudo está funcionando:**

```bash
#!/bin/bash
echo "🔍 Verificando instalação completa..."

# Verificar serviços
echo "📊 Status dos serviços:"
echo "Nginx:"
systemctl is-active nginx
echo "PM2:"
pm2 status

# Verificar portas
echo "🔌 Portas em uso:"
netstat -tlnp | grep -E ':80|:443|:5000'

# Testar URLs localmente
echo "🧪 Testando URLs:"
echo "Site principal:"
curl -I http://localhost/ | head -1
echo "API:"
curl -I http://localhost/api/health | head -1

# Verificar logs
echo "📋 Últimas linhas dos logs:"
echo "Nginx:"
tail -3 /var/log/nginx/raspadinha_access.log
echo "Backend:"
pm2 logs raspadinha-backend --lines 3

# Verificar espaço em disco
echo "💾 Espaço em disco:"
df -h /

echo "✅ Verificação concluída!"
echo "🌐 Acesse: https://raspadinhacomsorte.com"
```

---

## 🚀 **ORDEM DE EXECUÇÃO**

### **Execute os scripts nesta ordem:**

1. **SCRIPT 1** - Instalação inicial (primeiro)
2. **Upload dos arquivos** (manual)
3. **SCRIPT 2** - Configuração backend
4. **SCRIPT 3** - Build frontend
5. **SCRIPT 4** - Nginx e PM2
6. **Configurar DNS** (manual)
7. **SCRIPT 5** - SSL/HTTPS
8. **SCRIPT 6** - Verificação final

---

## 💡 **DICAS IMPORTANTES**

### **Como executar os scripts:**
1. Copie o código do script
2. Cole no console do droplet
3. Pressione Enter
4. Aguarde terminar antes do próximo

### **Se algo der errado:**
- Leia as mensagens de erro
- Execute o script de verificação
- Consulte os logs: `pm2 logs` e `/var/log/nginx/error.log`

### **Comandos úteis:**
```bash
# Ver status geral
pm2 status && systemctl status nginx

# Reiniciar tudo
pm2 restart all && systemctl restart nginx

# Ver logs em tempo real
pm2 logs raspadinha-backend --lines 50
```

**🎉 Com estes scripts, sua instalação será muito mais rápida e confiável!**

