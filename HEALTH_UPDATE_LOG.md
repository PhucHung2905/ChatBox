# Chatbot Tư Vấn Sức Khỏe - Update Lớn ✨

## 📋 Tóm Tắt Thay Đổi

Chatbot đã được **chuyển đổi hoàn toàn** từ tư vấn Solar sang **tư vấn sức khỏe toàn diện**. Đây là một bản nâng cấp lớn với datasets, system prompt, và mock responses hoàn toàn mới.

---

## 🔄 Thay Đổi Lớn

### ❌ Xóa
- ✅ `company_info.json` - Thông tin công ty Solar
- ✅ `investment_guide.txt` - Hướng dẫn đầu tư bất động sản
- ✅ `legal_regulations.txt` - Quy định pháp lý
- ✅ `pricing_guide.txt` - Hướng dẫn giá
- ✅ `real_estate_projects.json` - Các dự án bất động sản

### ✅ Thêm Mới
- 📄 `health_conditions.json` - Các bệnh, triệu chứng, phòng chống
- 📄 `health_guide.txt` - Hướng dẫn sức khỏe toàn diện
- 📄 `health_tips.json` - Mẹo sức khỏe hàng ngày

---

## 📚 Datasets Mới

### 1. **health_conditions.json**
Chứa thông tin chi tiết về các bệnh phổ biến:
- **Cảm Cúm** - Triệu chứng, nguyên nhân, phòng chống, điều trị
- **Cảm Lạnh** - Thông tin tương tự
- **Tiểu Đường** - Loại, nguy cơ, quản lý

```json
{
  "conditions": [
    {
      "id": "flu",
      "name": "Cảm Cúm",
      "symptoms": [...],
      "causes": "...",
      "prevention": [...],
      "treatment": [...]
    }
  ]
}
```

### 2. **health_guide.txt**
Hướng dẫn sức khỏe chi tiết về 8 lĩnh vực:
1. Sức khỏe tim mạch
2. Sức khỏe xương và khớp
3. Sức khỏe cơ sinh
4. Sức khỏe tinh thần
5. Dinh dưỡng cân bằng
6. Hoạt động thể chất
7. Ngủ và phục hồi
8. Phòng chống bệnh

### 3. **health_tips.json**
Mẹo sức khỏe hàng ngày được sắp xếp theo danh mục:
- Sức Khỏe Hàng Ngày
- Dinh Dưỡng
- Tập Thể Dục
- Quản Lý Stress
- Sức Khỏe Tinh Thần
- Phòng Chống Bệnh

---

## 🔧 Cập Nhật Backend

### **llm_handler.py**
```python
# System Prompt mới
- Thay đổi từ "NGÂN LONG SOLAR" → "TRỢ LÝ TƯ VẤN SỨC KHỎE"
- Format vẫn giữ nguyên (emoji, bullet points, bold text)
- Thêm disclaimer: "KHÔNG thay thế bác sĩ"
- Đề nhắc tư vấn bác sĩ cho các vấn đề nghiêm trọng

# Mock Responses
"sốt" → Thông tin về cảm cúm, sốt cao
"dinh dưỡng" → Hướng dẫn ăn uống cân bằng
"tập thể dục" → Cách tập luyện an toàn
"stress" → Quản lý stress & lo âu
"ngủ" → Giấc ngủ có chất lượng
"sức khỏe" → Greeting & intro chung
```

---

## 🎨 Cập Nhật Frontend

### **index.html**
```html
<!-- Cũ -->
<h1>🌞 Ngân Long Solar</h1>
<p>Tư Vấn & Thi Công Hệ Thống Solar</p>

<!-- Mới -->
<h1>🏥 Tư Vấn Sức Khỏe</h1>
<p>Trợ Lý Sức Khỏe Hàng Ngày</p>
```

Placeholder mới:
```html
<!-- Cũ -->
placeholder="Hỏi về bất động sản..."

<!-- Mới -->
placeholder="Hỏi về sức khỏe..."
```

---

## 🎯 Các Từ Khóa Trigger

