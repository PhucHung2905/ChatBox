# ✅ SQL Server Database Setup - Complete!

## 📊 Database Information

**Server**: PHUCHUNG\SQLEXPRESS  
**Database**: ChatBoxDB  
**Status**: ✅ Ready to use

---

## 📋 Tables Created (3)

### 1️⃣ **users** (10 columns)
Lưu thông tin tài khoản người dùng
```sql
Columns:
  • id (varchar 36) - PRIMARY KEY
  • email (varchar 255) - UNIQUE, NOT NULL
  • username (varchar 100) - UNIQUE, NOT NULL
  • password_hash (varchar 500) - NOT NULL
  • full_name (varchar 255) - NULL
  • is_admin (bit) - DEFAULT 0
  • is_active (bit) - DEFAULT 1
  • created_at (datetime) - DEFAULT GETUTCDATE()
  • updated_at (datetime) - DEFAULT GETUTCDATE()
  • last_login (datetime) - NULL

Indexes: 5 (email, username, is_admin, is_active, created_at)
```

### 2️⃣ **chat_histories** (8 columns)
Lưu lịch sử trò chuyện của người dùng
```sql
Columns:
  • id (varchar 36) - PRIMARY KEY
  • user_id (varchar 36) - FOREIGN KEY → users.id, ON DELETE CASCADE
  • conversation_id (varchar 255)
  • message (text)
  • response (text)
  • context_used (int) - DEFAULT 0
  • sources (text) - NULL
  • created_at (datetime) - DEFAULT GETUTCDATE()

Indexes: 3 (user_id, conversation_id, created_at)
Foreign Keys: 1 (user_id → users.id)
```

### 3️⃣ **audit_logs** (6 columns)
Lưu lịch sử hành động của admin
```sql
Columns:
  • id (varchar 36) - PRIMARY KEY
  • admin_id (varchar 36) - NOT NULL
  • action (varchar 255) - NOT NULL
  • target_user_id (varchar 36) - NULL
  • details (text) - NULL
  • created_at (datetime) - DEFAULT GETUTCDATE()

Indexes: 4 (admin_id, action, target_user_id, created_at)
```

---

## 🔧 Additional Resources Created

### Stored Procedures (2)
1. **sp_GetUserChatStats** @UserId
   - Tính toán thống kê chat cho một user

2. **sp_GetAdminStats**
   - Lấy tất cả thống kê hệ thống

### Views (1)
1. **vw_UserActivitySummary**
   - Kết hợp thông tin user và chat stats

---

## 👤 Default Admin Account

**Email**: admin@chatbox.local  
**Password**: admin123  
**Role**: Administrator  
**Status**: Active ✅

⚠️ **Important**: Hãy thay đổi mật khẩu sau lần đăng nhập đầu tiên!

---

## 📊 Database Statistics

| Item | Count |
|------|-------|
| Tables | 3 |
| Columns | 24 |
| Indexes | 12 |
| Foreign Keys | 1 |
| Stored Procedures | 2 |
| Views | 1 |

---

## 🚀 Bước Tiếp Theo

1. **Cài đặt Python Dependencies**
   ```bash
   cd backend
   pip install flask flask-cors flask-sqlalchemy flask-jwt-extended pyodbc python-dotenv sentence-transformers faiss-cpu google-generativeai
   ```

2. **Tạo .env file** (nếu chưa có)
   ```bash
   cd backend
   cat > .env << EOF
   FLASK_ENV=development
   PORT=5000
   SECRET_KEY=your-secret-key-change-in-production
   JWT_SECRET_KEY=your-jwt-secret-key
   
   # SQL Server
   DB_SERVER=PHUCHUNG\SQLEXPRESS
   DB_NAME=ChatBoxDB
   DB_USER=PhucHung
   DB_PASSWORD=1234
   DB_DRIVER={ODBC Driver 17 for SQL Server}
   DB_TRUSTED_CONNECTION=False
   
   # Gemini API
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-2.5-flash
   EOF
   ```

3. **Khởi động Backend**
   ```bash
   cd backend
   python app.py
   ```

4. **Mở Frontend**
   - Truy cập: http://localhost:5000
   - Đăng nhập: admin@chatbox.local / admin123

---

## 🔍 Verification Commands

### Kiểm tra Database
```sql
USE ChatBoxDB;

-- Xem tất cả bảng
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo';

-- Xem admin user
SELECT email, username, is_admin FROM users;

-- Xem thống kê
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as total_chats FROM chat_histories;
SELECT COUNT(*) as total_audit_logs FROM audit_logs;
```

### Kiểm tra Connection String
```python
# Từ backend
python -c "from config import SQLALCHEMY_DATABASE_URI; print(SQLALCHEMY_DATABASE_URI)"
```

---

## 📝 File Tạo Ra

- **setup_database.sql** - SQL migration script
- **setup_database.bat** - Windows batch runner (optional)
- **DATABASE_SETUP.md** - Documentation (this file)

---

## 🎉 Summary

✅ Database ChatBoxDB created  
✅ 3 tables with 24 columns created  
✅ 12 indexes for performance created  
✅ Foreign keys and relationships set  
✅ 2 stored procedures created  
✅ 1 view created  
✅ Default admin user created  
✅ Ready for Flask application!

---

**Created**: January 7, 2026  
**Status**: Production Ready ✅

