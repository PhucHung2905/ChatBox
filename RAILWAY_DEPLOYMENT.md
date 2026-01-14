# 🚀 RAILWAY DEPLOYMENT GUIDE - STEP BY STEP

## Vì sao Railway?
- ✅ **Dễ dàng**: Click vài nút là deploy xong
- ✅ **Rẻ**: $5-50/month tùy usage
- ✅ **Nhanh**: Deploy trong 5 phút
- ✅ **Tự động**: Tự build & deploy khi push code
- ✅ **Monitoring**: Dashboard đẹp để theo dõi

## 📋 CHECKLIST TRƯỚC KHI BẮT ĐẦU

- [ ] GitHub account (https://github.com)
- [ ] Gemini API Key (https://makersuite.google.com/app/apikey)
- [ ] SQL Server cloud (Azure SQL Database hoặc AWS RDS)
- [ ] Code đã push lên GitHub

---

## 🔧 STEP 1: PREPARE YOUR CODE

### 1.1 Tạo `.env.example` (đã tạo sẵn)

Kiểm tra file [.env.example](../.env.example) tồn tại

### 1.2 Cập nhật `runtime.txt`

File đã tạo. Nội dung:
```
python-3.11.7
```

### 1.3 Cập nhật `Procfile`

File đã tạo. Nội dung:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

### 1.4 Push code lên GitHub

```bash
# Nếu chưa push
git init
git add .
git commit -m "Prepare for Railway deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ChatBox.git
git push -u origin main

# Hoặc nếu đã có repo
git add .
git commit -m "Production ready"
git push origin main
```

✅ Kiểm tra code đã có trên GitHub

---

## 🔗 STEP 2: CREATE SQL SERVER DATABASE

### Option A: Azure SQL Database (Recommended)

1. **Truy cập Azure Portal**
   - URL: https://portal.azure.com
   - Đăng nhập hoặc tạo tài khoản (free $200 credit)

2. **Tạo SQL Database**
   ```
   - Click "Create a resource"
   - Search "SQL Database"
   - Click "Create"
   
   Settings:
   - Subscription: Free Trial
   - Resource group: Create new → "chatbox-rg"
   - Database name: "chatboxdb"
   - Server: Create new
     - Server name: "chatbox-server" (must be unique)
     - Admin login: "sqladmin"
     - Password: Strong password (min 8 chars, mix of upper/lower/numbers/symbols)
   - Compute + storage: Basic (B1)
   - Click "Review + Create"
   - Click "Create"
   ```

3. **Lấy Connection String**
   ```
   - Vào SQL Database vừa tạo
   - Click "Connection strings"
   - Copy "ADO.NET" string
   
   Dạng: Server=tcp:chatbox-server.database.windows.net,1433;Initial Catalog=chatboxdb;Persist Security Info=False;User ID=sqladmin;Password=YOUR_PASSWORD;
   ```

4. **Configure Firewall (QUAN TRỌNG!)**
   ```
   - Vào Server → "Networking"
   - Public endpoint: "Allow Azure services and resources to access this server" = YES
   - Add firewall rule: 0.0.0.0 - 255.255.255.255
   (Later can restrict to Railway IP only)
   ```

### Option B: AWS RDS (Alternative)

1. Tới https://console.aws.amazon.com
2. RDS → Create Database
3. Engine: SQL Server Express
4. Instance: db.t3.micro (free tier)
5. DB name: chatboxdb
6. Master username: admin
7. Password: strong password
8. Storage: 20 GB
9. Create

---

## 🎯 STEP 3: SETUP RAILWAY ACCOUNT

### 3.1 Create Railway Account

1. Go to https://railway.app
2. Click "Start Project" (top right)
3. Click "Deploy from GitHub repo"
4. Authorize Railway to access GitHub
5. Select your "ChatBox" repository
6. Click "Deploy"

Railway sẽ tự động bắt đầu build

### 3.2 Wait for Initial Build

- Chờ vài phút, Railway sẽ build Docker image
- Nếu lỗi, kiểm tra Logs tab

---

## ⚙️ STEP 4: CONFIGURE ENVIRONMENT VARIABLES

### 4.1 Thêm Environment Variables

Trong Railway Dashboard:
1. Click vào project "ChatBox"
2. Click "Variables" tab
3. Add các biến sau:

```bash
# Flask
FLASK_ENV=production
DEBUG=False
PORT=5000

# Gemini API
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-2.5-flash

# Database (từ Azure SQL)
DB_SERVER=your-server.database.windows.net
DB_NAME=chatboxdb
DB_USER=sqladmin
DB_PASSWORD=your_strong_password
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_TRUSTED_CONNECTION=False

# Security
JWT_SECRET_KEY=generate-a-very-strong-random-key-32-chars-min
SECRET_KEY=another-strong-random-key-for-flask

# Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=strong_admin_password

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,http://localhost:3000
```

### 4.2 Generate Secure Keys

```bash
# Chạy locally để generate keys
cd backend
python generate_keys.py

# Copy output vào JWT_SECRET_KEY và SECRET_KEY ở trên
```

---

## 🗄️ STEP 5: INITIALIZE DATABASE

### 5.1 Run Database Init Script

Railway cho phép chạy commands. Cách dễ nhất:

1. **Tạo file `railway.json`** (nếu cần)
   
   Hoặc dùng Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   railway shell
   python backend/init_production_db.py
   ```

2. **Hoặc khác cách - Tạo script phía backend**

   Thêm route để init database:
   ```python
   @app.route('/api/admin/init-db', methods=['POST'])
   def init_db_route():
       # Gọi init_production_db()
       # Return status
   ```

3. **Thêm command khi deploy**
   
   Sửa `Procfile`:
   ```
   release: python backend/init_production_db.py
   web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
   ```

✅ Database sẽ tự init khi deploy

---

## 🌐 STEP 6: UPDATE FRONTEND API URL

### 6.1 Lấy Railway URL

```
- Trong Railway Dashboard
- Click project
- Deployments tab
- Lấy URL như: https://chatbox-abc123.railway.app
```

### 6.2 Cập nhật Frontend

Edit [frontend/script.js](../frontend/script.js):

```javascript
// OLD:
const API_BASE_URL = 'http://localhost:5000';

// NEW:
const API_BASE_URL = 'https://chatbox-abc123.railway.app';
```

### 6.3 Push code

```bash
git add frontend/script.js
git commit -m "Update API URL for Railway production"
git push origin main
```

Railway tự động redeploy ✨

---

## ✅ STEP 7: TEST YOUR DEPLOYMENT

### 7.1 Visit Your Site

Tới: `https://your-railway-url.railway.app`

Bạn sẽ thấy:
- [ ] Login/Register page load
- [ ] Chat interface appear
- [ ] API calls work (check browser DevTools)

### 7.2 Test Functionality

1. **Register account**
   ```
   - Click "Đăng ký"
   - Fill form
   - Click "Đăng ký"
   - Should redirect to chat
   ```

2. **Login**
   ```
   - Click "Đăng nhập"
   - Enter credentials
   - Should show chat
   ```

3. **Chat**
   ```
   - Type message: "Xin chào"
   - Should get response
   ```

4. **Check Logs** (nếu error)
   ```
   - Railway Dashboard → Logs tab
   - Tìm error messages
   ```

---

## 🎉 STEP 8: SETUP CUSTOM DOMAIN (Optional but Recommended)

### 8.1 Buy Domain

Options:
- **Namecheap**: https://namecheap.com (~$9/year)
- **GoDaddy**: https://godaddy.com (~$15/year)
- **Google Domains**: https://domains.google (~$12/year)

Buy: `yourname.com` hoặc `yourdomain.vn`

### 8.2 Connect Domain to Railway

1. **Railway Dashboard → Custom Domain**
   - Click "Add Custom Domain"
   - Enter: `yourdomain.com`
   - Click "Add"

2. **Railway sẽ cho DNS records**
   - Type: CNAME
   - Value: `your-railway-domain.railway.app`

3. **Cấu hình DNS tại domain provider**
   ```
   Nameserver cũ:
   - Remove old nameservers
   
   Thêm:
   - CNAME: yourdomain.com → your-railway-domain.railway.app
   
   Hoặc đổi nameserver (tùy provider)
   ```

### 8.3 Wait for DNS Propagation

- DNS thường cập nhật trong 24 giờ
- Check: https://dns.google (lấy `yourdomain.com`)
- HTTPS tự động bật với Railway

### 8.4 Update Frontend URL

```javascript
// frontend/script.js
const API_BASE_URL = 'https://yourdomain.com';
```

---

## 📊 MONITORING & MAINTENANCE

### Logs & Monitoring

```bash
# View logs in Railway Dashboard
- Click project
- Logs tab
- Tail last 100 lines

# Check CPU/Memory usage
- Metrics tab
- See resource usage
```

### Update Code

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Railway automatically redeploys! ✨
```

### View Live Logs

```bash
railway login
railway logs --follow
```

---

## 🚨 TROUBLESHOOTING

### Issue: Build Failed

**Check:**
1. Python version compatible?
2. All requirements installed?
3. No syntax errors?

**Fix:**
```bash
# Test locally
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements-prod.txt
python backend/app.py
```

### Issue: 502 Bad Gateway

**Reason:** App crashed
**Fix:**
1. Check Railway logs for errors
2. Verify all environment variables set
3. Verify database connection
4. Restart app: Railway → Restart Deploy

### Issue: CORS Error

**Browser shows:** Access blocked by CORS

**Fix:**
```
.env:
CORS_ORIGINS=https://yourdomain.com,https://yourdomain.railway.app
```

### Issue: Database Connection Failed

**Check:**
1. Connection string correct?
2. Database firewall allows Railway IP?
3. Username/password correct?

**Verify Connection:**
```bash
# Locally
import pyodbc
conn_str = 'YOUR_CONNECTION_STRING'
conn = pyodbc.connect(conn_str)
print("✅ Connected!")
```

### Issue: Gemini API Error

**Fix:**
1. API key valid? https://makersuite.google.com/app/apikey
2. API enabled? https://console.cloud.google.com
3. Quota exhausted? Check usage

---

## 📚 USEFUL LINKS

- Railway Docs: https://docs.railway.app
- Azure SQL: https://docs.microsoft.com/azure/sql-database
- Flask Docs: https://flask.palletsprojects.com
- Gemini API: https://ai.google.dev

---

## 🎊 SUCCESS CHECKLIST

- [x] Code on GitHub
- [x] Database created on Azure
- [x] Railway project created
- [x] Environment variables set
- [x] Database initialized
- [x] Frontend API URL updated
- [x] Custom domain configured (optional)
- [x] Site tested & working
- [x] Live on the internet! 🌍

**Your app is now live! Everyone can use it! 🎉**

---

## 📞 NEED HELP?

- Railway Support: https://railway.app/support
- GitHub Issues: https://github.com/your-repo/issues
- Stack Overflow: tag railway-app or flask

**Time to deploy: ~1 hour (including setup)**
**Cost: ~$5-50/month depending on usage**
