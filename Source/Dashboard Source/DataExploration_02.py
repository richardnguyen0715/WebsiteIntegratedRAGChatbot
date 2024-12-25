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
        above_29_count = len(scores[scores >= 29])
        below_10_count = len(scores[scores < 10])

        # Lưu thông tin thống kê vào summary_stats
        summary_stats[block] = {
            'mean': mean_score,
            'median': median_score,
            'below_1_count': below_1_count,
            'below_avg_count': below_avg_count,
            'mode': mode_score,
            'above_29_count': above_29_count,
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

def section_02_02(df):
    avg_scores = {}
    for block, subjects in subjects_for_blocks.items():
        avg_scores[block] = df[subjects].mean()

    grouped_bar_charts = {}
    for block, subjects in subjects_for_blocks.items():
        grouped_bar_chart = go.Figure()
        grouped_bar_chart.add_trace(go.Bar(
            x=subjects,
            y=avg_scores[block].values,
            name=block,
            marker=dict(color='rgba(0, 158, 115, 0.8)')
        ))
        grouped_bar_chart.update_layout(
            barmode='group',
            title=f'Biểu đồ cột thể hiện sự chênh lệch điểm của khối {block}',
            xaxis_title='Môn học',
            yaxis_title='Điểm trung bình',
            yaxis=dict(range=[0, 10])
        )
        grouped_bar_charts[block] = json.dumps(grouped_bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return grouped_bar_charts

def section_02_03(df):
    density_plots = {}
    colors = ['rgba(0, 114, 178, 0.8)', 'rgba(213, 94, 0, 0.8)', 'rgba(0, 158, 115, 0.8)']
    for block, subjects in subjects_for_blocks.items():
        density_plot = go.Figure()
        colors = ['blue', 'green', 'red']

        for subject, color in zip(subjects, colors):
            density_plot.add_trace(go.Violin(
                x=df[subject],
                line_color=color,
                name=subject,
                box_visible=True,
                meanline_visible=True
            ))

        density_plot.update_layout(
            title=f'Density Plot for Block {block}',
            xaxis_title='Điểm số',
            yaxis_title='Mật độ',
            violingap=0,
            violingroupgap=0,
            violinmode='overlay'
        )

        density_plots[block] = json.dumps(density_plot, cls=plotly.utils.PlotlyJSONEncoder)

    return density_plots

# filepath: /d:/SINHVIEN/1.study/hk1_nam3/TrucQuanHoaDL/projects/DV-ClassPro-FinalProject/Source/Dashboard Source/DataExploration_02.py
def section_02_04(df):
    pie_charts = {}
    colors = ['rgba(0, 114, 178, 0.8)', 'rgba(213, 94, 0, 0.8)', 'rgba(0, 158, 115, 0.8)']
    for block, subjects in subjects_for_blocks.items():
        scores = df[block]
        below_15 = len(scores[scores < 15])
        between_15_23 = len(scores[(scores >= 15) & (scores <= 23)])
        above_23 = len(scores[scores > 23])

        labels = ['< 15 điểm', '15-23 điểm', '> 23 điểm']
        values = [below_15, between_15_23, above_23]

        pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label', marker=dict(colors=colors))])
        pie_chart.update_layout(
            title=f'Phân bố điểm thi của các học sinh dựa theo các nhóm điểm của khối {block}',
        )

        pie_charts[block] = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return pie_charts

def section_02_05(df):
    horizontal_bar_charts = {}
    colors = {
        '< 15 điểm': 'rgba(0, 114, 178, 0.8)',  # Blue
        '15-23 điểm': 'rgba(230, 159, 0, 0.8)',  # Orange
        '> 23 điểm': 'rgba(86, 180, 233, 0.8)'  # Sky Blue
    }
    for block, subjects in subjects_for_blocks.items():
        scores = df[subjects]
        groups = {
            '< 15 điểm': df[df[block] < 15][subjects],
            '15-23 điểm': df[(df[block] >= 15) & (df[block] <= 23)][subjects],
            '> 23 điểm': df[df[block] > 23][subjects]
        }

        horizontal_bar_chart = go.Figure()
        for group_name, group_scores in groups.items():
            avg_scores = group_scores.mean()
            horizontal_bar_chart.add_trace(go.Bar(
                x=avg_scores,
                y=subjects,
                orientation='h',
                name=group_name, 
                marker=dict(color=colors[group_name])
            ))

        horizontal_bar_chart.update_layout(
            title=f'Điểm trung bình của các môn theo nhóm điểm của khối {block}',
            xaxis_title='Điểm trung bình',
            yaxis_title='Môn học',
            xaxis=dict(range=[0, 10])
        )

        horizontal_bar_charts[block] = json.dumps(horizontal_bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return horizontal_bar_charts

def section_02_06(df):
    natural_subjects = ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học']
    social_subjects = ['Văn', 'Lịch Sử', 'Địa Lý', 'GDCD']

    df['avg_natural'] = df[natural_subjects].mean(axis=1)
    df['avg_social'] = df[social_subjects].mean(axis=1)

    natural_group = df[df['avg_natural'] > df['avg_social'] + 1]
    social_group = df[df['avg_social'] > df['avg_natural'] + 1]
    balanced_group = df[(df['avg_natural'] <= df['avg_social'] + 1) & (df['avg_social'] <= df['avg_natural'] + 1)]

    labels = ['Thiên về tự nhiên', 'Thiên về xã hội', 'Cân bằng']
    values = [len(natural_group), len(social_group), len(balanced_group)]

    colors = ['rgba(0, 114, 178, 0.8)', 'rgba(213, 94, 0, 0.8)', 'rgba(0, 158, 115, 0.8)'] 

    donut_chart = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,  # Tạo lỗ trống ở giữa để thành biểu đồ donut
        textinfo='percent', 
        marker=dict(colors=colors)
    )])
    donut_chart.update_layout(
        title='Phân loại học sinh theo thiên hướng học tập'
    )

    return json.dumps(donut_chart, cls=plotly.utils.PlotlyJSONEncoder)

