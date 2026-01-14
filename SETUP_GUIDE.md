# ChatBox v2.0 - Setup Guide 🚀

## 📋 Tổng Quan Tính Năng

Real Estate ChatBox v2.0 là một hệ thống tư vấn bất động sản thông minh với các tính năng:

### 🔐 Authentication & Authorization
- ✅ Đăng nhập / Đăng ký người dùng
- ✅ JWT Token-based authentication
- ✅ Quản lý phân quyền (Admin / User)
- ✅ Đổi mật khẩu & Cập nhật hồ sơ

### 👥 User Management
- ✅ Danh sách người dùng
- ✅ Xem lịch sử trò chuyện của từng user
- ✅ Cấp quyền Admin/Demote user
- ✅ Kích hoạt/Vô hiệu hóa tài khoản

### 📊 Admin Panel
- ✅ Xem thống kê hệ thống (tổng user, chat, etc)
- ✅ Audit log - Lịch sử hành động Admin
- ✅ Quản lý tài khoản người dùng
- ✅ Dashboard với các metrics quan trọng

### 💬 Chat Features
- ✅ Chat với AI assistant (xác thực bắt buộc)
- ✅ Tìm kiếm trong cơ sở dữ liệu
- ✅ Lịch sử trò chuyện cá nhân
- ✅ Lưu trữ trong SQL Server

### 💾 Database
- ✅ SQL Server (2016+)
- ✅ Bảng: Users, Chat Histories, Audit Logs
- ✅ Indexes & Stored Procedures
- ✅ Views cho dễ dàng truy vấn

---

## 🔧 Prerequisites

