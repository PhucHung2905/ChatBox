# 📊 Nguồn Dữ Liệu Bất Động Sản

Hướng dẫn chi tiết các nguồn dữ liệu và cách tích hợp vào chatbox.

## 🌐 Công Khai & Miễn Phí

### 1. Dữ Liệu Quốc Gia
- **Tổng Cục Thống Kê (GSO)**: https://www.gso.gov.vn
  - Dữ liệu kinh tế vĩ mô, giá cả
  - Tâm ly dân cư, khu vực
  
- **Bộ Xây Dựng**: https://www.moc.gov.vn
  - Quy định xây dựng
  - Tiêu chuẩn BĐS
  - Luật pháp bất động sản

### 2. Dữ Liệu Dự Án
- **Hiepxaydung.vn**: https://www.hiepxaydung.vn
  - Danh sách dự án
  - Tiến độ dự án
  - Thông tin chủ đầu tư

- **Batdongsan.com.vn**: https://batdongsan.com.vn
  - Danh sách tin rao bán
  - Giá thị trường
  - Dự án phát triển

- **Nhadat.com.vn**: https://nhadat.com.vn
  - Tin tức bất động sản
  - Giá tham khảo
  - Phân tích thị trường

### 3. Dữ Liệu Pháp Lý
- **Thư Viện Luật**: https://thuvienphapluat.vn
  - Văn bản pháp luật
  - Quy định bất động sản
  - Mẫu hợp đồng

- **Cổng TPHCM**: https://hochiminh.gov.vn
  - Quyết định địa phương
  - Quy hoạch
  - Các thông tư, chỉ thị

### 4. Dữ Liệu Giá
- **Ngân Hàng Phát Triển Châu Á (ADB)**: https://www.adb.org
  - Dữ liệu kinh tế khu vực
  - Phân tích bất động sản

- **IMF World Economic Outlook**: https://www.imf.org/en/Publications/WEO
  - Dự báo kinh tế
  - Tỷ giá, lãi suất

## 💰 Trả Phí

### 1. Cơ Sở Dữ Liệu Thương Mại
- **Knight Frank Vietnam**: https://www.knightfrank.com.vn
  - Market Report hàng quý
  - Dữ liệu giá chi tiết
  - Phân tích xu hướng

- **Savills Vietnam**: https://www.savills.com.vn
  - Báo cáo thị trường
  - Dữ liệu giao dịch
  - Dự báo

- **CBRE Vietnam**: https://www.cbre.com.vn
  - Market insights
  - Investment advisory
  - Transaction database

### 2. API Dữ Liệu
- **BĐS API (Batdongsan.com.vn)**
  - Cần đăng ký API key
  - Giới hạn request hàng ngày
  - Trả phí tùy theo package

- **ZingScore**: https://zingscore.com
  - Dữ liệu bất động sản lịch sử
  - API có sẵn
  - Trả phí

## 📥 Cách Tích Hợp Dữ Liệu

### Bước 1: Thu Thập Dữ Liệu
```bash
# Ví dụ: Tải dữ liệu từ API
curl https://api.example.com/properties?token=YOUR_TOKEN > data.json

# Hoặc: Sao chép nội dung từ website
# Copy dữ liệu từ bảng → Paste vào file
```

### Bước 2: Chuẩn Hóa Định Dạng
```json
[
  {
    "content": "Nội dung tài liệu hoàn chỉnh",
    "metadata": {
      "source": "Tên nguồn",
      "type": "dự án/giá/pháp lý",
      "date": "2025-01-06",
      "region": "Hà Nội",
      "category": "Residential/Commercial"
    }
  }
]
```

### Bước 3: Đặt vào `datasets/`
```
datasets/
├── api_data_2025.json
├── market_analysis.txt
├── legal_docs.pdf
└── projects_list.xlsx (convert to json/txt)
```

### Bước 4: Tạo Lại Knowledge Base
```bash
# Vào giao diện chatbox
# Click "Cơ sở dữ liệu" → "Tạo lại từ Tài liệu"

# Hoặc qua API
curl -X POST http://localhost:5000/api/init-knowledge-base
```

## 🔄 Cập Nhật Dữ Liệu Định Kỳ

### Script Python Tự Động
```python
# auto_update.py
import requests
import json
from datetime import datetime

def fetch_market_data():
    """Fetch data từ API"""
    url = "https://api.example.com/properties"
    response = requests.get(url, headers={"Authorization": "Bearer TOKEN"})
    data = response.json()
    
    # Lưu với timestamp
    filename = f"datasets/market_data_{datetime.now().date()}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Data saved to {filename}")

def reinit_kb():
    """Tạo lại knowledge base"""
    response = requests.post("http://localhost:5000/api/init-knowledge-base")
    print(response.json())

if __name__ == "__main__":
    fetch_market_data()
    reinit_kb()
```

### Chạy Script Định Kỳ
```bash
# Windows - Task Scheduler
# Tạo task chạy auto_update.py hàng ngày lúc 2:00 AM

# Linux/Mac - Cron Job
# Thêm vào crontab:
0 2 * * * cd /path/to/project && python auto_update.py
```