| Từ Khóa | Response |
|---------|----------|
| sốt | Thông tin cảm cúm & sốt cao |
| dinh dưỡng | Ăn uống cân bằng |
| tập thể dục | Hoạt động thể chất an toàn |
| stress | Quản lý stress & lo âu |
| ngủ | Giấc ngủ có chất lượng |
| sức khỏe | Greeting & intro chung |

---

## 📖 Nội Dung Hỗ Trợ

Chatbot hiện có thể hỗ trợ về:

### 🍎 **Dinh Dưỡng**
- Thực phẩm cần thiết hàng ngày
- Lượng Protein, Carbs, Fat phù hợp
- Loại thực phẩm nên tránh
- Lợi ích của dinh dưỡng tốt

### 💪 **Tập Thể Dục**
- Lợi ích của tập luyện
- Hướng dẫn tập từ từ
- Warm-up & Cool-down
- Cách tránh chấn thương

### 😊 **Sức Khỏe Tinh Thần**
- Giảm stress & lo âu
- Thiền, hít thở sâu
- Duy trì mối quan hệ xã hội
- Khi nào tìm bác sĩ

### 😴 **Giấc Ngủ**
- Giờ ngủ phù hợp
- Cách tạo môi trường ngủ tốt
- Thói quen trước khi ngủ
- Giải quyết mất ngủ

### 🏥 **Phòng Chống Bệnh**
- Triệu chứng & nguyên nhân
- Phòng chống hiệu quả
- Khi nào gặp bác sĩ
- Lời khuyên sơ cứu

---

## ⚠️ Disclaimer Quan Trọng

**Chatbot này KHÔNG thể thay thế bác sĩ**:
- Chỉ cung cấp **thông tin tham khảo**
- Không **chẩn đoán** bệnh
- Không **kê đơn** thuốc
- Hãy **khám bác sĩ** cho vấn đề sức khỏe
- **Khẩn cấp** → Gọi **120**

---

## 🔍 Cách Sử Dụng

### Demo Mode (Không API Key)
```bash
python backend/app.py
```

Các từ khóa trigger response:
- "Bị sốt cao phải làm gì?" → Thông tin về sốt
- "Cách ăn uống lành mạnh?" → Hướng dẫn dinh dưỡng
- "Tập thể dục bao lâu?" → Hướng dẫn tập luyện
- "Bị stress, lo âu?" → Quản lý stress
- "Ngủ không đủ?" → Giấc ngủ tốt

### Với Gemini API (Nếu có API Key)
- System prompt sẽ yêu cầu AI format response theo kiểu sức khỏe
- AI sẽ tự động sinh response đúng format

---

## 📊 Cấu Trúc Response

Tất cả responses đều follow format:

```markdown
🏥 **SỨC KHỎE - [CHỦ ĐỀ]**
═════════════════════════════════════════════════════════

💪 **TIÊU ĐỀ SECTION 1**
─────────────────────────────────────────
• Mục 1
• Mục 2
  - Chi tiết

😊 **TIÊU ĐỀ SECTION 2**
─────────────────────────────────────────
1. Mục 1
2. Mục 2

⚠️ **Lưu ý**: Tư vấn bác sĩ cho vấn đề nghiêm trọng.
```

---

## 🚀 Tiếp Theo (Tùy Chọn)

### Cải Thiện
- [ ] Thêm dữ liệu về bệnh tim mạch, cao huyết áp
- [ ] Thêm thông tin về phòng chống ung thư
- [ ] Hỗ trợ tính BMI, lượng calo tiêu thụ
- [ ] Theo dõi lịch sử sức khỏe người dùng

### Tối Ưu
- [ ] Tích hợp database y tế có thực
- [ ] Hợp tác với bác sĩ để kiểm tra thông tin
- [ ] Thêm multi-language support
- [ ] Cải thiện tìm kiếm bệnh dựa trên triệu chứng

---

## 📝 Ghi Chú

- Tất cả nội dung được tổ chức rõ ràng theo JSON format
- Dễ mở rộng với thêm bệnh, mẹo, hướng dẫn mới
- Format response thống nhất, chuyên nghiệp
- Luôn nhắc tư vấn bác sĩ để đảm bảo an toàn

---

**Cập nhật lần cuối**: 12/01/2026
**Phiên bản**: 3.0.0 (Health Advisory Chatbot)
**Status**: ✅ Sẵn sàng sử dụng
