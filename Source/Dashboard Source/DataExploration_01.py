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

# Loại bỏ cột 'id'
df = df.drop(columns=['id'])

#-------------------- Thực hiện xử lý các hàm dưới này nha mấy ní.

def section_01_01():
    # 1. Bar Chart: Average Scores by Subject
    averages = df.mean()
    bar_avg_chart = go.Figure(data=[
        go.Bar(
            x=averages.index, 
            y=averages.values, 
            name='Average Scores'
        )
    ])
    bar_avg_chart.update_layout(
        title="Average Scores by Subject",
        xaxis_title="Subjects",
        yaxis_title="Average Score"
    )
    bar_avg_chart_json = json.dumps(bar_avg_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # 2. Bar Chart: Minimum and Maximum Scores by Subject
    min_scores = df.min()
    max_scores = df.max()
    bar_min_max_chart = go.Figure(data=[
        go.Bar(x=min_scores.index, y=min_scores.values, name="Minimum Scores"),
        go.Bar(x=max_scores.index, y=max_scores.values, name="Maximum Scores")
    ])
    bar_min_max_chart.update_layout(
        title="Minimum and Maximum Scores by Subject",
        xaxis_title="Subjects",
        yaxis_title="Scores",
        barmode="group"
    )
    bar_min_max_chart_json = json.dumps(bar_min_max_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # 3. Pie Chart: Subject Coverage (Non-Null Counts)
    coverage = df.notnull().sum()
    pie_chart = go.Figure(data=[
        go.Pie(labels=coverage.index, values=coverage.values)
    ])
    pie_chart.update_layout(title="Subject Coverage (Data Availability)")
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_avg_chart_json, bar_min_max_chart_json, pie_chart_json