### Software Required
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **SQL Server 2016+** - [Download](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- **ODBC Driver 17 for SQL Server** - [Download](https://aka.ms/downloadodbc)
- **Git** (Optional) - [Download](https://git-scm.com/)

### System Requirements
- Windows 10+ or Linux/Mac with SQL Server
- 2GB RAM minimum
- 500MB disk space
- Internet connection (for APIs)

---

## 📦 Installation Steps

### Step 1: Install SQL Server

1. Download SQL Server Express from: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Run installer and follow the wizard
3. Note your server name (usually `localhost` or `YOUR-PC-NAME`)
4. Note the SA password you set

### Step 2: Install ODBC Driver

1. Download from: https://aka.ms/downloadodbc
2. Run installer
3. Verify installation: Open ODBC Data Sources and check for "ODBC Driver 17 for SQL Server"

### Step 3: Clone/Download Project

```bash
# If using Git
git clone <repository-url>
cd ChatBox

# Or download and extract the ZIP file
```

### Step 4: Create Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# or: source venv/bin/activate  # On Linux/Mac
```

### Step 5: Install Python Dependencies

```bash
# Make sure venv is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Configure Database

Create a `.env` file in the `backend` folder:

```bash
# Copy from .env.example
cp .env.example .env
# Edit .env with your SQL Server details
```

Edit the `.env` file with your database credentials:

```env
DB_SERVER=localhost
DB_NAME=ChatBoxDB
DB_USER=sa
DB_PASSWORD=your_sa_password
DB_DRIVER={ODBC Driver 17 for SQL Server}

JWT_SECRET_KEY=your-jwt-secret-key-here
ADMIN_EMAIL=admin@chatbox.local
ADMIN_PASSWORD=admin123

GEMINI_API_KEY=your-api-key-here
```

### Step 7: Run Database Migration

```bash
python migrate.py
```

Or manually in SQL Server Management Studio:
1. Open SQL Server Management Studio
2. Connect to your SQL Server
3. Open `backend/migrate.py` and copy the SQL script
4. Paste it in a new query window and execute

### Step 8: Verify Installation

```bash
# Run the menu script
# On Windows:
..\start.bat
# Choose option 7: Check Installation
```

---

## 🚀 Running the Application

### Option 1: Using start.bat (Windows)

```bash
# From the project root directory
start.bat

# Then choose from menu:
# 4. Start Backend (Flask API)
# 5. Start Frontend in Browser
```

### Option 2: Manual Start

Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate
python app.py
```

Terminal 2 (Frontend):
```bash
# Open browser and go to http://localhost:5000
```

### Option 3: Using Docker (Optional)

```bash
docker-compose up
```

---

## 🔑 Default Admin Account

- **Email**: `admin@chatbox.local`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change the admin password after first login!

---

## 📚 API Documentation

### Authentication Endpoints

```
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
GET /api/auth/verify
PUT /api/auth/profile
POST /api/auth/change-password
```

### Chat Endpoints (Require Auth)

```
POST /api/chat
POST /api/search
GET /api/chat-history
POST /api/clear-conversation
```

### Admin Endpoints (Require Admin Role)

```
GET /api/admin/users
GET /api/admin/users/<id>
GET /api/admin/users/<id>/chat-history
POST /api/admin/users/<id>/promote
POST /api/admin/users/<id>/demote
POST /api/admin/users/<id>/deactivate
POST /api/admin/users/<id>/activate
GET /api/admin/audit-logs
GET /api/admin/stats
```

---

## 🔗 Troubleshooting

### Issue: "Cannot connect to SQL Server"

**Solution:**
1. Verify SQL Server is running
2. Check server name: `SELECT @@SERVERNAME` in SSMS
3. Verify ODBC driver: Open ODBC Data Sources
4. Test connection string in `.env`

### Issue: "ODBC Driver 17 not found"

**Solution:**
1. Download and install ODBC Driver 17: https://aka.ms/downloadodbc
2. Restart Python/Terminal
3. Verify in ODBC Data Sources

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Database already exists"

**Solution:**
```sql
-- In SQL Server Management Studio, to drop and recreate:
DROP DATABASE ChatBoxDB;
-- Then run migrate.py again
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Change port in .env
PORT=5001

# Or kill the process using port 5000:
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

---

## 📝 File Structure

```
ChatBox/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── auth.py             # Authentication module
│   ├── admin.py            # Admin features
│   ├── database.py         # Database models
│   ├── config.py           # Configuration
│   ├── migrate.py          # Database migration script
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Configuration file (create this)
│   └── venv/               # Virtual environment
│
├── frontend/
│   ├── index.html          # Main HTML
│   ├── script.js           # JavaScript logic
│   └── styles.css          # Styling
│
├── datasets/               # Knowledge base files
├── data/                   # Vector database
├── start.bat               # Windows startup script
└── README.md               # Documentation
```

---

## 🔐 Security Best Practices

1. **Change Default Credentials**
   ```bash
   # After first login, change admin password in Settings
   ```

2. **Update Secret Keys** (Production)
   ```env
   SECRET_KEY=generate-random-string-here
   JWT_SECRET_KEY=generate-another-random-string
   ```

3. **Use Strong Passwords**
   - Minimum 6 characters (enforced)
   - Mix of uppercase, lowercase, numbers, symbols
   - Never use the same password as other accounts

4. **Database Security**
   - Use complex SA password
   - Restrict database access
   - Keep SQL Server updated
   - Use Windows Authentication when possible

5. **HTTPS in Production**
   - Use a reverse proxy (Nginx, Apache)
   - Get SSL certificate (Let's Encrypt)
   - Force HTTPS on all endpoints

6. **API Security**
   - JWT tokens expire after 24 hours
   - Validate all user inputs
   - Use CORS appropriately
   - Rate limiting recommended

---

## 📊 Database Schema

### users table
```sql
- id (UUID)
- email (unique)
- username (unique)
- password_hash
- full_name
- is_admin (boolean)
- is_active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
- last_login (timestamp)
```

### chat_histories table
```sql
- id (UUID)
- user_id (FK)
- conversation_id
- message (text)
- response (text)
- context_used (int)
- sources (JSON)
- created_at (timestamp)
```

### audit_logs table
```sql
- id (UUID)
- admin_id (FK)
- action (varchar)
- target_user_id (FK, nullable)
- details (JSON, nullable)
- created_at (timestamp)
```

---

## 🚀 Performance Tips

1. **Database Indexes**: Already created for common queries
2. **Caching**: JWT tokens cached on client
3. **Pagination**: Admin endpoints support pagination (per_page=20)
4. **Connection Pooling**: SQLAlchemy handles connection pooling

---

## 📞 Support & Contact

- **Issues**: Check Troubleshooting section above
- **Documentation**: See README.md
- **API Docs**: Available at http://localhost:5000/api
- **Database**: SQL Server Management Studio for direct queries

---

## 🎯 Next Steps

1. ✅ Install and run the application
2. ✅ Login with admin account
3. ✅ Create test users and explore
4. ✅ Customize for your needs
5. ✅ Deploy to production (guide coming soon)

---

## 📄 License

[Your License Here]

## 👨‍💼 Author

Real Estate ChatBox Development Team

---

## 🎉 Happy Coding!

For questions or contributions, please open an issue or contact the development team.
