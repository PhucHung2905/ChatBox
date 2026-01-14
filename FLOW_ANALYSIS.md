# 📊 PHÂN TÍCH LUỒNG XỬ LÝ HỆ THỐNG CHATBOX

## 🎯 Tổng Quan
Khi người dùng đặt một câu hỏi, hệ thống thực hiện quá trình RAG (Retrieval-Augmented Generation) để tìm kiếm tài liệu liên quan, sau đó sử dụng LLM để sinh ra câu trả lời. Dưới đây là chi tiết từng bước.

---

## 1️⃣ GIAI ĐOẠN FRONTEND - Người Dùng Gửi Câu Hỏi

### 📍 File: `frontend/script.js` - Hàm `sendMessage()` (Dòng 163)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: NGƯỜI DÙNG NHẬP VÀ GỬI CÂUHỎI                      │
└─────────────────────────────────────────────────────────────┘
```

**Quy trình chi tiết:**

| Bước | Mô tả | Code |
|------|-------|------|
| 1.1 | Lấy nội dung từ input | `message = document.getElementById('messageInput').value.trim()` |
| 1.2 | Kiểm tra trống & không đang xử lý | `if (!message \|\| state.isLoading) return` |
| 1.3 | Đặt trạng thái loading | `state.isLoading = true` |
| 1.4 | Vô hiệu hóa nút Send | `document.getElementById('sendBtn').disabled = true` |
| 1.5 | Hiển thị câu hỏi lên UI | `addMessageToChat(message, 'user')` |
| 1.6 | Xóa input field | `document.getElementById('messageInput').value = ''` |

**Dữ liệu gửi đi:**
```json
{
  "message": "Câu hỏi của người dùng",
  "conversation_id": "chat_1234567890"
}
```

**Header request:**
```
POST /api/chat
Content-Type: application/json
Authorization: Bearer {token}
```

---

## 2️⃣ GIAI ĐOẠN BACKEND - Nhận Và Xử Lý Request

### 📍 File: `backend/app.py` - Endpoint `/api/chat` (Dòng 322)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 2: BACKEND NHẬN REQUEST VÀ KIỂM THỰC                   │
└─────────────────────────────────────────────────────────────┘
```

**Quy trình chi tiết:**

| Bước | Mô tả | Xử lý |
|------|-------|-------|
| 2.1 | Decorator kiểm tra đăng nhập | `@require_login` - Xác thực token JWT |
| 2.2 | Lấy thông tin user | `user = get_current_user()` |
| 2.3 | Kiểm tra user hợp lệ | `if not user: return 401` |
| 2.4 | Lấy dữ liệu từ request | `user_message = data.get('message')` |
| 2.5 | Validate dữ liệu | `if not user_message: return 400` |
| 2.6 | Khởi tạo lịch sử hội thoại | `if conversation_id not in conversation_history: ...` |
| 2.7 | Thêm câu hỏi vào history | Append user message với role='user' |

---

## 3️⃣ GIAI ĐOẠN RAG - TÌM KIẾM TÀI LIỆU LIÊN QUAN

### 📍 File: `backend/vector_db.py` - Hàm `search()` (Dòng 45)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 3: VECTOR DATABASE SEARCH (RETRIEVAL)                  │
└─────────────────────────────────────────────────────────────┘
```

**Chi tiết quy trình:**

```
USER MESSAGE (Câu hỏi)
    ↓
[Embedding Model] - sentence-transformers/all-MiniLM-L6-v2
    ↓
VECTOR EMBEDDING (Biến đổi câu hỏi thành vector)
    ↓
FAISS INDEX SEARCH (Tìm kiếm vector tương tự trong database)
    ↓
K SIMILAR DOCUMENTS (Trả về 5 tài liệu gần nhất)
    ↓
