# 🌐 CONFIGURAÇÃO DNS - CLOUDFLARE + GODADDY

## 🎯 **OBJETIVO**
Configurar o domínio **raspadinhacomsorte.com** para apontar para seu servidor Digital Ocean usando Cloudflare como proxy.

---

## 📋 **PARTE 1: PREPARAÇÃO**

### **Informações que você precisa ter em mãos:**
1. ✅ IP do seu Droplet Digital Ocean (ex: 123.456.789.10)
2. ✅ Acesso ao painel GoDaddy
3. ✅ Acesso ao painel Cloudflare
4. ✅ Domínio: raspadinhacomsorte.com

### **Como encontrar o IP do Droplet:**
1. Entre no Digital Ocean
2. Vá em "Droplets"
3. O IP aparece na lista (ex: 123.456.789.10)
4. **ANOTE ESTE IP** - você vai precisar dele!

---

## 🔧 **PARTE 2: CONFIGURAR CLOUDFLARE**

### **PASSO 1: Adicionar Domínio no Cloudflare**
1. Entre em: https://dash.cloudflare.com
2. Clique em **"Add a Site"** (Adicionar Site)
3. Digite: **raspadinhacomsorte.com**
4. Clique em **"Add Site"**
5. Escolha o plano **"Free"** (gratuito)
6. Clique em **"Continue"**

### **PASSO 2: Configurar Registros DNS**
Agora você vai adicionar os registros DNS. Na tela do Cloudflare:

1. **Registro A para domínio principal:**
   - **Type**: A
   - **Name**: @ (ou deixe vazio)
   - **IPv4 address**: SEU_IP_DO_DROPLET
   - **Proxy status**: 🟠 Proxied (nuvem laranja)
   - Clique **"Save"**

2. **Registro A para www:**
   - **Type**: A
   - **Name**: www
   - **IPv4 address**: SEU_IP_DO_DROPLET
   - **Proxy status**: 🟠 Proxied (nuvem laranja)
   - Clique **"Save"**

3. **Registro CNAME para afiliados:**
   - **Type**: CNAME
   - **Name**: afiliados
   - **Target**: raspadinhacomsorte.com
   - **Proxy status**: 🟠 Proxied (nuvem laranja)
   - Clique **"Save"**

### **PASSO 3: Anotar Nameservers**
1. Após adicionar os registros, o Cloudflare vai mostrar os **nameservers**
2. Eles serão algo como:
   ```
   alice.ns.cloudflare.com
   bob.ns.cloudflare.com
   ```
3. **ANOTE ESTES NAMESERVERS** - você vai precisar no GoDaddy!

---

## 🏠 **PARTE 3: CONFIGURAR GODADDY**

### **PASSO 1: Acessar Painel GoDaddy**
1. Entre em: https://account.godaddy.com
2. Faça login com sua conta
3. Vá em **"My Products"** (Meus Produtos)
4. Encontre **raspadinhacomsorte.com**
5. Clique em **"DNS"** ou **"Manage DNS"**

### **PASSO 2: Alterar Nameservers**
1. Procure por **"Nameservers"** ou **"Name Servers"**
2. Clique em **"Change"** ou **"Alterar"**
3. Selecione **"Custom"** ou **"Personalizado"**
4. Apague os nameservers atuais
5. Adicione os nameservers do Cloudflare:
   ```
   alice.ns.cloudflare.com
   bob.ns.cloudflare.com
   ```
   (Use os que o Cloudflare te deu!)
6. Clique em **"Save"** ou **"Salvar"**

### **PASSO 3: Aguardar Propagação**
- A mudança pode demorar de **2 a 24 horas** para funcionar
- Você pode testar digitando seu domínio no navegador
- Inicialmente pode não funcionar, é normal!

---

## ⚙️ **PARTE 4: CONFIGURAÇÕES EXTRAS CLOUDFLARE**

### **SSL/TLS (HTTPS)**
1. No painel Cloudflare, vá em **"SSL/TLS"**
2. Selecione **"Full (strict)"**
3. Isso garante que seu site tenha HTTPS

### **Security (Segurança)**
1. Vá em **"Security"** → **"Settings"**
2. **Security Level**: Medium
3. **Bot Fight Mode**: On
4. Isso protege contra ataques

### **Speed (Velocidade)**
1. Vá em **"Speed"** → **"Optimization"**
2. **Auto Minify**: Marque CSS, HTML, JavaScript
3. **Brotli**: On
4. Isso deixa o site mais rápido

---

## 🧪 **PARTE 5: TESTAR CONFIGURAÇÃO**

### **Verificar se DNS está funcionando:**
1. Abra o site: https://dnschecker.org
2. Digite: **raspadinhacomsorte.com**
3. Clique em **"Search"**
4. Deve mostrar o IP do seu droplet em vários locais

### **Testar no navegador:**
1. Digite: **http://raspadinhacomsorte.com**
2. Digite: **http://www.raspadinhacomsorte.com**
3. Se aparecer a página do Nginx ou seu site, funcionou!

### **Se não funcionar ainda:**
- Aguarde mais tempo (pode demorar até 24h)
- Verifique se os nameservers estão corretos
- Confirme se o IP do droplet está certo

---

## 🔍 **VERIFICAR CONFIGURAÇÃO FINAL**

### **No Cloudflare, você deve ter:**
```
Type    Name        Content                 Status
A       @           SEU_IP_DROPLET         🟠 Proxied
A       www         SEU_IP_DROPLET         🟠 Proxied
CNAME   afiliados   raspadinhacomsorte.com 🟠 Proxied
```

### **No GoDaddy, você deve ter:**
```
Nameservers:
alice.ns.cloudflare.com
bob.ns.cloudflare.com
```

---

## 🆘 **PROBLEMAS COMUNS**

### **"Site não carrega"**
- Aguarde mais tempo (até 24h)
- Verifique se o servidor está funcionando
- Confirme se o IP está correto

### **"Erro de SSL"**
- No Cloudflare, vá em SSL/TLS
- Mude para "Full (strict)"
- Aguarde alguns minutos

### **"DNS não propaga"**
- Verifique se os nameservers estão corretos no GoDaddy
- Aguarde mais tempo
- Tente limpar cache do navegador (Ctrl+F5)

### **"Subdomínio afiliados não funciona"**
- Verifique se criou o CNAME no Cloudflare
- Confirme se está apontando para raspadinhacomsorte.com
- Aguarde propagação

---

## 📞 **COMANDOS ÚTEIS PARA TESTAR**

### **No console do droplet:**
```bash
# Verificar se Nginx está rodando
systemctl status nginx

# Testar se o site responde localmente
curl localhost

# Ver logs do Nginx
tail -f /var/log/nginx/access.log
```

### **No seu computador:**
```bash
# Verificar DNS (Windows)
nslookup raspadinhacomsorte.com

# Verificar DNS (Mac/Linux)
dig raspadinhacomsorte.com
```

---

## 🎯 **RESULTADO FINAL**

Quando tudo estiver funcionando, você terá:

- ✅ **raspadinhacomsorte.com** → Site principal
- ✅ **www.raspadinhacomsorte.com** → Site principal
- ✅ **afiliados.raspadinhacomsorte.com** → Landing page afiliados
- ✅ **HTTPS** funcionando automaticamente
- ✅ **Proteção** do Cloudflare ativa
- ✅ **Velocidade** otimizada

**🎉 Seu domínio estará configurado e funcionando perfeitamente!**

