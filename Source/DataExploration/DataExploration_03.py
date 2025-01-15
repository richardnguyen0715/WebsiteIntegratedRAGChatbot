from Libraries import *
from Shared_Functions import *
import pandas as pd
import plotly.graph_objects as go
import json
import seaborn as sns
import plotly.express as px

def analyze_student_performance(df):
    # Calculate total score for each student
    df['total_score'] = df[['Toán', 'Văn', 'Vật Lý', 'Hóa Học', 'Sinh Học', 
                           'Tiếng Anh', 'Lịch Sử', 'Địa Lý', 'GDCD']].sum(axis=1)
    
    # Define high performers (top 25%)
    high_score_threshold = df['total_score'].quantile(0.75)
    high_performers = df[df['total_score'] >= high_score_threshold]
    
    # Analyze subject patterns
    performance_analysis = {
        'threshold': high_score_threshold,
        'avg_scores': {subject: high_performers[subject].mean() 
                      for subject in df.columns if subject != 'total_score'},
        'subject_correlations': {subject: df[subject].corr(df['total_score']) 
                               for subject in df.columns if subject != 'total_score'}
    }
    
    # Find successful subject combinations
    high_score_subjects = []
    for subject in df.columns:
        if subject != 'total_score':
            high_score_count = len(df[df[subject] >= 8])
            high_score_subjects.append((subject, high_score_count))
    
    top_subjects = sorted(high_score_subjects, key=lambda x: x[1], reverse=True)[:3]
    
    performance_analysis['top_subjects'] = {
        'subjects': [x[0] for x in top_subjects],
        'counts': [x[1] for x in top_subjects],
        'avg_score': high_performers['total_score'].mean()
    }
    
    return performance_analysis



# Dữ liệu mẫu
data = pd.read_csv('Dataset/THPTQG_2023_processed.csv')
#convert to DataFrame
raw_df = pd.DataFrame(data)

# Loại bỏ cột 'id'
raw_df = raw_df.drop(columns=['Student ID'])
#đổi tên các cột về tên môn
raw_df = raw_df.rename(columns={
'Mathematics': 'Toán',
'Literature': 'Văn',
'Physics': 'Vật Lý',
'Chemistry': 'Hóa Học',
'Biology': 'Sinh Học',
'Foreign language': 'Tiếng Anh',
'History': 'Lịch Sử',
'Geography': 'Địa Lý',
'Civic education': 'GDCD'
})
def section_03_01():
    # Calculate correlation matrix
    correlation_matrix = raw_df.corr()

    # Create heatmap
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        text=np.round(correlation_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 14, "color": "black"},
        hoverongaps=False,
        colorscale='Viridis',  # Colorblind-friendly colorscale
        zmid=0
    ))

    heatmap.update_layout(
        title='Ma trận tương quan giữa các môn học',
        width=800,
        height=600,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 12},
        xaxis={'showgrid': False},
        yaxis={'showgrid': False},
        margin=dict(
            l=60,
            r=60,
            t=100,
            b=60,
            pad=4
        ),
        autosize=False
    )
    # Convert to JSON
    heatmap_json = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)

    # Find strongest and weakest correlations
    correlations = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr = {
                'subject1': correlation_matrix.columns[i],
                'subject2': correlation_matrix.columns[j],
                'correlation': correlation_matrix.iloc[i, j]
            }
            correlations.append(corr)
    
    strongest_correlations = sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)[:10]
    weakest_correlations = sorted(correlations, key=lambda x: abs(x['correlation']))[:10]
    #--------------------------------------------------------------------------------------------------------#
    # Calculate total score and launch pad analysis
    df = raw_df.copy()
    df['total_score'] = df[['Toán', 'Văn', 'Vật Lý', 'Hóa Học', 'Sinh Học', 
                           'Tiếng Anh', 'Lịch Sử', 'Địa Lý', 'GDCD']].sum(axis=1)
    
    launch_pad_stats = []
    for subject in df.columns[:-1]:
        stats = {
            'subject': subject,
            'mean_score': df[subject].mean(),
            'total_correlation': df[subject].corr(df['total_score']),
            'high_score_count': len(df[df[subject] >= 8])
        }
        launch_pad_stats.append(stats)
    launch_pad_stats = sorted(launch_pad_stats, key=lambda x: (x['total_correlation'], x['high_score_count']), reverse=True)
    # Create launch pad visualization
    launch_pad = go.Figure(data=[
        go.Scatter(
            x=[stat['mean_score'] for stat in launch_pad_stats],
            y=[stat['total_correlation'] for stat in launch_pad_stats],
            mode='markers+text',
            text=[stat['subject'] for stat in launch_pad_stats],
            textposition="top center",
            marker=dict(
                size=12,
                color=[stat['high_score_count'] for stat in launch_pad_stats],
                colorscale='Greens',  # Colorblind-friendly colorscale
                showscale=True,
                colorbar=dict(title="Số lượng điểm cao (≥8)")
            )
        )
    ])
    
    launch_pad.update_layout(
        title='Phân tích những môn học bệ phóng',
        xaxis=dict(
            title="Điểm trung bình môn",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='rgba(128,128,128,0.5)'
        ),
        yaxis=dict(
            title="Tương quan với tổng điểm",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='rgba(128,128,128,0.5)'
        ),
        width=800,
        height=700,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black'},
        margin=dict(l=50, r=50, t=80, b=50)
    )
    launch_pad_json = json.dumps(launch_pad, cls=plotly.utils.PlotlyJSONEncoder)
    prediction_results = analyze_student_performance(df)
    return (heatmap_json, strongest_correlations, weakest_correlations, 
            launch_pad_stats, launch_pad_json, prediction_results)
    

