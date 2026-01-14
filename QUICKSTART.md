# 🌞 SOLAR ENERGY CONSULTING CHATBOX - Quick Start Guide

## ⚡ Bắt Đầu Nhanh (10 Phút)

### Bước 1: Chuẩn Bị Python & Dependencies
```bash
# 1. Mở PowerShell (Windows) hoặc Terminal
# 2. Di chuyển vào thư mục backend
cd e:\TTTNghiep\Project\ChatBox\backend

# 3. Tạo Virtual Environment
python -m venv venv

# 4. Kích hoạt Virtual Environment
# Trên Windows:
venv\Scripts\activate

# Trên macOS/Linux:
source venv/bin/activate
```

### Bước 2: Cài Đặt Dependencies
```bash
# Cài đặt các gói cần thiết
pip install -r requirements.txt

# Nếu gặp lỗi pyodbc, cài đặt các gói chính:
pip install flask flask-cors flask-sqlalchemy flask-jwt-extended python-dotenv requests faiss-cpu numpy python-docx PyPDF2 sentence-transformers werkzeug
```

### Bước 3: Cấu Hình Gemini API
```bash
# Lấy Gemini API Key từ: https://ai.google.dev/gemini-api
# 1. Truy cập https://ai.google.dev/gemini-api
# 2. Nhấn "Get API key" 
# 3. Tạo API key mới
# 4. Copy API key

# Sao chép file cấu hình
copy .env.example .env

# Mở file .env với Notepad hoặc VS Code
# Sửa dòng:
# GEMINI_API_KEY=AIzaSy... (dán API key của bạn)
# GEMINI_MODEL=gemini-2.5-flash
```

### Bước 4: Khởi Động Backend Server
```bash
# Đảm bảo bạn đang ở thư mục backend
cd e:\TTTNghiep\Project\ChatBox\backend

# Chạy server Flask
python app.py

# Bạn sẽ thấy output như này:
# ✓ Database initialized successfully
# ✓ Admin user already exists: admin@chatbox.local
# 🚀 Starting Real Estate ChatBox Backend (v2.0)
# Server running on http://localhost:5000
# Press CTRL+C to quit
```

### Bước 5: Mở Frontend & Chat
```bash
# Mở trình duyệt và truy cập:
http://localhost:5000

# Hoặc các URL khác:
# Đăng nhập:    http://localhost:5000/login.html
# Đăng ký:      http://localhost:5000/register.html
```

### Bước 6: Đăng Nhập hoặc Đăng Ký
```
Tài khoản Admin (sẵn có):
- Email: admin@chatbox.local
- Password: admin123

Hoặc tạo tài khoản mới bằng "Register"
```

### Bước 7: Chat với Chatbot
```
Hỏi ví dụ:
- "Hệ thống solar 10kW có giá bao nhiêu?"
- "Solar nên lắp đặt ở vị trí nào?"
- "Lắp đặt solar có cần cấp phép không?"
- "Hoàn vốn solar trong bao lâu?"
- "Lợi ích của solar energy là gì?"
```

## 🔍 Các Câu Hỏi Ví Dụ

```
Solar Energy Consulting:
- "Hệ thống solar 10kW có giá bao nhiêu?"
- "Solar nên lắp đặt ở vị trí nào?"
- "Lắp đặt solar có cần cấp phép không?"
- "Hoàn vốn solar trong bao lâu?"
- "Lợi ích của solar energy là gì?"
- "Bất lợi của solar energy?"
- "Hệ thống solar hybrid là gì?"
- "Bức xạ mặt trời ở Việt Nam như thế nào?"
```

## 📂 Cấu Trúc Tệp Quan Trọng

```
ChatBox/
├── backend/
│   ├── app.py              # Ứng dụng chính (Chạy cái này!)
│   ├── config.py           # Cấu hình (Sửa ở đây)
│   ├── .env                # Biến môi trường (Tạo từ .env.example)
│   ├── requirements.txt    # Danh sách dependencies
│   └── data/               # Vector database & knowledge base
│
├── frontend/
│   ├── index.html          # Giao diện chính
│   ├── script.js           # Logic JavaScript
│   └── styles.css          # Kiểu dáng
│
├── datasets/               # Tài liệu Solar Energy
│   ├── investment_guide.txt
│   ├── pricing_guide.txt
│   ├── legal_regulations.txt
│   └── real_estate_projects.json
│
└── QUICKSTART.md           # File này
```

## ⚠️ Vấn Đề Thường Gặp & Giải Pháp

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
# Giải pháp: Cài đặt dependencies
pip install -r requirements.txt

# Hoặc cài thủ công:
pip install flask flask-cors flask-sqlalchemy flask-jwt-extended python-dotenv
```

### ❌ "GEMINI_API_KEY not found"
```
Giải pháp:
1. Kiểm tra file .env có tồn tại không
2. Đảm bảo GEMINI_API_KEY có giá trị
3. Nếu không, lấy từ https://ai.google.dev/gemini-api
```

### ❌ "Address already in use (port 5000)"
```bash
# Giải pháp 1: Dùng port khác
set PORT=5001
python app.py

