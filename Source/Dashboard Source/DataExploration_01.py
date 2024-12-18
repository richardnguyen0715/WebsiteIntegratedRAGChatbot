#-------------------- Thực hiện xử lý các hàm dưới này nha mấy ní.

# def section_01_01():
#     line_chart = go.Figure(data=[
#         go.Scatter(x=["Jan", "Feb", "Mar", "Apr"], y=[10, 15, 13, 17], name="Tickets Created"),
#         go.Scatter(x=["Jan", "Feb", "Mar", "Apr"], y=[8, 12, 11, 14], name="Tickets Solved")
#     ])
#     line_chart_json = json.dumps(line_chart, cls=plotly.utils.PlotlyJSONEncoder)

#     pie_chart = go.Figure(data=[
#         go.Pie(labels=["Setup", "Features", "Fixes"], values=[19, 26, 55])
#     ])
#     pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

#     bar_chart = go.Figure(data=[
#         go.Bar(x=["Mon", "Tue", "Wed", "Thu", "Fri"], y=[5, 10, 15, 20, 25], name="Tickets/Week")
#     ])
#     bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

#     return line_chart_json, pie_chart_json, bar_chart_json
from Libraries import *
from Shared_Functions import *
import pandas as pd
import plotly.graph_objects as go
import json
import pandas as pd

# Dữ liệu mẫu
data = pd.read_csv('Dataset/THPTQG_2022_processed.csv')
# Convert to DataFrame
df = pd.DataFrame(data)
# Hàm làm tròn điểm về bội số gần nhất của 0.25
def lam_tron_diem(diem):
    # Check if diem is NaN
    if np.isnan(diem):
        return diem  # Return NaN as is
    return round(diem / 0.25) * 0.25
# Loại bỏ cột 'id'
df = df.drop(columns=['id'])
df['literature_score'] = df['literature_score'].apply(lam_tron_diem)
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

#-------------------- Thực hiện xử lý các hàm dưới này nha mấy ní.

def section_01_01():
    # 1. Bar Chart: Average Scores by Subject
    averages = df.mean()
    sorted_averages = averages.sort_values()
    bar_avg_chart = go.Figure(data=[
        go.Bar(
            x=sorted_averages.index, 
            y=sorted_averages.values, 
            name='Điểm trung bình',
        )
    ])
    bar_avg_chart.update_layout(
        title="Điểm trung bình của từng môn học",
        xaxis_title="Môn học",
        yaxis_title="Điểm trung bình"
    )
    bar_avg_chart_json = json.dumps(bar_avg_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # 3. Pie Chart: Subject Coverage (Non-Null Counts)
    coverage = df.notnull().sum()
    pie_chart = go.Figure(data=[
        go.Pie(labels=coverage.index, values=coverage.values)
    ])
    pie_chart.update_layout(title="Số lượng học sinh đã thi mỗi môn")
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # 4. Histogram: Distribution of Scores by Subject
    histogram_charts = {}
    summary_stats = {}  # Tạo dictionary để lưu thông tin thống kê

    for column in df.columns:
        # Lấy dữ liệu từng điểm số cụ thể và loại bỏ NaN
        scores = df[column].dropna()
        mean_score = scores.mean()
        below_1_count = len(scores[scores <= 1])
        median_score = scores.median()
        below_avg_count = len(scores[scores < mean_score])
        mode_score = scores.mode()[0] if not scores.mode().empty else None  # Mốc điểm trung bình phổ biến nhất
        
        # Tạo bảng thống kê
        summary_stats[column] = {
            'mean': mean_score,
            'median': median_score,
            'below_1_count': below_1_count,
            'below_avg_count': below_avg_count,
            'mode': mode_score
        }
        # Tính tần số xuất hiện của từng điểm số (cụ thể từ 0.0 đến 10.0 với bước 0.25)
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

        hist.update_layout(
            title=f"Phân bố điểm thi môn {column}",
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

        histogram_charts[column] = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_avg_chart_json, pie_chart_json, histogram_charts, summary_stats