def section_02_07(df):
    natural_subjects = ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học']
    social_subjects = ['Văn', 'Lịch Sử', 'Địa Lý', 'GDCD']

    df['avg_natural'] = df[natural_subjects].mean(axis=1)
    df['avg_social'] = df[social_subjects].mean(axis=1)

    natural_group = df[df['avg_natural'] > df['avg_social'] + 1]
    social_group = df[df['avg_social'] > df['avg_natural'] + 1]
    balanced_group = df[(df['avg_natural'] <= df['avg_social'] + 1) & (df['avg_social'] <= df['avg_natural'] + 1)]

    blocks = ['A00', 'A01', 'B00', 'C00', 'D00']
    group_labels = ['Thiên về tự nhiên', 'Thiên về xã hội', 'Cân bằng']
    group_data = {
        'Thiên về tự nhiên': [],
        'Thiên về xã hội': [],
        'Cân bằng': []
    }

    for block in blocks:
        group_data['Thiên về tự nhiên'].append(len(natural_group[natural_group[block].notna()]))
        group_data['Thiên về xã hội'].append(len(social_group[social_group[block].notna()]))
        group_data['Cân bằng'].append(len(balanced_group[balanced_group[block].notna()]))

    stacked_bar_chart = go.Figure()
    colors = ['rgba(0, 114, 178, 0.8)', 'rgba(213, 94, 0, 0.8)', 'rgba(0, 158, 115, 0.8)']  # Blue, Vermillion, Green

    for group_name, color in zip(group_labels, colors):
        stacked_bar_chart.add_trace(go.Bar(
            x=blocks,
            y=group_data[group_name],
            name=group_name,
            marker=dict(color=color)
        ))

    stacked_bar_chart.update_layout(
        title='Tỷ lệ học sinh thuộc từng nhóm thiên hướng trong các khối thi',
        xaxis_title='Khối thi',
        yaxis_title='Số lượng học sinh',
        barmode='stack'
    )

    return json.dumps(stacked_bar_chart, cls=plotly.utils.PlotlyJSONEncoder)