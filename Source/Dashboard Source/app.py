import sys
import os

# Add Shared and DataExploration
sys.path.append(os.path.join(os.getcwd(), 'Source', 'DataExploration'))
sys.path.append(os.path.join(os.getcwd(), 'Source', 'Shared'))

# Import các module cần thiết
from DataExploration_example import *
from DataExploration_01 import *
from DataExploration_02 import *
from DataExploration_03 import *
from Libraries import *
from Shared_Functions import *

#Dashboard Libraries
from flask import Flask, render_template, render_template, request, jsonify
import plotly.graph_objects as go
import json
import plotly
import requests

app = Flask(__name__)

# LM Studio Local Server
BASE_URL = "http://localhost:1234"

def query_lmstudio(prompt):
    """
    Gửi truy vấn tới LM Studio Local Server và nhận phản hồi.
    """
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.7,
            }
        )
        if response.status_code == 200:
            # Get the response message from the LLM model
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error connecting to LM Studio: {e}"


#---------------------------------------------------- Không chỉnh sửa vùng ở trên. Trừ việc thêm thư viện vào.

@app.route('/')
def homepage():
    # Giả sử df là DataFrame chứa dataset
    num_rows = raw_df.shape[0]  # Số hàng
    num_columns = raw_df.shape[1]  # Số cột
    column_names = ', '.join(raw_df.columns)  # Tên các cột
    missing_values = raw_df.isnull().sum().to_dict()  # Thông tin về giá trị thiếu

    return render_template('index.html', 
                           num_rows=num_rows, 
                           num_columns=num_columns,
                           column_names=column_names,
                           missing_values=missing_values)

@app.route('/section1')
def section1():
    bar_avg_chart_json, pie_chart_json, histogram_charts, summary_stats,boxplot_chart_json = section_01_01()
    return render_template(
        'section1.html',
        bar_avg_chart=bar_avg_chart_json,
        pie_chart=pie_chart_json,
        histogram_charts=histogram_charts,
        summary_stats=summary_stats,
        boxplot_chart=boxplot_chart_json
    )

@app.route('/section2')
def section2():
    histogram_charts_json, summary_stats_json = section_02_01()
    grouped_bar_charts_json = section_02_02(df)
    density_plots_json = section_02_03(df)
    pie_charts_json = section_02_04(df)
    horizontal_bar_charts_json = section_02_05(df)
    student_group_donut_chart_json = section_02_06(df)
    student_stacked_bar_chart_json = section_02_07(df)
    return render_template(
        'section2.html',
        histogram_charts=histogram_charts_json,
        summary_stats=summary_stats_json,
        grouped_bar_charts=grouped_bar_charts_json,
        density_plots=density_plots_json,
        pie_charts=pie_charts_json,
        horizontal_bar_charts=horizontal_bar_charts_json,
        student_group_donut_chart=student_group_donut_chart_json,
        student_stacked_bar_chart=student_stacked_bar_chart_json
    )
                           
@app.route('/section3')
def section3():
    heatmap_json, strongest_correlations, weakest_correlations, launch_pad_stats, launch_pad_json, prediction_results = section_03_01()
    return render_template('section3.html', 
                         heatmap=heatmap_json,
                         strongest_correlations=strongest_correlations,
                         weakest_correlations=weakest_correlations,
                         launch_pad_stats=launch_pad_stats,
                         launch_pad=launch_pad_json,
                         performance_analysis=prediction_results)  
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_response = query_lmstudio(user_message)  # Gửi câu hỏi tới LM Studio
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
