# 🚀 QUICK START - DEPLOY IN 1 HOUR

## ⏱️ Timeline: ~60 phút từ đầu đến khi live

Bạn sẽ có một website hoạt động 24/7 mà mọi người trên thế giới có thể truy cập!

---

## 🎯 FLOW DIAGRAM

```
0️⃣  Setup (20 mins)
    ↓
1️⃣  Create Database (10 mins)
    ↓
2️⃣  Deploy on Railway (15 mins)
    ↓
3️⃣  Configure & Test (10 mins)
    ↓
4️⃣  Setup Domain (Optional, 5 mins)
    ↓
🎉 LIVE ON INTERNET!
```

---

## 📝 QUICK CHECKLIST

Before starting, make sure you have:
- [ ] GitHub account (https://github.com)
- [ ] Gemini API Key (https://makersuite.google.com/app/apikey)
- [ ] Email address (for Railway signup)

---

## 0️⃣ PREP (20 minutes)

### Push Code to GitHub

```bash
# Command line / Terminal
cd e:\TTTNghiep\Project\ChatBox

git init
git add .
git commit -m "Initial commit - ready to deploy"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ChatBox.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

### Generate Secret Keys

```bash
cd backend
python generate_keys.py
```

Copy the output - you'll need it soon!

---

## 1️⃣ CREATE DATABASE (10 minutes)

### Option A: Azure SQL (Recommended)

1. Go to: https://portal.azure.com
2. Sign up for free (get $200 credit)
3. Create SQL Database
   - Name: `chatboxdb`
   - Server: New → `chatbox-server`
   - Admin login: `sqladmin`
   - Password: `YourStrongPassword123!`
4. Firewall → Allow Azure services
5. Copy Connection String

### Option B: AWS RDS

1. Go to: https://console.aws.amazon.com
2. RDS → Create Database
3. Engine: SQL Server Express
4. Instance: db.t3.micro
5. DB name: `chatboxdb`
6. Admin: `admin` / `YourStrongPassword123!`

**Save your:**
- ✅ Server address
- ✅ Database name
- ✅ Username
- ✅ Password

---

## 2️⃣ DEPLOY ON RAILWAY (15 minutes)

### Step 1: Create Railway Account

1. Go to: https://railway.app
2. Click "Start Project"
3. Select "Deploy from GitHub repo"
4. Choose your ChatBox repository
5. Click "Deploy"

Wait for build... (2-5 mins)

### Step 2: Add Environment Variables

Railway Dashboard → Variables → Add:

```bash
# Copy-paste each one:

FLASK_ENV=production
DEBUG=False
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-2.5-flash
DB_SERVER=your-server.database.windows.net
DB_NAME=chatboxdb
DB_USER=sqladmin
DB_PASSWORD=YourStrongPassword123!
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_TRUSTED_CONNECTION=False
JWT_SECRET_KEY=PASTE_FROM_generate_keys.py
SECRET_KEY=PASTE_FROM_generate_keys.py
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
CORS_ORIGINS=https://yourdomain.com,http://localhost:3000
```

**Replace with YOUR actual values!**

### Step 3: Deploy

Click "Redeploy" → Wait for build ✨

---

## 3️⃣ TEST & CONFIGURE (10 minutes)

### Get Your URL

Railway Dashboard → Deployments → Copy URL
Example: `https://chatbox-abc123.railway.app`

### Update Frontend

Edit: `frontend/script.js`

```javascript
// Find this line (around line 1):
const API_BASE_URL = 'http://localhost:5000';

// Change to:
const API_BASE_URL = 'https://chatbox-abc123.railway.app';
```

### Push Update

```bash
git add frontend/script.js
git commit -m "Update API URL"
git push origin main
```

Railway redeploys automatically! ✨

### Test Website

1. Visit: `https://chatbox-abc123.railway.app`
2. Register account
3. Try chat
4. If error → Check Railway logs

---

## 4️⃣ SETUP CUSTOM DOMAIN (Optional, 5 mins)

### Buy Domain

1. Go to: https://namecheap.com or https://godaddy.com
2. Search & buy: `yourdomain.com` (~$10/year)

### Connect to Railway

Railway Dashboard → Custom Domain → Add:
```
yourdomain.com
```

Railway shows DNS record → Add to your domain provider's DNS settings

### Update Frontend Again

```javascript
// frontend/script.js
const API_BASE_URL = 'https://yourdomain.com';
```

```bash
git add frontend/script.js
git commit -m "Update to custom domain"
git push origin main
```

Wait 24 hours for DNS to propagate

---

## ✅ SUCCESS!

You now have:
- ✅ Website running 24/7
- ✅ Can access from anywhere in world
- ✅ Custom domain (optional)
- ✅ HTTPS/SSL automatic
- ✅ Database in cloud
- ✅ Ready for users!

---

## 💰 COSTS

| Service | Cost | Free Tier |
|---------|------|-----------|
| Railway | $5-50/month | Limited |
| Azure SQL | $5-50/month | $200 credit |
| Gemini API | $0-50/month | 15 RPM free |
| Domain | $10/year | - |
| **Total** | **~$15-100/month** | **Can be FREE first year** |

---

## 📞 PROBLEMS?

### White screen?
- Check Railway logs
- Verify API URL in frontend/script.js

### 502 Error?
- App crashed
- Check environment variables
- Verify database connection

### CORS Error?
- Update CORS_ORIGINS variable
- Redeploy

### Can't login?
- Database initialized?
- Run: `python backend/init_production_db.py` via Railway shell
- Check logs for SQL errors

---

## 📚 DETAILED GUIDES

For more detailed steps, see:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Full guide
- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Railway specific

---

## 🎊 CELEBRATE! 🎉

You just deployed a production application to the internet!

Next steps:
- Share with friends: `https://yourdomain.com`
- Monitor usage: Railway Dashboard
- Add more features
- Scale as needed

**Questions? Check the detailed guides or Railway docs!**
