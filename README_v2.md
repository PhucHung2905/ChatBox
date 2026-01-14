# 🏠 Real Estate ChatBox v2.0

> **Intelligent Real Estate Consultation System with Authentication, User Management, and Admin Dashboard**

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Database](https://img.shields.io/badge/database-SQL%20Server-red)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Key Features

### 🔐 Authentication System
- User registration and login with JWT tokens
- Email and username uniqueness validation
- Secure password hashing with PBKDF2
- Session management and token verification
- Logout functionality

### 👥 User Management
- Admin dashboard for user management
- View all users with pagination
- Deactivate/Activate user accounts
- Promote regular users to admin
- View user details and chat statistics

### 📊 Admin Panel
- **User Management**: View, promote, deactivate users
- **Audit Logs**: Track all admin actions
- **System Statistics**: Real-time dashboard with:
  - Total users (active/inactive)
  - Total chats count
  - Active users in last 24h
  - Admin count
- **Chat History**: View user conversations

### 💬 Chat Features
- AI-powered real estate consultation
- Vector-based document search
- Context-aware responses
- Multi-turn conversation support
- Chat history storage and retrieval
- User-specific conversation isolation

### 💾 Database Management
- SQL Server backend with robust schema
- Automatic indexing for performance
- Stored procedures for complex queries
- Audit logging for compliance
- Data isolation between users

### ⚙️ User Features
- Update personal profile
- Change password
- View personal chat history
- Search knowledge base
- Manage conversations

---

## 🎯 What's New in v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Authentication | ❌ | ✅ |
| User Roles | ❌ | ✅ |
| Admin Panel | ❌ | ✅ |
| SQL Database | ❌ | ✅ |
| Audit Logs | ❌ | ✅ |
| User Management | ❌ | ✅ |
| JWT Security | ❌ | ✅ |
| Multi-user Chat | ❌ | ✅ |

---

## 🚀 Quick Start

### Minimum Requirements
- Python 3.8+
- SQL Server 2016+
- Windows/Linux/Mac

### 5-Minute Setup

1. **Install Dependencies**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup Database** (See [SETUP_GUIDE.md](SETUP_GUIDE.md))
   ```bash
   python migrate.py
   ```

3. **Configure Environment**
   ```bash
   # Copy and edit .env.example to .env
   cp .env.example .env
   ```

4. **Run Application**
   ```bash
   # Terminal 1 - Backend
   python app.py
   
   # Terminal 2 - Open Browser
   http://localhost:5000
   ```

5. **Login with Default Admin**
   - Email: `admin@chatbox.local`
   - Password: `admin123`

---

## 📋 API Endpoints

### Authentication
```
POST   /api/auth/register           - Register new user
POST   /api/auth/login              - Login and get JWT token
GET    /api/auth/me                 - Get current user info
GET    /api/auth/verify             - Verify JWT token
PUT    /api/auth/profile            - Update profile
POST   /api/auth/change-password    - Change password
```

### Chat (Require Authentication)
```
POST   /api/chat                    - Send message
POST   /api/search                  - Search knowledge base
GET    /api/chat-history            - Get chat history
POST   /api/clear-conversation      - Clear conversation
```

### Admin (Require Admin Role)
```
GET    /api/admin/users             - List all users
GET    /api/admin/users/<id>        - Get user details
GET    /api/admin/users/<id>/chat-history  - User's chats
POST   /api/admin/users/<id>/promote       - Promote to admin
POST   /api/admin/users/<id>/demote       - Demote from admin
POST   /api/admin/users/<id>/deactivate   - Deactivate user
POST   /api/admin/users/<id>/activate     - Activate user
GET    /api/admin/audit-logs       - View audit logs
GET    /api/admin/stats            - Dashboard statistics
```

---

## 🏗️ Architecture

### Backend Stack
- **Framework**: Flask 3.0
- **Database**: SQL Server with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **Security**: PBKDF2 password hashing
- **Search**: Vector embeddings (FAISS)
- **LLM**: Google Gemini 2.5 Flash

### Frontend Stack
- **Markup**: HTML5
- **Styling**: CSS3 with responsive design
- **Logic**: Vanilla JavaScript (ES6+)
- **Storage**: LocalStorage for tokens/preferences
- **Architecture**: Component-based

### Database Schema
```
┌─────────────┐
│   users     │
├─────────────┤
│ id (PK)     │
│ email       │
│ username    │
│ password    │
│ is_admin    │
│ is_active   │
└─────────────┘
      ↓
┌──────────────────┐        ┌──────────────┐
│ chat_histories   │        │ audit_logs   │
├──────────────────┤        ├──────────────┤
│ id (PK)          │        │ id (PK)      │
│ user_id (FK)     │        │ admin_id     │
│ message          │        │ action       │
│ response         │        │ created_at   │
│ created_at       │        └──────────────┘
└──────────────────┘
```

---

## 📁 Project Structure

```
ChatBox/
│
├── backend/                    # Flask API Server
│   ├── app.py                 # Main application
│   ├── auth.py                # Authentication logic
│   ├── admin.py               # Admin routes
│   ├── database.py            # SQLAlchemy models
│   ├── config.py              # Configuration
│   ├── migrate.py             # Database migration
│   ├── requirements.txt        # Dependencies
│   ├── .env.example           # Environment template
│   └── venv/                  # Virtual environment
│
├── frontend/                   # Web UI
│   ├── index.html             # Main layout
│   ├── script.js              # Application logic
│   └── styles.css             # Styling
│
├── datasets/                   # Knowledge base files
│   ├── investment_guide.txt
│   ├── legal_regulations.txt
│   ├── pricing_guide.txt
│   └── real_estate_projects.json
│
├── data/                       # Runtime data
│   └── knowledge_base/        # Vector database
│
├── docs/
│   ├── SETUP_GUIDE.md         # Installation guide
│   └── API_DOCUMENTATION.md   # API reference
│
├── start.bat                   # Windows startup script
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

---

## 🔐 Security Features

### User Security
- ✅ Secure password hashing (PBKDF2)
- ✅ JWT token authentication
- ✅ Token expiration (24 hours)
- ✅ Password strength validation
- ✅ Account deactivation support

### Data Security
- ✅ User data isolation
- ✅ Admin audit logging
- ✅ Encrypted connections (HTTPS ready)
- ✅ SQL injection prevention (ORM)
- ✅ CORS configuration

### Admin Controls
- ✅ Role-based access control
- ✅ Admin action logging
- ✅ User account management
- ✅ Activity monitoring
- ✅ Audit trail

---

## 📊 User Roles

### 👤 Regular User
- Register and login
- Send messages to chatbot
- Search knowledge base
- View personal chat history
- Update own profile
- Change own password

### 🔑 Admin User
- All user permissions +
- View all users
- Promote/demote users
- Deactivate/activate users
- View any user's chat history
- Access audit logs
- View system statistics
- Manage user accounts

---

## 🔄 Authentication Flow

```
1. User Registration
   │
   ├─> Validate email/username
   ├─> Hash password
   ├─> Create user in DB
   └─> Send success response

2. User Login
   │
   ├─> Verify email exists
   ├─> Check password hash
   ├─> Generate JWT token
   ├─> Update last_login
   └─> Return token + user data

3. Protected Request
   │
   ├─> Extract token from header
   ├─> Verify token signature
   ├─> Extract user_id
   ├─> Load user from DB
   └─> Allow/Deny based on permissions

4. Admin Action
   │
   ├─> Check is_admin flag
   ├─> Log action to audit_logs
   └─> Execute action
```

---

## 🚀 Deployment

### Development
```bash
FLASK_ENV=development python app.py
```

### Production
```bash
# Use a production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t chatbox:v2 .
docker run -p 5000:5000 chatbox:v2
```

---

## 📈 Performance

- **Database**: Optimized with indexes on common queries
- **Vector Search**: FAISS for fast similarity search
- **Caching**: JWT tokens cached on client
- **Pagination**: Admin endpoints support pagination
- **Connection Pooling**: SQLAlchemy manages connections

---

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
# Use browser developer tools for testing
```

---

## 🛠️ Troubleshooting

### Common Issues

**Q: "Database connection failed"**
- A: Check `.env` file, verify SQL Server is running

**Q: "Port 5000 already in use"**
- A: Change PORT in `.env` or kill process using port 5000

**Q: "Module not found"**
- A: Activate venv and run `pip install -r requirements.txt`

**Q: "ODBC driver not found"**
- A: Install ODBC Driver 17 from https://aka.ms/downloadodbc

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Added authentication system
- ✨ Added admin panel
- ✨ Added SQL Server support
- ✨ Added user management
- ✨ Added audit logging
- 🔧 Improved security
- 📚 Added comprehensive documentation

### v1.0.0
- 🚀 Initial release
- 💬 Basic chat functionality
- 🔍 Knowledge base search
- 📚 Vector database support

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💼 About

Developed as a modern real estate consultation system with enterprise-grade features.

**Key Technologies:**
- Python/Flask
- SQL Server
- JWT Authentication
- Vector Embeddings
- Google Gemini AI

---

## 🙏 Acknowledgments

- Flask and extensions community
- Google Gemini API
- SQL Server documentation
- FAISS library

---

## 📞 Support

- **Documentation**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Issues**: Open an issue on GitHub
- **Email**: [your-email@example.com](mailto:your-email@example.com)

---

## 🎯 Roadmap

- [ ] Email verification for registration
- [ ] Two-factor authentication
- [ ] Advanced search filters
- [ ] Chat export functionality
- [ ] User roles with custom permissions
- [ ] Real-time notifications
- [ ] Mobile app
- [ ] Multi-language support

---

## ⭐ Show Your Support

If you found this project helpful, please give it a star! ⭐

---

**Last Updated**: January 2026  
**Status**: ✅ Production Ready

---

*For detailed setup instructions, please refer to [SETUP_GUIDE.md](SETUP_GUIDE.md)*
