# DV-ClassPro-FinalProject
*Dự án cuối khóa về trực quan hóa dữ liệu - HCMUS - Tháng 11 năm 2024.*
---
## Hướng dẫn nhanh
1. Cài đặt thư viện kaggle: `pip install kaggle`.
2. Nhận Mã thông báo API kaggle để sử dụng trong bước thu thập dữ liệu.

2.1 *Đăng nhập vào Kaggle*:

- Truy cập trang chủ [Kaggle](https://www.kaggle.com/) và đăng nhập vào tài khoản của bạn.

2.2 *Tải xuống Mã thông báo API*:

- Nhấp vào ảnh hồ sơ của bạn ở góc trên bên phải và chọn **"Tài khoản của tôi"**.

- Cuộn xuống phần **"API"**, sau đó nhấp vào nút **"Tạo Mã thông báo API mới"**.

- Tệp có tên `kaggle.json` sẽ được tải xuống. Tệp này chứa thông tin xác thực (tên người dùng và khóa API).

2.3 *Đặt `kaggle.json` vào đúng vị trí*:
- **Linux/MacOS**:
- Tạo một thư mục ẩn `.kaggle` trong thư mục gốc của bạn (nếu nó chưa tồn tại):
```bash
mkdir ~/.kaggle
```
- Di chuyển tệp `kaggle.json` vào thư mục `.kaggle`:
```bash
mv /path/to/kaggle.json ~/.kaggle/
```
- Đặt quyền cho tệp:
```bash
chmod 600 ~/.kaggle/kaggle.json
```
- **Windows**:
- Di chuyển tệp `kaggle.json` vào thư mục:
```
C:\Users\<YourUsername>\.kaggle\kaggle.json
```
- Nếu Thư mục `.kaggle` không tồn tại, hãy tạo thủ công.
3. Chạy Data Collection: `Source\DataCollection\DataCollection.ipynb`
4. Chạy Data Preprocessing: `Source\DataPreProcessing\DataPreprocessing.ipynb`
5. Chạy Data Exploration:\
5.1 `Source\DataExploration\DataExploration_01.ipynb`\
5.2 `Source\DataExploration\DataExploration_02.ipynb`\
5.3 `Source\DataExploration\DataExploration_03.ipynb`
7. Chạy Dashboard.\
6.1 `Source\DashboardSource\app.py`

## Giới thiệu về kho lưu trữ:

### **Chính sách làm việc nhóm:**
1. Chính sách Github: Quy tắc khi thực hiện cam kết trên git.
2. Chính sách đặt tên: Nguyên tắc đặt tên chung cho các dự án.
### **Thư mục Dataset:**
1. google.csv: Tải xuống tập dữ liệu đầu tiên.
2. google_processed.csv: Tập dữ liệu sau khi xử lý trước sẽ được sử dụng cho các bước tiếp theo.
### **Thư mục yêu cầu:**
Các yêu cầu cần triển khai trong dự án này.
### **Thư mục nguồn:**
1. Libraries: Đây là các thư viện thường được sử dụng cho các tác vụ trong quy trình.
2. Shared_Functions: Các hàm được chia sẻ bởi toàn bộ quy trình, chẳng hạn như đọc, ghi, lấy đường dẫn, v.v.
3. Thư mục DataCollection&PreProcessing:
3.1 Thu thập dữ liệu: Thực hiện các bước tải tập dữ liệu xuống thiết bị của bạn.
3.2 Tiền xử lý dữ liệu: Thực hiện các tác vụ tiền xử lý như kiểm tra giá trị bị thiếu, kiểm tra tính chính xác của dữ liệu,...
4. Thư mục Data Exploration:
4.1 DataExploration_01.ipynb - Mục 01.
4.2 DataExploration_02.ipynb - Mục 02.
4.3 DataExploration_03.ipynb - Mục 03.
5. Bảng điều khiển:
5.1 ...
6. Nguồn AI:
6.1 ...
