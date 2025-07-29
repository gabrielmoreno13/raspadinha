# 🚀 GUIA COMPLETO DE DEPLOY - RASPADINHA COM SORTE
## Digital Ocean + Cloudflare + GoDaddy

### 📋 **PRÉ-REQUISITOS**
- ✅ Droplet no Digital Ocean (Ubuntu 22.04)
- ✅ Domínio raspadinhacomsorte.com no GoDaddy
- ✅ Conta no Cloudflare
- ✅ Console do Droplet aberto

---

## 🖥️ **PARTE 1: CONFIGURAÇÃO INICIAL DO SERVIDOR**

### **1.1 Acessar o Console do Droplet**
1. Entre no painel do Digital Ocean
2. Vá em "Droplets"
3. Clique no seu droplet
4. Clique em "Console" (ícone de terminal)
5. Faça login como root

### **1.2 Atualizar o Sistema**
```bash
apt update && apt upgrade -y
```

### **1.3 Instalar Dependências**
```bash
# Instalar Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt-get install -y nodejs

# Instalar Python e pip
apt install -y python3 python3-pip python3-venv

# Instalar Nginx
apt install -y nginx

# Instalar PM2 (gerenciador de processos)
npm install -g pm2

# Instalar Git
apt install -y git
```

### **1.4 Configurar Firewall**
```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw allow 80
ufw allow 443
ufw enable
```

---

## 📁 **PARTE 2: UPLOAD DOS ARQUIVOS**

### **2.1 Criar Estrutura de Diretórios**
```bash
mkdir -p /var/www/raspadinha
cd /var/www/raspadinha
```

### **2.2 Upload dos Arquivos**
**Opção A: Via SCP (se tiver SSH configurado)**
```bash
# No seu computador local:
scp -r raspadinha-completo/* root@SEU_IP_DROPLET:/var/www/raspadinha/
```

**Opção B: Via Git (recomendado)**
```bash
# No console do droplet:
cd /var/www/raspadinha
# Você precisará criar um repositório Git ou usar outro método de transferência
```

**Opção C: Via Console (arquivo por arquivo)**
- Use o editor nano para criar cada arquivo manualmente
- Copie e cole o conteúdo de cada arquivo

---

## 🔧 **PARTE 3: CONFIGURAÇÃO DO BACKEND**

### **3.1 Configurar Backend Flask**
```bash
cd /var/www/raspadinha/raspadinha-backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install flask flask-cors flask-jwt-extended bcrypt marshmallow python-dotenv

# Criar arquivo de configuração
nano .env
```

**Conteúdo do .env:**
```env
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_super_forte_aqui
DATABASE_URL=sqlite:///raspadinha.db
```

### **3.2 Testar Backend**
```bash
cd /var/www/raspadinha/raspadinha-backend
source venv/bin/activate
python src/main.py
```

### **3.3 Configurar PM2 para Backend**
```bash
# Criar arquivo de configuração PM2
nano /var/www/raspadinha/ecosystem.config.js
```

**Conteúdo do ecosystem.config.js:**
```javascript
module.exports = {
  apps: [{
    name: 'raspadinha-backend',
    script: '/var/www/raspadinha/raspadinha-backend/venv/bin/python',
    args: '/var/www/raspadinha/raspadinha-backend/src/main.py',
    cwd: '/var/www/raspadinha/raspadinha-backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 5000
    }
  }]
};
```

```bash
# Iniciar backend com PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## 🌐 **PARTE 4: CONFIGURAÇÃO DO FRONTEND**

### **4.1 Build do Site Principal**
```bash
cd /var/www/raspadinha/raspadinha-sorte-clone

# Instalar dependências
npm install

# Fazer build para produção
npm run build

