# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                        DEPLOYMENT GUIDE FOR PRODUCTION                     ║
# ║                    Hướng Dẫn Deploy Lên Web Công Khai                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝

## 📋 TABLE OF CONTENTS / MỤC LỤC
1. [Prerequisites / Yêu cầu](#prerequisites)
2. [Platform Options / Các Lựa Chọn Nền Tảng](#platform-options)
3. [Database Setup / Cấu Hình Database](#database-setup)
4. [Deploy on Railway / Deploy trên Railway](#railway)
5. [Deploy on Render / Deploy trên Render](#render)
6. [Deploy on Azure / Deploy trên Azure](#azure)
7. [Custom Domain & SSL / Tên Miền Tùy Chỉnh & SSL](#custom-domain)
8. [Post-Deployment / Sau Deployment](#post-deployment)

---

## <a name="prerequisites"></a>
## 1️⃣ PREREQUISITES / YÊU CẦU

### Cần chuẩn bị:
- [ ] GitHub account (để push code)
- [ ] Gemini API Key từ Google (https://makersuite.google.com/app/apikey)
- [ ] SQL Server Database (Azure SQL Database hoặc Cloud SQL)
- [ ] Credit card để thanh toán cloud services (nếu vượt free tier)
- [ ] Git installed on your computer

### Các Service Cần Dùng:
1. **Hosting Platform**: Railway, Render, hoặc Azure App Service
2. **Database**: Azure SQL Database hoặc AWS RDS SQL Server
3. **Domain** (optional): Namecheap, GoDaddy
4. **Email Service** (optional): SendGrid, Mailgun

---

## <a name="platform-options"></a>
## 2️⃣ PLATFORM OPTIONS / CÁC LỰA CHỌN NỀN TẢNG

### Recommended Solutions:

| Platform | Cost | Difficulty | Support | Best For |
|----------|------|-----------|---------|----------|
| **Railway** | ~$5-50/month | ⭐ Easy | Good | Quick deployment |
| **Render** | Free-$50/month | ⭐ Easy | Good | Free tier available |
| **Azure** | ~$10-100/month | ⭐⭐ Medium | Excellent | Enterprise-grade |
| **Heroku** | ~$7-50/month | ⭐ Easy | Good | Classic option (paid now) |
| **AWS** | ~$5-100/month | ⭐⭐⭐ Hard | Excellent | Scalable |

### 🚀 Recommended for beginners: **RAILWAY** or **RENDER**

---

## <a name="database-setup"></a>
## 3️⃣ DATABASE SETUP / CẤU HÌNH DATABASE

### Option A: Azure SQL Database (Recommended)

1. **Go to Azure Portal** (https://portal.azure.com)
   - Login or create Azure account
   - Search for "SQL Database"

2. **Create SQL Database:**
   - Resource Group: Create new "ChatBoxRG"
   - Database name: "ChatBoxDB"
   - Server: Create new
   - Admin login: "sqladmin"
   - Password: Use strong password (min 8 chars)

3. **Configure Firewall:**
   - Go to Server → Networking
   - Add your IP and Railway/Render IP (0.0.0.0/0 for now)

4. **Get Connection String:**
   - Server name: "your-server.database.windows.net"
   - Database: "ChatBoxDB"
   - User: "sqladmin"
   - Password: (your password)

### Option B: AWS RDS SQL Server

1. Go to AWS RDS → Create Database
2. Engine: SQL Server Express (free tier)
3. DB instance identifier: "chatbox-db"
4. Master username: "admin"
5. Password: (strong password)
6. Storage: 20 GB (free tier)

---

## <a name="railway"></a>
## 4️⃣ DEPLOY ON RAILWAY / DEPLOY TRÊN RAILWAY

### ✅ EASIEST OPTION FOR BEGINNERS

#### Step 1: Prepare GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ChatBox.git
git push -u origin main
```

#### Step 2: Create Railway Account

1. Go to https://railway.app
2. Click "Start Project"
3. Login with GitHub
4. Connect your GitHub account

#### Step 3: Create New Project on Railway

1. Click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Choose your ChatBox repository
4. Click "Deploy"

#### Step 4: Configure Environment Variables

1. In Railway dashboard, go to "Variables"
2. Add these environment variables:

```
FLASK_ENV=production
DEBUG=False
GEMINI_API_KEY=your-gemini-api-key
DB_SERVER=your-azure-server.database.windows.net
DB_NAME=ChatBoxDB
DB_USER=sqladmin
DB_PASSWORD=your-password
JWT_SECRET_KEY=generate-random-key-32-chars-minimum
SECRET_KEY=another-random-key
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=strong-admin-password
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

#### Step 5: Build & Deploy

Railway automatically builds and deploys when you push to GitHub

```bash
# After making changes locally
git add .
git commit -m "Your message"
git push origin main
# Railway will automatically deploy!
```

#### Step 6: Access Your App

Railway will give you a URL like: `https://chatbox-abc123.railway.app`

---

## <a name="render"></a>
## 5️⃣ DEPLOY ON RENDER / DEPLOY TRÊN RENDER

### Alternative (Similar to Railway)

#### Step 1: Create Account
- Go to https://render.com
- Sign up with GitHub

#### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect GitHub repo
3. Select "ChatBox" repository

#### Step 3: Configure
- Name: chatbox
- Environment: Python 3
- Build Command: `pip install -r backend/requirements-prod.txt`
- Start Command: `gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app`

#### Step 4: Add Environment Variables
Same as Railway (see above)

#### Step 5: Deploy
Click "Create Web Service" - Render will deploy automatically

---

## <a name="azure"></a>
## 6️⃣ DEPLOY ON AZURE / DEPLOY TRÊN AZURE

### Enterprise-Grade Solution

#### Step 1: Create App Service

```bash
# Install Azure CLI
# Download from https://aka.ms/installazurecliwindows

# Login to Azure
az login

# Create Resource Group
az group create --name ChatBoxRG --location eastasia

# Create App Service Plan
az appservice plan create \
  --name ChatBoxPlan \
  --resource-group ChatBoxRG \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group ChatBoxRG \
  --plan ChatBoxPlan \
  --name chatbox-app \
  --runtime "PYTHON:3.11"
```

#### Step 2: Deploy Code

```bash
# Initialize git for Azure
git init
git add .
git commit -m "Initial commit"

# Deploy to Azure
az webapp deployment source config-zip \
  --resource-group ChatBoxRG \
  --name chatbox-app \
  --src <path-to-zip-file>

# Or use GitHub Actions (recommended)
# Go to GitHub → Settings → Secrets and add AZURE_WEBAPP_PUBLISH_PROFILE
```

#### Step 3: Configure App Settings

```bash
az webapp config appsettings set \
  --resource-group ChatBoxRG \
  --name chatbox-app \
  --settings \
  FLASK_ENV=production \
  GEMINI_API_KEY="your-key" \
  DB_SERVER="your-server.database.windows.net" \
  DB_NAME="ChatBoxDB" \
  DB_USER="sqladmin" \
  DB_PASSWORD="password" \
  JWT_SECRET_KEY="your-secret-key" \
  SECRET_KEY="your-secret" \
  CORS_ORIGINS="https://yourdomain.com"
```

---

## <a name="custom-domain"></a>
## 7️⃣ CUSTOM DOMAIN & SSL / TÊN MIỀN TÙY CHỈNH & SSL

### Step 1: Buy Domain
- Go to Namecheap.com or GoDaddy.com
- Buy domain: example.com (cost: ~$8-15/year)

### Step 2: Configure DNS Records
1. Login to your domain provider
2. Go to DNS Management
3. Change Nameservers to:
   - Railway: Add CNAME record pointing to your Railway app
   - Render: Add CNAME record pointing to your Render app
   - Azure: Add CNAME record pointing to your Azure app

### Step 3: Enable SSL/HTTPS
- Railway: Automatic SSL
- Render: Automatic SSL
- Azure: Automatic SSL with App Service

### Step 4: Update Frontend

Edit [frontend/script.js](../frontend/script.js):

```javascript
// Change this line
const API_BASE_URL = 'http://localhost:5000';

// To this:
const API_BASE_URL = 'https://yourdomain.com';
```

---

## <a name="post-deployment"></a>
## 8️⃣ POST-DEPLOYMENT / SAU DEPLOYMENT

### ✅ Checklist:

- [ ] Test website at your domain: https://yourdomain.com
- [ ] Create admin account (if first deploy)
- [ ] Upload dataset and initialize knowledge base
- [ ] Configure Gemini API key
- [ ] Test chat functionality
- [ ] Monitor logs for errors
- [ ] Setup monitoring/alerts

### View Logs:

```bash
# Railway
railway logs

# Render
# Dashboard → Logs tab

# Azure
az webapp log tail --resource-group ChatBoxRG --name chatbox-app
```

### Monitor Performance:
- CPU & Memory usage
- Response times
- Error rates
- User count

### Scaling:

If your app gets slow:
1. **Railway**: Increase instance size
2. **Render**: Upgrade plan
3. **Azure**: Scale up App Service plan

---

## 🐛 TROUBLESHOOTING / GIẢI QUYẾT SỰ CỐ

### Issue: Database Connection Failed

**Solution:**
- Check IP whitelist on database server
- Verify credentials in environment variables
- Test connection string locally first

```python
import pyodbc
conn_str = 'YOUR_CONNECTION_STRING'
conn = pyodbc.connect(conn_str)
print("Connected!")
```

### Issue: CORS Error

**Solution:**
- Update CORS_ORIGINS environment variable
- Make sure frontend domain is in whitelist
- Check security_config.py

### Issue: Gemini API Error

**Solution:**
- Verify API key is valid
- Check API quotas at https://makersuite.google.com
- Enable Generative AI API in Google Cloud Console

### Issue: 502 Bad Gateway

**Solution:**
- Check app logs
- Restart container
- Verify all environment variables are set
- Check for Python errors

---

## 📞 SUPPORT / HỖ TRỢ

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Azure Docs: https://docs.microsoft.com/azure
- Flask Docs: https://flask.palletsprojects.com
- Google Gemini: https://ai.google.dev

---

## 🎉 SUCCESS!

Khi deploy thành công, bạn sẽ có:
✅ Website chạy 24/7 trên server cloud
✅ Mọi người trên thế giới có thể truy cập
✅ Database lưu trữ trên cloud
✅ HTTPS/SSL security
✅ Tên miền riêng (optional)

**Congratulations! Your ChatBox app is now live on the internet!** 🚀

---

## 💡 QUICK START - RECOMMENDED FLOW

1. **Buy domain** (Namecheap) - 5 mins
2. **Create Azure SQL Database** - 10 mins
3. **Push code to GitHub** - 5 mins
4. **Deploy on Railway** - 5 mins
5. **Configure environment variables** - 5 mins
6. **Setup custom domain** - 10 mins
7. **Test & Go Live** - 10 mins

**Total Time: ~50 minutes to go live! ⚡**

---

Last Updated: January 2026
Version: 1.0
