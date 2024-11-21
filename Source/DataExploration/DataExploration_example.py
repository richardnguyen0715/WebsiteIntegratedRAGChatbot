from Libraries import *
from Shared_Functions import *

#-------------------- Thực hiện xử lý các hàm dưới này nha mấy ní.

def section_01_01():
    line_chart = go.Figure(data=[
        go.Scatter(x=["Jan", "Feb", "Mar", "Apr"], y=[10, 15, 13, 17], name="Tickets Created"),
        go.Scatter(x=["Jan", "Feb", "Mar", "Apr"], y=[8, 12, 11, 14], name="Tickets Solved")
    ])
    line_chart_json = json.dumps(line_chart, cls=plotly.utils.PlotlyJSONEncoder)

    pie_chart = go.Figure(data=[
        go.Pie(labels=["Setup", "Features", "Fixes"], values=[19, 26, 55])
    ])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)

    bar_chart = go.Figure(data=[
        go.Bar(x=["Mon", "Tue", "Wed", "Thu", "Fri"], y=[5, 10, 15, 20, 25], name="Tickets/Week")
    ])
    bar_chart_json = json.dumps(bar_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return line_chart_json, pie_chart_json, bar_chart_json