# 🏠 Health ChatBox

Một chatbox thông minh để tư vấn về sức khỏe, tích hợp vector database, LLM và sức khỏe.

## 🎯 Tính năng

- **Chat thông minh**: Trả lời câu hỏi về sức khỏe con người dựa trên cơ sở dữ liệu kiến thức
- **Tìm kiếm vector**: Tìm kiếm tài liệu liên quan dựa trên ngữ nghĩa
- **Quản lý cơ sở dữ liệu**: Tạo lại và quản lý vector database
- **Giao diện thân thiện**: UI hiện đại với hỗ trợ mobile
- **Hỗ trợ đa định dạng**: Tài liệu TXT, PDF, DOCX, JSON

## 🏗️ Cấu trúc Dự Án

```
ChatBox/
├── backend/                  # Backend API (Flask)
│   ├── app.py               # Ứng dụng chính
│   ├── config.py            # Cấu hình
│   ├── vector_db.py         # Vector database với FAISS
│   ├── knowledge_base.py    # Quản lý kiến thức
│   ├── llm_handler.py       # Xử lý LLM (OpenAI)
│   ├── requirements.txt     # Dependencies
│   ├── .env.example         # Mẫu file cấu hình
│   └── /data                # Dữ liệu lưu trữ
│       └── /knowledge_base  # Vector database
│       └── /vector_db       # Index FAISS
├── frontend/                # Frontend (HTML/CSS/JS)
│   ├── index.html          # Trang chính
│   ├── styles.css          # Kiểu dáng
│   ├── script.js           # Logic JavaScript
│   └── /data               # Dữ liệu cache
├── datasets/               # Tài liệu đầu vào
│   ├── real_estate_projects.json      # Dữ liệu dự án
│   ├── legal_regulations.txt          # Quy định pháp lý
│   ├── pricing_guide.txt              # Hướng dẫn định giá
│   └── investment_guide.txt           # Hướng dẫn đầu tư
├── data/                   # Dữ liệu được xử lý
│   ├── knowledge_base/    # Tài liệu embedding
│   └── vector_db/         # Vector database
└── README.md              # Tài liệu này
```

## 🚀 Hướng Dẫn Cài Đặt

### 1. Yêu Cầu Hệ Thống
- Python 3.8+
- Node.js 14+ (tùy chọn, nếu muốn chạy server frontend)
- OpenAI API Key

### 2. Cài Đặt Backend

```bash
# Chuyển vào thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 3. Cấu Hình Environment

```bash
# Sao chép file cấu hình
cp .env.example .env

# Chỉnh sửa .env và thêm OpenAI API Key
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 4. Chuẩn Bị Dữ Liệu

```bash
# Đảm bảo các file dữ liệu có trong thư mục datasets/
# - real_estate_projects.json
# - legal_regulations.txt
# - pricing_guide.txt
# - investment_guide.txt
# (hoặc thêm các tài liệu của riêng bạn)
```

### 5. Khởi Động Server Backend

**⚠️ QUAN TRỌNG: Bạn PHẢI kích hoạt virtual environment trước!**

#### Cách 1: Từ thư mục gốc dự án (Khuyên dùng)
```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
cd backend
python app.py

# Windows (Command Prompt)
.venv\Scripts\activate.bat
cd backend
python app.py

# macOS/Linux
source .venv/bin/activate
cd backend
python app.py
```

#### Cách 2: Chạy trực tiếp từ gốc dự án (không cần activate)
```bash
# Windows
.\.venv\Scripts\python.exe backend/app.py

# macOS/Linux
.venv/bin/python backend/app.py
```

Server sẽ chạy trên: **http://localhost:5000**

### 6. Khởi Động Server Frontend (Terminal Mới)

Mở **terminal mới** và chạy:

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
cd frontend
python -m http.server 8000

# Windows (Command Prompt)
.venv\Scripts\activate.bat
cd frontend
python -m http.server 8000

# macOS/Linux
source .venv/bin/activate
cd frontend
python -m http.server 8000
```

Frontend sẽ chạy trên: **http://localhost:8000**

## 📚 Quản Lý Cơ Sở Dữ Liệu

### Tạo lại Knowledge Base

```bash
# Thông qua API
curl -X POST http://localhost:5000/api/init-knowledge-base

# Hoặc từ giao diện:
# 1. Vào mục "Cơ sở dữ liệu"
# 2. Click "Tạo lại từ Tài liệu"
```

### Tải Knowledge Base có sẵn

```bash
# Thông qua API
curl -X POST http://localhost:5000/api/load-knowledge-base