## 📊 Các Loại Dữ Liệu Cần Thiết

### 1. Dữ Liệu Dự Án (Projects)
```json
{
  "name": "Tên dự án",
  "location": "Vị trí",
  "developer": "Chủ đầu tư",
  "type": "Residential/Commercial/Mixed",
  "price_range": "Khoảng giá",
  "status": "Planning/Construction/Completed",
  "amenities": ["Tiện ích"],
  "description": "Mô tả chi tiết"
}
```

### 2. Dữ Liệu Giá (Pricing)
```json
{
  "region": "Khu vực",
  "district": "Quận/Huyện",
  "property_type": "Loại BĐS",
  "avg_price": "Giá trung bình",
  "price_range": "Khoảng giá",
  "price_per_sqm": "Giá/m²",
  "date": "Ngày cập nhật",
  "trend": "Tăng/Giảm/Ổn định"
}
```

### 3. Dữ Liệu Pháp Lý (Legal)
```json
{
  "title": "Tiêu đề quy định",
  "content": "Nội dung đầy đủ",
  "effective_date": "Ngày có hiệu lực",
  "document_type": "Luật/Quy định/Thông tư",
  "issuer": "Cơ quan phát hành",
  "status": "Hiệu lực/Bãi bỏ"
}
```

### 4. Dữ Liệu Giao Dịch (Transactions)
```json
{
  "property_type": "Loại BĐS",
  "area_size": "Diện tích",
  "transaction_price": "Giá giao dịch",
  "price_per_sqm": "Giá/m²",
  "district": "Quận/Huyện",
  "date": "Ngày giao dịch",
  "trend": "Xu hướng"
}
```

## ⚠️ Quy Định Pháp Lý

### Sử Dụng Dữ Liệu An Toàn
- ✅ Dữ liệu công khai từ chính phủ
- ✅ Dữ liệu có giấy phép sử dụng
- ✅ Dữ liệu tự thu thập, khảo sát
- ❌ Dữ liệu bản quyền mà chưa được cấp phép
- ❌ Dữ liệu cá nhân không được công khai
- ❌ Dữ liệu vi phạm quyền riêng tư

### Ghi Nguồn Dữ Liệu
Luôn ghi rõ:
```
Nguồn: [Tên Tổ Chức]
Link: [URL nếu có]
Ngày cập nhật: [Ngày]
Giấy phép: [CC-BY, Public Domain, v.v.]
```

## 🎯 Ưu Tiên Dữ Liệu

### Cao (Ưu Tiên Tích Hợp Ngay)
1. Quy định pháp lý mới nhất
2. Dữ liệu giá thị trường hiện tại
3. Dự án phát triển mới
4. Hướng dẫn định giá

### Trung Bình
5. Lịch sử giao dịch 3-6 tháng qua
6. Phân tích thị trường
7. Thông tin tiện ích khu vực

### Thấp
8. Dữ liệu lịch sử > 1 năm
9. Thống kê quốc gia
10. Tài liệu tham khảo lịch sử

## 📈 Cải Thiện Chất Lượng Dữ Liệu

### Làm Sạch Dữ Liệu
```python
import pandas as pd
import re

def clean_data(df):
    # Loại bỏ dòng trống
    df = df.dropna()
    
    # Chuẩn hóa giá
    df['price'] = df['price'].str.replace('[,.]', '', regex=True)
    
    # Chuẩn hóa địa chỉ
    df['address'] = df['address'].str.strip().str.title()
    
    return df

# Sử dụng
df = pd.read_csv('raw_data.csv')
df_clean = clean_data(df)
df_clean.to_json('datasets/cleaned_data.json', orient='records')
```

### Xác Thực Dữ Liệu
```python
def validate_data(item):
    """Kiểm tra dữ liệu hợp lệ"""
    required_fields = ['content', 'metadata']
    
    for field in required_fields:
        if field not in item:
            return False
    
    # Kiểm tra content không trống
    if not item['content'].strip():
        return False
    
    # Kiểm tra metadata có key tối thiểu
    if 'source' not in item['metadata']:
        return False
    
    return True
```

## 🚀 Tích Hợp Tự Động

### Webhook Integration
```python
@app.route('/webhook/market-update', methods=['POST'])
def webhook_market_update():
    """Nhận dữ liệu cập nhật từ webhook"""
    data = request.json
    
    # Lưu dữ liệu
    with open('datasets/webhook_update.json', 'a') as f:
        f.write(json.dumps(data) + '\n')
    
    # Tạo lại KB
    # os.system('python update_kb.py')
    
    return jsonify({'status': 'received'})
```

## 📚 Tài Liệu Tham Khảo

- Hướng dẫn API BĐS: https://batdongsan.com.vn/api-docs
- Python Data Analysis: https://pandas.pydata.org
- Luật bất động sản VN: https://thuvienphapluat.vn/searched/bat+dong+san

---

**Cập nhật**: 2025-01-06  
**Version**: 1.0