RANK & SCORE (Sắp xếp theo điểm tương tự)
```

### 📊 Ví dụ Quá Trình Search:

**Input:** `"Đau lưng dưới phải làm sao?"`

**Xử lý:**
1. Encode câu hỏi thành vector 384 chiều
2. Tìm kiếm trong FAISS index
3. Trả về top 5 documents với điểm tương tự (similarity score)

**Output:**
```python
[
  {
    'content': 'Vật lí trị liệu cho đau lưng dưới...',
    'metadata': {'source': 'physical_therapy.json', 'type': 'json'},
    'score': 0.92  # 92% tương tự
  },
  {
    'content': 'Các bài tập giảm đau lưng...',
    'metadata': {'source': 'health_guide.txt', 'type': 'text'},
    'score': 0.87  # 87% tương tự
  },
  ...
]
```

**Code từ app.py:**
```python
# Dòng 347-348
relevant_docs = vector_db.search(user_message, k=5)
```

---

## 4️⃣ GIAI ĐOẠN LLM - SINH CÂU TRẢ LỜI

### 📍 File: `backend/llm_handler.py` - Hàm `generate_response()` (Dòng 110)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 4: LLM SINH CÂU TRẢ LỜI VỚI CONTEXT                    │
└─────────────────────────────────────────────────────────────┘
```

**Chi tiết quy trình:**

### 🔄 Chuẩn bị dữ liệu (Augmentation):

**4.1 Chuẩn bị Context từ tài liệu:**
```
relevant_docs (5 tài liệu)
    ↓
_prepare_context() - Định dạng context
    ↓
Context string (max 2000 ký tự)
```

**Code từ llm_handler.py (Dòng 473):**
```python
context = self._prepare_context(context_docs)
# Format: [Nguồn 1: file.json (Độ liên quan: 0.92)]
#         Nội dung tài liệu
#         ---
#         [Nguồn 2: file.txt (Độ liên quan: 0.87)]
```

**4.2 Chuẩn bị Conversation History:**
```
conversation_history (toàn bộ cuộc trò chuyện)
    ↓
Lấy 10 message gần nhất
    ↓
Format: "user: Câu hỏi 1"
        "assistant: Câu trả lời 1"
        "user: Câu hỏi 2"
```

**4.3 Xây dựng Prompt cho LLM:**
```
SYSTEM PROMPT (Hướng dẫn vai trò)
    ↓
FORMATTING INSTRUCTIONS (Hướng dẫn định dạng trả lời)
    ↓
CONTEXT (Tài liệu tham khảo từ search)
    ↓
CONVERSATION HISTORY (Ngữ cảnh cuộc trò chuyện)
    ↓
USER QUESTION (Câu hỏi hiện tại)
```

### 🤖 Gọi Gemini API:

**Request đến Google Gemini:**
```json
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent

{
  "contents": [
    {
      "parts": [
        {
          "text": "FULL_PROMPT_TEXT"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 3000
  }
}
```

**Tham số:**
- `temperature`: 0.7 - Độ "sáng tạo" (0 = cố định, 1 = ngẫu nhiên)
- `maxOutputTokens`: 3000 - Giới hạn độ dài response

### ✅ Response từ LLM:

**Output Example:**
```
🏥 **SỨC KHỎE - ĐAU LƯNG DƯỚI**
═════════════════════════════════════

💪 **NGUYÊN NHÂN PHỔ BIẾN**
─────────────────────────────
• Tư thế không tốt
• Cơ lõm yếu
• Quá tải từ tập luyện

🏃 **CÁCH ĐIỀU TRỊ**
─────────────────────────────
1. Plank - 3 set × 30 giây
2. Bird Dog - 3 set × 10 lần
3. Cat-Cow Stretch - 3 set × 8 lần

⚠️ **Lưu ý**: Đây là thông tin tham khảo...
```

---

## 5️⃣ GIAI ĐOẠN LƯU TRỮ - LƯU RESPONSE VÀO DATABASE