# Hoặc từ giao diện:
# 1. Vào mục "Cơ sở dữ liệu"
# 2. Click "Tải Cơ sở Dữ liệu"
```

## 🤖 API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /api/chat
Content-Type: application/json

{
  "message": "Giá nhà ở Hà Nội hiện bao nhiêu?",
  "conversation_id": "chat_123",
  "context_count": 5
}

Response:
{
  "success": true,
  "response": "...",
  "context_used": 3,
  "sources": [...]
}
```

### Search Knowledge Base
```
POST /api/search
Content-Type: application/json

{
  "query": "định giá bất động sản",
  "k": 5
}

Response:
{
  "success": true,
  "results": [...],
  "count": 5
}
```

### Initialize Knowledge Base
```
POST /api/init-knowledge-base
```

### Load Knowledge Base
```
POST /api/load-knowledge-base
```

### Get Knowledge Base Info
```
GET /api/knowledge-base-info

Response:
{
  "documents_count": 150,
  "has_index": true,
  "embeddings_model": "sentence-transformers/all-MiniLM-L6-v2",
  "llm_model": "gpt-3.5-turbo"
}
```

### Clear Conversation
```
POST /api/clear-conversation
Content-Type: application/json

{
  "conversation_id": "chat_123"
}
```

## 🔧 Cấu Hình

### backend/config.py

| Tham số | Giải thích | Mặc định |
|---------|-----------|---------|
| FLASK_ENV | Môi trường (development/production) | development |
| PORT | Cổng chạy server | 5000 |
| OPENAI_API_KEY | API key từ OpenAI | - |
| OPENAI_MODEL | Model LLM cần sử dụng | gpt-3.5-turbo |
| EMBEDDINGS_MODEL | Model tạo embedding | sentence-transformers/all-MiniLM-L6-v2 |
| MAX_CONTEXT_LENGTH | Độ dài tối đa ngữ cảnh | 4000 |
| TEMPERATURE | Độ "sáng tạo" của LLM (0-2) | 0.7 |

## 📖 Thêm Tài Liệu Mới

### Định dạng hỗ trợ

1. **Text (.txt)**
   ```
   Đơn giản copy-paste nội dung vào file .txt
   ```

2. **JSON (.json)**
   ```json
   [
     {
       "content": "Nội dung tài liệu",
       "metadata": {
         "source": "Tên nguồn",
         "category": "Danh mục"
       }
     }
   ]
   ```

3. **PDF (.pdf)**
   - Tự động trích xuất text từ PDF

4. **Word (.docx)**
   - Tự động trích xuất text từ Word

### Cách thêm tài liệu

1. Đặt tài liệu vào thư mục `datasets/`
2. Vào giao diện → "Cơ sở dữ liệu" → "Tạo lại từ Tài liệu"
3. Hoặc gọi API: `POST /api/init-knowledge-base`

## 🔐 Bảo Mật

- **API Key**: Không commit `.env` vào git, sử dụng `.env.example` làm template
- **CORS**: Hiện tại cho phép tất cả origins, tùy chỉnh trong `app.py` nếu cần
- **Rate Limiting**: Cân nhắc thêm rate limiting cho production

## 🐛 Khắc Phục Sự Cố

### Lỗi "OpenAI API Key not found"
- Kiểm tra file `.env` có chứa `OPENAI_API_KEY`
- Xác nhận API key hợp lệ

### Lỗi "No documents found"
- Kiểm tra thư mục `datasets/` có chứa tài liệu
- Kiểm tra định dạng file hỗ trợ

### Lỗi Connection từ Frontend
- Kiểm tra backend server đang chạy
- Kiểm tra `backendUrl` trong settings khớp với port backend

### Lỗi CORS
- Kiểm tra frontend được phục vụ từ đúng origin
- Tùy chỉnh CORS policy trong `app.py`

## 📈 Nâng Cấp & Mở Rộng

### Model LLM khác
- Thay đổi `OPENAI_MODEL` sang `gpt-4` hoặc model khác
- Hoặc tích hợp LLM local (Ollama, LLaMA, v.v.)

### Vector Database khác
- Thay thế FAISS bằng Pinecone, Weaviate, Milvus, v.v.

### Database lưu trữ
- Thêm MongoDB/PostgreSQL để lưu conversation history

### Xác thực người dùng
- Thêm JWT authentication
- Tích hợp OAuth

## 📊 Thống Kê & Monitoring

- Thêm logging cho tất cả requests
- Theo dõi token usage OpenAI
- Theo dõi search performance

## 🤝 Đóng Góp

Các suggestion và issues có thể được gửi qua GitHub Issues.

## 📄 License

MIT License - Xem FILE LICENSE để biết chi tiết

## 👨‍💼 Hỗ Trợ

Cho các câu hỏi hoặc hỗ trợ, vui lòng liên hệ:
- Email: support@realestate-chatbox.com
- Website: https://realestate-chatbox.com

---

**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: 2025-01-06
