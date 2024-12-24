from Libraries import *
from Shared_Functions import *
import pandas as pd
import plotly.graph_objects as go
import json
import pandas as pd


#-------------------- Thực hiện xử lý các hàm dưới này nha mấy ní.
# Dữ liệu mẫu
data = pd.read_csv('Dataset/THPTQG_2022_processed.csv')
#convert to DataFrame
raw_df = pd.DataFrame(data)
# Hàm làm tròn điểm về bội số gần nhất của 0.25
def lam_tron_diem_0_25(diem):
    # Check if diem is NaN
    if np.isnan(diem):
        return diem  # Return NaN as is
    return round(diem / 0.25) * 0.25
def lam_tron_0_5(diem):
        return round(diem * 2) / 2
# Loại bỏ cột 'id'
df = raw_df.drop(columns=['id'])
df['literature_score'] = df['literature_score'].apply(lam_tron_diem_0_25)
#đổi tên các cột về tên môn
df = df.rename(columns={
'mathematics_score': 'Toán',
'literature_score': 'Văn',
'physics_score': 'Vật Lý',
'chemistry_score': 'Hóa Học',
'biology_score': 'Sinh Học',
'english_score': 'Tiếng Anh',
'history_score': 'Lịch Sử',
'geography_score': 'Địa Lý',
'civic_education_score': 'GDCD'
})
# Tính tổng điểm từng khối
df['A00'] = df['Toán'] + df['Vật Lý'] + df['Hóa Học']
df['A01'] = df['Toán'] + df['Vật Lý'] + df['Tiếng Anh']
df['B00'] = df['Toán'] + df['Hóa Học'] + df['Sinh Học']
df['C00'] = df['Văn'] + df['Lịch Sử'] + df['Địa Lý']
df['D00'] = df['Toán'] + df['Văn'] + df['Tiếng Anh']
subjects_for_blocks = {
    'A00': ['Toán', 'Vật Lý', 'Hóa Học'],
    'A01': ['Toán', 'Vật Lý', 'Tiếng Anh'],
    'B00': ['Toán', 'Hóa Học', 'Sinh Học'],
    'C00': ['Văn', 'Lịch Sử', 'Địa Lý'],
    'D00': ['Toán', 'Văn', 'Tiếng Anh']
}
def section_02_01():
    # Giả sử df là DataFrame của bạn đã có các cột 'A00', 'A01', 'B00', 'C00', 'D00'
    histogram_charts = {}
    summary_stats = {}  # Tạo dictionary để lưu thông tin thống kê

    # Các khối điểm
    blocks = ['A00', 'A01', 'B00', 'C00', 'D00']

    for block in blocks:
        # Lấy dữ liệu từng khối điểm và nếu có 1 trong 3 cột có giá trị NaN thì bỏ qua giá trị điểm của học sinh đó
        subjects = subjects_for_blocks[block]
    
        # Lọc các hàng không có giá trị NaN trong bất kỳ môn nào của khối hiện tại
        valid_rows = df.dropna(subset=subjects)

        # Lấy dữ liệu điểm của khối từ các hàng hợp lệ (không có NaN)
        scores = valid_rows[block].apply(lam_tron_0_5)
        
        # Tính các thống kê
        mean_score = scores.mean()
        mean_score = round(mean_score, 3)
        below_1_count = len(scores[scores <= 1])/len(scores)*100
        below_1_count = round(below_1_count, 3)
        median_score = scores.median()
        median_score = round(median_score, 3)
        below_avg_count = len(scores[scores < mean_score])/len(scores)*100
        below_avg_count = round(below_avg_count, 3)
        mode_score = scores.mode()[0] if not scores.mode().empty else None  # Mốc điểm trung bình phổ biến nhất
        mode_score = round(mode_score, 3) if mode_score is not None else None
        above_30_count = len(scores[scores >= 29])
        below_10_count = len(scores[scores < 10])

        # Lưu thông tin thống kê vào summary_stats
        summary_stats[block] = {
            'mean': mean_score,
            'median': median_score,
            'below_1_count': below_1_count,
            'below_avg_count': below_avg_count,
            'mode': mode_score,
            'above_29_count': above_30_count,
            'below_10_count': below_10_count
        }

        # Tính tần số xuất hiện của từng điểm số (cụ thể từ 0.0 đến 30.0 với bước 0.25)
        unique_scores = sorted(scores.unique())  # Lấy các điểm số duy nhất
        score_counts = scores.value_counts().sort_index()

        # Xây dựng histogram
        hist = go.Figure(data=[
            go.Bar(
                x=score_counts.index,  # Trục X là các điểm số
                y=score_counts.values,  # Trục Y là tần số xuất hiện
                marker=dict(
                    color="blue",
                    line=dict(color="white", width=1)  # Viền đậm màu đen
                ),
                text=score_counts.values,  # Hiển thị số liệu trên từng cột
                textposition='outside'  # Đặt số liệu bên ngoài cột
            )
        ])
        # Cập nhật layout cho histogram
        hist.update_layout(
            title=f"Phân bố điểm thi khối {block}",
            xaxis_title="Điểm",
            yaxis_title="Số lượng học sinh",
            xaxis=dict(
                tickmode="array",
                tickvals=unique_scores,  # Hiển thị chính xác từng điểm số
                ticktext=[str(score) for score in unique_scores]
            ),
            bargap=0.05,  # Khoảng cách giữa các cột
            yaxis=dict(range=[0, score_counts.max() * 1.2])  # Mở rộng trục Y
        )

    # Lưu histogram vào dictionary
        histogram_charts[block] = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    # Trả về histogram và thông tin thống kê
    return histogram_charts, summary_stats