### 📍 File: `backend/app.py` - Dòng 355-362

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 5: LƯU DỮ LIỆU VÀO DATABASE                            │
└─────────────────────────────────────────────────────────────┘
```

**Chi tiết:**

| Bước | Xử lý |
|------|-------|
| 5.1 | Thêm response vào conversation_history | `conversation_history[conversation_id].append(...)` |
| 5.2 | Tạo ChatHistory record | `ChatHistory(user_id, conversation_id, message, response, ...)` |
| 5.3 | Lưu sources (tài liệu tham khảo) | `json.dumps([doc metadata])` |
| 5.4 | Commit vào database | `db.session.add()` & `db.session.commit()` |

**Dữ liệu lưu trữ:**
```python
ChatHistory(
    user_id=123,
    conversation_id='chat_1234567890',
    message='Đau lưng dưới phải làm sao?',
    response='🏥 **SỨC KHỎE - ĐAU LƯNG DƯỚI**...',
    context_used=5,  # Số tài liệu sử dụng
    sources='[{"source": "physical_therapy.json", "type": "json"}...]'
)
```

---

## 6️⃣ GIAI ĐOẠN FRONTEND - HIỂN THỊ RESPONSE

### 📍 File: `frontend/script.js` - Hàm `addMessageToChat()` (Dòng 201)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 6: FRONTEND HIỂN THỊ CÂU TRẢ LỜI                       │
└─────────────────────────────────────────────────────────────┘
```

**Chi tiết:**

| Bước | Xử lý |
|------|-------|
| 6.1 | Nhận response từ backend | `const data = await response.json()` |
| 6.2 | Kiểm tra success | `if (data.success)` |
| 6.3 | Parse Markdown | `marked.parse(data.response)` |
| 6.4 | Sanitize HTML (chống XSS) | `DOMPurify.sanitize(htmlContent, {...})` |
| 6.5 | Thêm vào DOM | `messageEl.innerHTML = cleanHTML` |
| 6.6 | Cuộn xuống cuối | `chatMessages.scrollTop = chatMessages.scrollHeight` |
| 6.7 | Hiển thị thông tin context | `📚 Sử dụng 5 tài liệu tham khảo` |
| 6.8 | Tắt loading state | `state.isLoading = false` |

**Kết quả:** Câu trả lời được hiển thị với format đẹp mắt, đã parse Markdown

---

## 📈 SƠ ĐỒ TỔNG THỂ LUỒNG XỬ LÝ

```
┌──────────────────────────────────────────────────────────────────┐
│                      NGƯỜI DÙNG                                   │
│             (Gõ câu hỏi vào input box)                           │
└────────────────────────┬─────────────────────────────────────────┘
                         │ sendMessage()
                         ▼
         ┌──────────────────────────────┐
         │  FRONTEND (script.js)        │
         │  - Validate input            │
         │  - Show loading state        │
         │  - Add user message to UI    │
         └────────────┬─────────────────┘
                      │ POST /api/chat
                      │ {message, conversation_id, token}
                      ▼
         ┌──────────────────────────────┐
         │  BACKEND (app.py)            │
         │  - Verify JWT token          │
         │  - Get user from DB          │
         │  - Add message to history    │
         └────────────┬─────────────────┘
                      │
                      ▼
    ┌────────────────────────────────────┐
    │  VECTOR DATABASE (vector_db.py)    │
    │  - Encode user message to vector   │
    │  - Search FAISS index              │
    │  - Return top 5 similar docs       │
    └────────────┬───────────────────────┘
                 │ [relevant_docs: {content, metadata, score}]
                 ▼
    ┌────────────────────────────────────┐
    │  LLM HANDLER (llm_handler.py)      │
    │  - Prepare context from docs       │
    │  - Build system prompt             │
    │  - Add conversation history        │
    │  - Call Gemini API                 │
    │  - Get formatted response          │
    └────────────┬───────────────────────┘
                 │ response: "🏥 **SỨC KHỎE**..."
                 ▼
    ┌────────────────────────────────────┐
    │  DATABASE (app.py)                 │
    │  - Save chat to ChatHistory        │
    │  - Save sources metadata           │
    │  - Update user stats               │
    └────────────┬───────────────────────┘
                 │ {success: true, response, context_used}
                 ▼
         ┌──────────────────────────────┐
         │  FRONTEND (script.js)        │
         │  - Parse Markdown response   │
         │  - Sanitize HTML             │
         │  - Add to chat display       │
         │  - Show context info         │
         │  - Stop loading state        │
         └────────────┬─────────────────┘
                      │
                      ▼
         ┌──────────────────────────────┐
         │  NGƯỜI DÙNG NHÌN THẤY        │
         │  Câu trả lời được định dạng │
         │  đẹp với Markdown            │
         └──────────────────────────────┘
```