# Copiar arquivos para Nginx
cp -r dist/* /var/www/html/
```

### **4.2 Build do Site de Afiliados**
```bash
cd /var/www/raspadinha/afiliados-raspadinha

# Instalar dependências
npm install

# Fazer build para produção
npm run build

# Criar diretório para afiliados
mkdir -p /var/www/html/afiliados
cp -r dist/* /var/www/html/afiliados/
```

---

## ⚙️ **PARTE 5: CONFIGURAÇÃO DO NGINX**

### **5.1 Configurar Site Principal**
```bash
nano /etc/nginx/sites-available/raspadinha
```

**Conteúdo do arquivo:**
```nginx
server {
    listen 80;
    server_name raspadinhacomsorte.com www.raspadinhacomsorte.com;
    root /var/www/html;
    index index.html;

    # Site principal
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Site de afiliados
    location /afiliados {
        alias /var/www/html/afiliados;
        try_files $uri $uri/ /afiliados/index.html;
    }

    # API Backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Configurações de cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### **5.2 Ativar Site**
```bash
ln -s /etc/nginx/sites-available/raspadinha /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

---

## 🔒 **PARTE 6: CONFIGURAÇÃO SSL (HTTPS)**

### **6.1 Instalar Certbot**
```bash
apt install -y certbot python3-certbot-nginx
```

### **6.2 Obter Certificado SSL**
```bash
certbot --nginx -d raspadinhacomsorte.com -d www.raspadinhacomsorte.com
```

### **6.3 Configurar Renovação Automática**
```bash
crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🌍 **PARTE 7: CONFIGURAÇÃO DNS**

### **7.1 Cloudflare**
1. Adicione o domínio raspadinhacomsorte.com no Cloudflare
2. Configure os nameservers no GoDaddy para apontar para Cloudflare
3. No Cloudflare, adicione os registros DNS:
   - **A Record**: @ → IP_DO_SEU_DROPLET
   - **A Record**: www → IP_DO_SEU_DROPLET
   - **CNAME**: afiliados → raspadinhacomsorte.com

### **7.2 GoDaddy**
1. Vá em "Gerenciar DNS"
2. Altere os nameservers para os fornecidos pelo Cloudflare
3. Aguarde propagação (até 24h)

---

## ✅ **PARTE 8: VERIFICAÇÃO E TESTES**

### **8.1 Verificar Serviços**
```bash
# Verificar Nginx
systemctl status nginx

# Verificar PM2
pm2 status

# Verificar logs
pm2 logs raspadinha-backend
```

### **8.2 Testar URLs**
- **Site Principal**: https://raspadinhacomsorte.com
- **Site Afiliados**: https://raspadinhacomsorte.com/afiliados
- **API**: https://raspadinhacomsorte.com/api/health

---

## 🔧 **COMANDOS ÚTEIS DE MANUTENÇÃO**

```bash
# Reiniciar backend
pm2 restart raspadinha-backend

# Ver logs em tempo real
pm2 logs raspadinha-backend --lines 100

# Reiniciar Nginx
systemctl restart nginx

# Verificar uso de recursos
htop

# Backup do banco de dados
cp /var/www/raspadinha/raspadinha-backend/raspadinha.db /backup/
```

---

## 🆘 **TROUBLESHOOTING**

### **Problema: Site não carrega**
```bash
# Verificar Nginx
nginx -t
systemctl status nginx

# Verificar logs
tail -f /var/log/nginx/error.log
```

### **Problema: API não responde**
```bash
# Verificar PM2
pm2 status
pm2 logs raspadinha-backend

# Reiniciar backend
pm2 restart raspadinha-backend
```

### **Problema: SSL não funciona**
```bash
# Renovar certificado
certbot renew
systemctl reload nginx
```

---

## 📞 **SUPORTE**

Se encontrar problemas:
1. Verifique os logs: `pm2 logs` e `/var/log/nginx/error.log`
2. Teste cada componente individualmente
3. Verifique se todas as portas estão abertas no firewall
4. Confirme se o DNS está propagado

**🎉 Parabéns! Seu sistema de raspadinha está online!**

