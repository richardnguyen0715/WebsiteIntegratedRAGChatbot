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
    line_chart_json, pie_chart_json, bar_chart_json = section_home_01()

    return render_template(
        "index.html",
        line_chart=line_chart_json,
        pie_chart=pie_chart_json,
        bar_chart=bar_chart_json
    )

@app.route('/section1')
def section1():
    bar_avg_chart_json, bar_min_max_chart_json, pie_chart_json = section_01_01()
    return render_template(
        'section1.html',
        bar_avg_chart=bar_avg_chart_json,       # Average scores
        bar_min_max_chart=bar_min_max_chart_json,  # Min/Max scores
        pie_chart=pie_chart_json                # Subject coverage
    )

@app.route('/section2')
def section2():
    return render_template('section2.html')

@app.route('/section3')
def section3():
    return render_template('section3.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    bot_response = query_lmstudio(user_message)  # Gửi câu hỏi tới LM Studio
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