---

## 🔍 CHI TIẾT CỈM TẬT CÁC THÀNH PHẦN

### 📚 Knowledge Base Documents
**Vị trí:** `/datasets/`
- `health_conditions.json` - Bệnh lý sức khỏe
- `health_guide.txt` - Hướng dẫn sức khỏe
- `health_tips.json` - Mẹo sức khỏe
- `physical_therapy.json` - Vật lí trị liệu (mới)

### 🎯 Vector Database
**Loại:** FAISS (Facebook AI Similarity Search)
- **Model:** sentence-transformers/all-MiniLM-L6-v2
- **Chiều:** 384 chiều vector
- **Lưu trữ:** `/vectorstore/`
  - `index.faiss` - FAISS index
  - `documents.json` - Nội dung & metadata

### 🤖 LLM Model
**Nhà cung cấp:** Google Gemini
- **Model:** gemini-1.5-flash
- **Temperature:** 0.7 (cân bằng giữa xác định & sáng tạo)
- **Max tokens:** 3000 ký tự

### 💾 Database Structure
**Model:** ChatHistory
```python
user_id (FK to User)
conversation_id (ID cuộc trò chuyện)
message (Câu hỏi của user)
response (Câu trả lời từ AI)
context_used (Số tài liệu dùng)
sources (JSON metadata của tài liệu)
timestamp (Thời gian)
```

---

## ⚡ HIỆU SUẤT & TỐI ƯU HÓA

### Điểm Mạnh:
✅ **RAG hiệu quả** - Kết hợp retrieval + generation
✅ **Cached conversation** - Lưu history trên memory & DB
✅ **Vector search nhanh** - FAISS indexing
✅ **Multi-format support** - JSON, TXT, PDF, DOCX

### Cần Cải Thiện:
⚠️ **Conversation history trên memory** - Mất khi restart server
⚠️ **FAISS index rebuild** - Cần rebuild khi thêm doc mới
⚠️ **Limited context window** - Max 2000 ký tự cho context
⚠️ **API rate limiting** - Gemini API có giới hạn request

---

## 🔐 BẢO MẬT

| Bước | Bảo mật |
|------|---------|
| Request | JWT token validation (`@require_login`) |
| Frontend | XSS protection (DOMPurify sanitization) |
| Database | User-specific chat history (user_id filter) |
| LLM | Không lưu trữ API key trong frontend |
| Context | Metadata không chứa thông tin nhạy cảm |

---

## 📝 SUMMARY

**Luồng xử lý 6 bước:**
1. 👤 **Frontend** - User gửi câu hỏi
2. 🔐 **Backend** - Validate & lưu vào history
3. 🔍 **Vector DB** - Tìm kiếm tài liệu liên quan (RAG Retrieval)
4. 🤖 **LLM** - Sinh response với context (RAG Augmentation & Generation)
5. 💾 **Database** - Lưu trữ chat history
6. 📱 **Frontend** - Hiển thị response cho user

**Công nghệ chính:**
- **RAG Framework** - Kết hợp retrieval + generation
- **Vector DB** - FAISS + SentenceTransformer
- **LLM** - Google Gemini API
- **Backend** - Flask + SQLAlchemy
- **Frontend** - Vanilla JavaScript + Marked.js + DOMPurify