def section_03_02():
    # Define subject groups
    sciences = ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học', 'Tiếng Anh']

    # Calculate average scores for each combination
    avg_scores_A00 = raw_df[['Toán', 'Vật Lý', 'Hóa Học']].mean()
    avg_scores_A01 = raw_df[['Toán', 'Vật Lý', 'Tiếng Anh']].mean()
    avg_scores_B00 = raw_df[['Toán', 'Hóa Học', 'Sinh Học']].mean()

    # Ensure all subjects are included in each combination
    avg_scores_A00 = avg_scores_A00.reindex(sciences, fill_value=0)
    avg_scores_A01 = avg_scores_A01.reindex(sciences, fill_value=0)
    avg_scores_B00 = avg_scores_B00.reindex(sciences, fill_value=0)

    # Find the highest score in each combination
    max_A00 = avg_scores_A00.max()
    max_A01 = avg_scores_A01.max()
    max_B00 = avg_scores_B00.max()

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_scores_A00,
        theta=sciences,
        fill='toself',
        name='A00',
        line=dict(color='rgb(68, 1, 84)'),  # Color from Viridis palette
        marker=dict(
            size=[15 if val == max_A00 else 5 for val in avg_scores_A00],
            color='rgb(68, 1, 84)'
        )
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_scores_A01,
        theta=sciences,
        fill='toself',
        name='A01',
        line=dict(color='rgb(49, 104, 142)'),  # Color from Viridis palette
        marker=dict(
            size=[15 if val == max_A01 else 5 for val in avg_scores_A01],
            color='rgb(49, 104, 142)'
        )
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_scores_B00,
        theta=sciences,
        fill='toself',
        name='B00',
        line=dict(color='rgb(53, 183, 121)'),  # Color from Viridis palette
        marker=dict(
            size=[15 if val == max_B00 else 5 for val in avg_scores_B00],
            color='rgb(53, 183, 121)'
        )
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title='Điểm trung bình các môn KHTN theo tổ hợp xét tuyển',
        width=650,
        height=500,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 12}
    )

    # Convert to JSON
    radar_chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return radar_chart_json

def section_03_03():
    # Define subject groups
    natural_sciences = ['Toán', 'Vật Lý', 'Hóa Học', 'Sinh Học']

    # Calculate total score
    df = raw_df.copy()
    df['total_score'] = df[natural_sciences].sum(axis=1)

    # Calculate correlation with total score
    correlations = df[natural_sciences].corrwith(df['total_score'])

    # Create bar chart
    fig = px.bar(
        x=correlations.index,
        y=correlations.values,
        labels={'x': 'Môn học', 'y': 'Hệ số tương quan'},
        title='Hệ số tương quan giữa điểm môn KHTN và tổng điểm của tổ hợp Tự Nhiên',
    )

    fig.update_layout(
        width=700,
        height=500,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 12}
    )

    # Convert to JSON
    bar_chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_json

def section_03_04():
    # Define subject groups
    social_sciences = ['Toán', 'Văn', 'Lịch Sử', 'Địa Lý', 'Tiếng Anh']

    # Calculate average scores for each combination
    avg_scores_C00 = raw_df[['Văn', 'Lịch Sử', 'Địa Lý']].mean()
    avg_scores_D00 = raw_df[['Văn', 'Toán', 'Tiếng Anh']].mean()

    # Ensure all subjects are included in each combination
    avg_scores_C00 = avg_scores_C00.reindex(social_sciences, fill_value=0)
    avg_scores_D00 = avg_scores_D00.reindex(social_sciences, fill_value=0)

    # Find the highest score in each combination
    max_C00 = avg_scores_C00.max()
    max_D00 = avg_scores_D00.max()

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=avg_scores_C00,
        theta=social_sciences,
        fill='toself',
        name='C00',
        line=dict(color='rgb(49, 104, 142)'),  # Color from Viridis palette
        marker=dict(
            size=[15 if val == max_C00 else 5 for val in avg_scores_C00],
            color='rgb(49, 104, 142)'
        )
    ))

    fig.add_trace(go.Scatterpolar(
        r=avg_scores_D00,
        theta=social_sciences,
        fill='toself',
        name='D00',
        line=dict(color='rgb(68, 1, 84)'),  # Color from Viridis palette
        marker=dict(
            size=[15 if val == max_D00 else 5 for val in avg_scores_D00],
            color='rgb(68, 1, 84)'
        )
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title='Điểm trung bình các môn KHXH theo tổ hợp xét tuyển',
        width=650,
        height=500,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 12}
    )

    # Convert to JSON
    radar_chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return radar_chart_json

def section_03_05():
    # Define subject groups
    natural_sciences = ['Văn', 'Lịch Sử', 'Địa Lý', 'GDCD']

    # Calculate total score
    df = raw_df.copy()
    df['total_score'] = df[natural_sciences].sum(axis=1)

    # Calculate correlation with total score
    correlations = df[natural_sciences].corrwith(df['total_score'])

    # Create bar chart
    fig = px.bar(
        x=correlations.index,
        y=correlations.values,
        labels={'x': 'Môn học', 'y': 'Hệ số tương quan'},
        title='Hệ số tương quan giữa điểm môn KHXH và tổng điểm của tổ hợp Xã hội',
    )

    fig.update_layout(
        width=700,
        height=500,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 12}
    )

    # Convert to JSON
    bar_chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return bar_chart_json