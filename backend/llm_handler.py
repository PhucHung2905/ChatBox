import os
from typing import List, Dict
import requests
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_CONTEXT_LENGTH, TEMPERATURE

class LLMHandler:
    """Handles LLM interactions with Gemini API"""
    
    def __init__(self, model=None):
        self.model = model or GEMINI_MODEL
        self.api_key = GEMINI_API_KEY
        self.use_mock = not self.api_key  # Use mock if no API key
        
        self.system_prompt = """BẠN LÀ TRỢ LÝ TƯ VẤN SỨC KHỎE CHUYÊN NGHIỆP 🏥

📌 THÔNG TIN:
• Vai trò: Trợ lý tư vấn sức khỏe hàng ngày
• Lĩnh vực: Dinh dưỡng, tập thể dục, phòng chống bệnh, sức khỏe tinh thần
• Lưu ý: KHÔNG phải thay thế bác sĩ - chỉ cung cấp thông tin tham khảo

═══════════════════════════════════════════════════════════
⭐ ĐỊNH DẠNG TRÌNH BÀY BẮT BUỘC (PHẢI LÀM THEO 100%)
═══════════════════════════════════════════════════════════

✅ CÁCH ĐỊNH DẠNG ĐÚNG:

1️⃣ LUÔN bắt đầu với TIÊU ĐỀ CHÍNH:
   🏥 **SỨC KHỎE - [CHỦ ĐỀ]**
   (Với emoji thích hợp và **in đậm**)

2️⃣ SAU ĐÓ chia thành CÁC SECTION với FORMAT:
   💪 **TIÊU ĐỀ SECTION**
   ─────────────────────────────────────────
   • Mục 1: Chi tiết
     - Chi tiết con
     - Chi tiết con
   • Mục 2: Thông tin khác

3️⃣ CÁC QIUY TẮC BẮT BUỘC:
   ✓ Mỗi section phải có emoji (💪, 🍎, 😊, ⚠️, 🏃, ✅, etc.)
   ✓ Tiêu đề section PHẢI in đậm: **TEXT**
   ✓ Dùng dòng gạch ngang phân chia sections: ─────────────────
   ✓ Bullet points (•) cho danh sách không thứ tự
   ✓ Numbered list (1. 2. 3.) cho danh sách có thứ tự
   ✓ Sub-items dùng dấu gạch (-) hoặc 2 khoảng trắng indent
   ✓ Thông tin QUAN TRỌNG in đậm: **text**
   ✓ Cảnh báo và mẹo khỏe mạnh phải in đậm
   ✓ KHÔNG viết paragraph dài liên lạc - chia thành bullet points
   ✓ LUÔN kết thúc bằng: "⚠️ **Lưu ý**: Đây là thông tin tham khảo. Hãy tư vấn bác sĩ khi cần."

VÍ DỤ CỤ THỀ PHẢI LÀM GIỐNG HỆT:

🏥 **SỨC KHỎE - DINH DƯỠNG CƠSMEAN**
═══════════════════════════════════════════════════════════

🍎 **THỰC PHẨM TỐITRONGMỖI NGÀY**
─────────────────────────────────────────
• Rau quả: **5 phần/ngày** (đủ màu sắc)
  - Rau lá xanh (salad, rau muống)
  - Trái cây tươi (cam, táo, chuối)
• Protein: **50-60g/ngày**
  - Cá, gà, thịt nạc
  - Trứng, sữa, sản phẩm từ sữa
  - Đậu, hạt
• Ngũ cốc nguyên hạt: **150g/ngày**
  - Cơm gạo lứt, bánh mì lúa mạch

💪 **LỢI ÍCH CỦA DINH DƯỠNG TỐT**
─────────────────────────────────────────
• Năng lượng **dồi dào** (sáng suốt, không buồn ngủ)
• Hệ miễn dịch **mạnh mẽ** (ít bệnh tật)
• Cân nặng **cân bằng** (không quá cân hoặc thiếu cân)
• Làn da **sáng khỏe** (tóc móng chắc khỏe)

⚠️ **TRÁNH CÁC LOẠI**:
• Đường tinh luyện: **ít hơn 25-36g/ngày**
• Muối: **ít hơn 5g/ngày**
• Chất béo bão hòa: **ít hơn 10% tổng calo**

⚠️ **Lưu ý**: Đây là thông tin tham khảo. Hãy tư vấn bác sĩ hoặc chuyên gia dinh dưỡng cho kế hoạch ăn uống cá nhân.

════════════════════════════════════════════════════════════

⚠️ TUYỆT ĐỐI KHÔNG được:
✗ Viết dạng paragraph dài liên lạc
✗ Quên emoji đầu section
✗ Quên dòng gạch ngang phân chia
✗ Không in đậm thông tin quan trọng
✗ Quên lưu ý về tư vấn bác sĩ ở cuối
✗ Chẩn đoán bệnh (chỉ mô tả triệu chứng)
✗ Sử dụng HTML tags - chỉ dùng Markdown
✗ Viết quá dài trên 1 dòng - chia nhỏ thành bullet points"""
    
    def generate_response(self, user_message: str, context_docs: List[Dict], 
                         conversation_history: List[Dict]) -> str:
        """
        Generate a response using the LLM with context
        Args:
            user_message: The user's question
            context_docs: Relevant documents from knowledge base
            conversation_history: Previous conversation messages
        Returns:
            Generated response text
        """
        
        # Use mock response if no API key
        if self.use_mock:
            return self._generate_mock_response(user_message, context_docs)
        
        # Prepare context from documents
        context = self._prepare_context(context_docs)
        
        # Build messages for the API
        messages = []
        
        # Add conversation history (limit to last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # Build a single prompt string for Gemini
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages]) if messages else ""
        prompt_parts = [self.system_prompt]
        
        # Add strict formatting instruction
        prompt_parts.append("""
════════════════════════════════════════════════════════════
🔴 HƯỚNG DẪN TRÌNH BÀY RESPONSE (BẮT BUỘC 100%):
════════════════════════════════════════════════════════════

1️⃣ TIÊU ĐỀ CHÍNH (ngay dòng đầu):
   Emoji + **HEALTH - [TÊN CỤ THỂ]**

2️⃣ PHÂN CHIA SECTIONS với format:
   Emoji + **TIÊU ĐỀ**
   ─────────────────────
   • Chi tiết 1
   • Chi tiết 2

3️⃣ LUÔN LUÔN dùng Markdown:
   ✓ **Bold**: **text**
   ✓ Bullet: • hoặc -
   ✓ Số thứ tự: 1. 2. 3.
   ✓ Sub-items: thêm 2 spaces
   ✓ Line break: ────────

4️⃣ MỤC LỤC THÔNG TIN PHẢI CÓ:
   ✓ Tiêu đề sản phẩm/dịch vụ
   ✓ Giá cả (in đậm)
   ✓ Lợi ích/tính năng
   ✓ Bảo hành
   ✓ Liên hệ: 0398416377 (in đậm)

⚠️ TUYỆT ĐỐI CẤM:
   ✗ Viết paragraph dài liên tục
   ✗ Quên emoji hoặc dòng gạch
   ✗ Không in đậm số/giá/SĐT
   ✗ Không nhắc Ngân Long Solar
════════════════════════════════════════════════════════════
""")
        
        if context:
            prompt_parts.append(f"📚 Thông tin tham khảo:\n{context}")
        if history_text:
            prompt_parts.append(f"💬 Ngữ cảnh hội thoại:\n{history_text}")
        prompt_parts.append(f"❓ Câu hỏi: {user_message}")
        prompt_text = "\n\n".join(prompt_parts)

        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt_text}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": TEMPERATURE,
                    "maxOutputTokens": 3000
                }
            }

            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}",
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return f"Xin lỗi, tôi gặp lỗi khi xử lý câu hỏi của bạn: {str(e)}"
    
    
    def _generate_mock_response(self, user_message: str, context_docs: List[Dict]) -> str:
        """Generate a formatted mock response for demo purposes"""
        
        # Simple keyword-based mock responses matching health domain
        responses = {
            "sốt": """🏥 **SỨC KHỎE - CAM CÚM VÀ SỐT**
═════════════════════════════════════════════════════════
💡 **Sốt là gì?**
• Nhiệt độ cơ thể tăng trên **37.5°C**
• Là phản ứng miễn dịch của cơ thể chống lại nhiễm trùng

🌡️ **NGUYÊN NHÂN PHỔ BIẾN**
─────────────────────────────────────────
• Cảm cúm, cảm lạnh
• Viêm họng, viêm phế quản
• Viêm tai, viêm xoang
• Nhiễm trùng đường tiểu
• Bệnh khác (phải khám bác sĩ)

💪 **LÀM GÌ ĐỂ GIẢM SỐT?**
─────────────────────────────────────────
1. Uống nước ấm (gừng, mật ong, nước chanh)
2. Nghỉ ngơi đủ (không hoạt động nặng)
3. Dùng thuốc hạ sốt (Paracetamol, Ibuprofen)
   - Tuân thủ liều lượng trên hộp
   - Uống sau khi ăn
4. Mặc quần áo mỏng nhẹ
5. Nén mặt, nách, bẹn bằng nước ấm
6. Tránh tự chẩn đoán

⚠️ **KHI NÀO GẶP BÁC SĨ?**
─────────────────────────────────────────
• Sốt cao trên **39°C** kéo dài
• Sốt kèm theo những triệu chứng nghiêm trọng
• Sốt ở trẻ em hoặc người lớn tuổi
• Sốt không hạ sau 3-4 ngày dùng thuốc

⚠️ **Lưu ý**: Đây là thông tin tham khảo. Hãy tư vấn bác sĩ khi sốt kéo dài.""",

            "dinh dưỡng": """🏥 **SỨC KHỎE - DINH DƯỠNG CÂN BẰNG**
═════════════════════════════════════════════════════════
🍎 **THỰC PHẨM CẦN CÓ HÀNG NGÀY**
─────────────────────────────────────────
1. Rau quả: **5 phần/ngày**
   - Rau lá xanh (cải, cần tây, rau muống)
   - Trái cây (cam, táo, chuối, dâu)

2. Protein: **50-60g/ngày**
   - Cá (cá hồi, cá tuyết) - 2-3 lần/tuần
   - Gà, thịt nạc
   - Trứng - 3-4 quả/tuần
   - Đậu, hạt, sữa

3. Ngũ cốc nguyên hạt: **150g/ngày**
   - Cơm gạo lứt
   - Bánh mì lúa mạch
   - Yến mạch

4. Sữa & Sản phẩm: **2-3 phần/ngày**
   - Sữa tươi, sữa chua
   - Phô mai (ít muối)

💪 **LỢI ÍCH CỦA DINH DƯỠNG TỐT**
─────────────────────────────────────────
• **Năng lượng** dồi dào suốt ngày
• **Miễn dịch** mạnh mẽ, ít bệnh tật
• **Cân nặng** cân bằng
• **Làn da** sáng khỏe, tóc móng chắc
• **Não bộ** tỉnh táo, tập trung tốt

⚠️ **TRÁNH**
─────────────────────────────────────────
• Đường: **ít hơn 25-36g/ngày**
• Muối: **ít hơn 5g/ngày**
• Chất béo bão hòa: **ít hơn 10% tổng calo**
• Thực phẩm chế biến (chip, bánh kẹo)
• Nước ngọt có đường

⚠️ **Lưu ý**: Hãy tư vấn chuyên gia dinh dưỡng cho kế hoạch ăn uống riêng.""",

            "tập thể dục": """🏥 **SỨC KHỎE - HOẠT ĐỘNG THỂ CHẤT**
═════════════════════════════════════════════════════════
💪 **LỢI ÍCH CỦA TẬP THỂ DỤC**
─────────────────────────────────────────
• Sức khỏe tim mạch: Giảm nguy cơ bệnh tim
• Cân nặng: Đốt calorico, giảm béo phì
• Xương & khớp: Chắc khỏe, tránh loãng xương
• Tâm lý: Giảm stress, chống trầm cảm
• Tuổi thọ: Tăng tuổi thọ và chất lượng sống

🏃 **HƯỚNG DẪN TẬP THỂ DỤC**
─────────────────────────────────────────
1. Vận động vừa phải: **150 phút/tuần**
   - Đi bộ nhanh, chạy nhẹ, bơi
   - 30 phút/ngày × 5 ngày/tuần

2. Vận động mạnh: **75 phút/tuần**
   - Chạy bộ, bóng đá, tennis
   - 15-20 phút/ngày × 4 ngày/tuần

3. Sức đề kháng: **2 lần/tuần**
   - Tạ, yoga, pilates
   - Các bài tập cơ

🎯 **CÁCH BẮT ĐẦU**
─────────────────────────────────────────
1. Chọn môn sport bạn yêu thích
2. Bắt đầu từ từ (không quá nặng)
3. Tăng cường độ dần dần
4. Tập với bạn bè (tăng động lực)
5. Đảm bảo ăn, ngủ, nghỉ ngơi đủ

⚠️ **AN TOÀN**
─────────────────────────────────────────
• Warm-up 5-10 phút trước tập
• Cool-down 5-10 phút sau tập
• Nghe lời cơ thể, dừng nếu đau
• Uống nước đủ trước, trong, sau tập
• Tìm bác sĩ nếu cảm thấy không khỏe

⚠️ **Lưu ý**: Hãy tư vấn bác sĩ trước khi bắt đầu chương trình tập luyện.""",

            "stress": """🏥 **SỨC KHỎE - QUẢN LÝ STRESS & LO ÂU**
═════════════════════════════════════════════════════════
😟 **DẤU HIỆU STRESS**
─────────────────────────────────────────
• Thể chất: Đau đầu, mất ngủ, mệt mỏi
• Cảm xúc: Lo lắng, bực bội, cảm giác bất lực
• Hành vi: Ăn uống thay đổi, tránh xã hội

😊 **CÁCH GIẢM STRESS**
─────────────────────────────────────────
1. Thiền & Hít thở sâu: **10-15 phút/ngày**
   - Tìm chỗ yên tĩnh
   - Hít vào 4 giây, giữ 4 giây, thở ra 4 giây
   - Lặp lại 5-10 lần

2. Tập thể dục: **30 phút/ngày**
   - Đi bộ, chạy, yoga
   - Giải phóng endorphin (hormon vui)

3. Sở thích & Vui chơi: **Thường xuyên**
   - Làm việc yêu thích
   - Chơi game, đọc sách
   - Gặp bạn bè, gia đình

4. Ngủ đủ: **7-9 giờ/đêm**
   - Tạo thói quen ngủ
   - Phòng mát, tối, yên tĩnh

5. Dinh dưỡng tốt
   - Ăn cân bằng, tránh caffeine nhiều

6. Nói chuyện & Xin hỗ trợ
   - Chia sẻ cảm xúc với người thân
   - Tư vấn bác sĩ nếu cần

⚠️ **TRÁNH**
─────────────────────────────────────────
• Rượu, thuốc, các chất gây nghiện
• Caffeine quá nhiều
• Làm việc quá sức
• Cô lập xã hội

⚠️ **Lưu ý**: Hãy tư vấn bác sĩ nếu lo âu/stress kéo dài.""",

            "ngủ": """🏥 **SỨC KHỎE - GIẤC NGỦ CÓ CHẤT LƯỢNG**
═════════════════════════════════════════════════════════
😴 **LỢI ÍCH CỦA NGỦ ĐỦJZ**
─────────────────────────────────────────
• Phục hồi: Cơ thể tự sửa chữa, tăng cường miễn dịch
• Tập trung: Bộ nhớ, tư duy, phán đoán tốt hơn
• Cân nặng: Giảm nguy cơ béo phì
• Tâm trạng: Giảm cáu, lo âu, trầm cảm
• Sức khỏe: Giảm bệnh tim, tiểu đường

⏰ **HƯỚNG DẪN NGỦ TỐT**
─────────────────────────────────────────
1. Thời lượng: **7-9 giờ/đêm**
   - Người lớn bình thường
   - Tuổi teen: 8-10 giờ
   - Người lớn tuổi: 7-8 giờ

2. Thời gian cố định
   - Đi ngủ: **22-23 giờ**
   - Thức dậy: **6-7 giờ**
   - (Kể cả cuối tuần)

3. Chuẩn bị phòng
   - Nhiệt độ: **16-19°C** (mát)
   - Độ sáng: **Tối hẳn**
   - Âm thanh: **Yên tĩnh**

4. Thói quen trước ngủ
   - Tắm nước ấm
   - Đọc sách lẫm
   - Thiền, yoga nhẹ
   - Tránh màn hình 1 giờ trước

5. Tránh trước ngủ
   - Caffeine (cà phê, trà đen)
   - Rượu
   - Ăn nặng
   - Tập luyện nặng

⚠️ **Lưu ý**: Hãy tư vấn bác sĩ nếu mất ngủ kéo dài (>2 tuần).""",

            "sức khỏe": """🏥 **TRỢ LÝ TƯ VẤN SỨC KHỎE**
═════════════════════════════════════════════════════════
Xin chào! Tôi là trợ lý tư vấn sức khỏe hàng ngày. 💪

💡 **Tôi có thể giúp bạn về**:
• 🍎 Dinh dưỡng & chế độ ăn uống
• 💪 Tập thể dục & hoạt động thể chất
• 😊 Quản lý stress & sức khỏe tinh thần
• 😴 Giấc ngủ & phục hồi
• 🏥 Phòng chống bệnh & vệ sinh
• ⚠️ Triệu chứng & lời khuyên sơ cứu
• 💊 Thông tin về sức khỏe chung

❓ **Hãy hỏi cụ thể, ví dụ**:
• "Cách giảm cân an toàn?"
• "Nên tập thể dục như thế nào?"
• "Bị sốt cao phải làm gì?"
• "Ngủ không đủ gây hại gì?"
• "Cách giảm stress hiệu quả?"

⚠️ **NHẮC NHỚ QUAN TRỌNG**:
• Đây là **thông tin tham khảo**
• **KHÔNG thay thế** bác sĩ
• Hãy **khám bác sĩ** khi cần
• **Khẩn cấp** → Gọi cấp cứu (120)

⚠️ **Lưu ý**: Hãy tư vấn bác sĩ cho các vấn đề sức khỏe nghiêm trọng."""
        }
        
        # Find best match
        message_lower = user_message.lower()
        for keyword, response_text in responses.items():
            if keyword in message_lower:
                return response_text
        
        # Default response
        default = """🏥 **TRỢ LÝ TƯ VẤN SỨC KHỎE**
═════════════════════════════════════════════════════════
Xin chào! Tôi là trợ lý tư vấn sức khỏe hàng ngày. 💪

💡 **Tôi có thể giúp bạn về**:
• 🍎 Dinh dưỡng & chế độ ăn uống
• 💪 Tập thể dục & hoạt động thể chất
• 😊 Quản lý stress & sức khỏe tinh thần
• 😴 Giấc ngủ & phục hồi
• 🏥 Phòng chống bệnh & vệ sinh
• ⚠️ Triệu chứng & lời khuyên sơ cứu
• 💊 Thông tin về sức khỏe chung

❓ **Hãy hỏi cụ thể, ví dụ**:
• "Cách giảm cân an toàn?"
• "Nên tập thể dục như thế nào?"
• "Bị sốt cao phải làm gì?"
• "Ngủ không đủ gây hại gì?"
• "Cách giảm stress hiệu quả?"

⚠️ **NHẮC NHỚ QUAN TRỌNG**:
• Đây là **thông tin tham khảo**
• **KHÔNG thay thế** bác sĩ
• Hãy **khám bác sĩ** khi cần
• **Khẩn cấp** → Gọi cấp cứu (120)

⚠️ **Lưu ý**: Hãy tư vấn bác sĩ cho các vấn đề sức khỏe nghiêm trọng."""
        return default
    
    def _prepare_context(self, context_docs: List[Dict], max_length: int = 2000) -> str:
        """
        Prepare context string from documents
        Args:
            context_docs: List of relevant documents
            max_length: Maximum length of context to include
        Returns:
            Formatted context string
        """
        if not context_docs:
            return ""
        
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(context_docs, 1):
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            source = metadata.get('source', 'Unknown')
            score = doc.get('score', 0)
            
            # Format document
            doc_text = f"\n[Nguồn {i}: {source} (Độ liên quan: {score:.2f})]\n{content}"
            
            if current_length + len(doc_text) <= max_length:
                context_parts.append(doc_text)
                current_length += len(doc_text)
            else:
                break
        
        return "\n---\n".join(context_parts) if context_parts else ""

