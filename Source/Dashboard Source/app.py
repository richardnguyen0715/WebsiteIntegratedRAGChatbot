import sys
import os

# Add Shared and DataExploration
sys.path.append(os.path.join(os.getcwd(), 'Source', 'DataExploration'))
sys.path.append(os.path.join(os.getcwd(), 'Source', 'Shared'))

# Import các module cần thiết
from DataExploration_example import *
from Libraries import *
from Shared_Functions import *

#Dashboard Libraries
from flask import Flask, render_template
import plotly.graph_objects as go
import json
import plotly

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route("/section1")
def section1():

    line_chart_json, pie_chart_json, bar_chart_json = section_01_01()

    return render_template(
        "section1.html",
        line_chart=line_chart_json,
        pie_chart=pie_chart_json,
        bar_chart=bar_chart_json
    )

@app.route('/section2')
def section2():
    return render_template('section2.html')

@app.route('/section3')
def section3():
    return render_template('section3.html')

if __name__ == "__main__":
    app.run(debug=True)