# Giải pháp 2: Tìm process chiếm port
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### ❌ "Connection refused" hoặc "Cannot connect to server"
```
Giải pháp:
1. Kiểm tra backend đang chạy (http://localhost:5000)
2. Nếu chưa, chạy: python app.py
3. Kiểm tra console có lỗi không
```

### ❌ "ModuleNotFoundError: sentence_transformers"
```bash
# Lỗi này xảy ra khi tải embedding model
# Giải pháp: Cài đặt đầy đủ
pip install sentence-transformers
```

### ❌ "Vector database is empty"
```
Giải pháp:
1. Kiểm tra folder datasets/ có file không
2. Khởi động lại server (Ctrl+C rồi python app.py)
3. Server sẽ tự tạo vector database từ datasets/
```

## 🚀 Chạy Lần Tới

Mỗi lần sau, chỉ cần:

```bash
# 1. Mở PowerShell
# 2. Di chuyển vào backend
cd e:\TTTNghiep\Project\ChatBox\backend

# 3. Kích hoạt virtual environment
venv\Scripts\activate

# 4. Chạy server
python app.py

# 5. Mở trình duyệt
# http://localhost:5000
```

## 📊 Tài Liệu Dataset

Chatbox được tích hợp 4 file dữ liệu Solar Energy:

| File | Nội dung | Sử dụng cho |
|------|---------|-----------|
| `investment_guide.txt` | Hướng dẫn đầu tư Solar (loại hệ thống, phân tích tài chính) | "Nên đầu tư solar không?", "Hoàn vốn mất bao lâu?" |
| `pricing_guide.txt` | Hướng dẫn định giá (phương pháp, giá tham khảo) | "Solar 10kW giá bao nhiêu?", "Chi phí từng thành phần?" |
| `legal_regulations.txt` | Quy định pháp lý (luật, cấp phép, thuế) | "Cần cấp phép không?", "Mức giá mua điện?" |
| `real_estate_projects.json` | 10 dự án Solar tiêu biểu | "Có dự án solar nào?", "Chi tiết dự án?" |

## 💡 Mẹo Sử Dụng

1. **Chat cụ thể hơn** để được trả lời chính xác hơn
   - ❌ "Solar thế nào?"
   - ✅ "Hệ thống solar 10kW rooftop ở TPHCM giá bao nhiêu?"

2. **Vector Search** tìm kiếm tài liệu nhanh
   - Nó sẽ tìm những tài liệu liên quan nhất từ datasets/

3. **Lịch sử Chat** được lưu vào database
   - Bạn có thể xem lại cuộc trò chuyện cũ

4. **Admin Account** để quản lý người dùng
   - Email: admin@chatbox.local
   - Password: admin123

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra error message trong console
2. Đọc log trong `data/logs/` (nếu có)
3. Xem file config có đúng không
4. Thử khởi động lại server

## 🎉 Chúc Mừng!

Nếu bạn thấy:
```
🚀 Starting Real Estate ChatBox Backend (v2.0)
Server running on http://localhost:5000
```

**Tức là bạn đã thành công!** 🎊

Giờ chatbox sẵn sàng tư vấn về Solar Energy ☀️

---

**Phiên bản**: v2.0 (Solar Energy Edition)  
**Ngôn ngữ**: Python + Flask + JavaScript  
**API**: Gemini (Google)  
**Database**: Vector (FAISS) + SQL Server  

Vui lòng để lại feedback nếu có vấn đề! 📧
4. **Deploy** - Đưa lên production (Heroku, AWS, v.v.)
5. **Analytics** - Theo dõi usage và hiệu suất

## 🎓 Học Thêm

- FAISS Vector Database: https://github.com/facebookresearch/faiss
- LangChain: https://github.com/langchain-ai/langchain
- OpenAI API: https://platform.openai.com/docs
- Flask Framework: https://flask.palletsprojects.com

## ✅ Checklist Hoàn Thành Setup

- [ ] Python 3.8+ đã cài đặt
- [ ] Virtual environment đã tạo
- [ ] Dependencies đã cài đặt (pip install -r requirements.txt)
- [ ] .env file đã cấu hình với OPENAI_API_KEY
- [ ] Tài liệu datasets đã có sẵn
- [ ] Backend server đang chạy (port 5000)
- [ ] Frontend đang hoạt động
- [ ] Knowledge base đã được tạo
- [ ] Chatbox sẵn sàng sử dụng

---

💡 **Tip**: Để chạy server Backend lâu dài mà không bị đóng khi đóng terminal:
```bash
# Windows - Chạy ở background
start python app.py

# Hoặc sử dụng task scheduler để tự động khởi động khi boot
```

🎉 **Chúc mừng!** Bạn đã thiết lập thành công Real Estate ChatBox!

Nếu gặp vấn đề, hãy:
1. Kiểm tra lại các bước trên
2. Xem phần "Vấn đề Thường Gặp"
3. Kiểm tra logs trong terminal

Happy chatting! 🚀
