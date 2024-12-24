from Libraries import *
from Shared_Functions import *
import pandas as pd
import plotly.graph_objects as go
import json
import seaborn as sns
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

def section_03_01():
    # Load and prepare data
    data = pd.read_csv('Dataset/THPTQG_2022_processed.csv')
    df = pd.DataFrame(data)
    df = df.drop(columns=['id'])
    
    # Rename columns to Vietnamese
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

    # Calculate correlation matrix
    correlation_matrix = df.corr()

    # Create heatmap
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        text=np.round(correlation_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 14, "color": "black"},
        hoverongaps=False,
        colorscale='RdBu',
        zmid=0
    ))

    heatmap.update_layout(
        width=1030,
        height=800,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black', 'size': 14},
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

    # Find strongest correlations
    correlations = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr = {
                'subject1': correlation_matrix.columns[i],
                'subject2': correlation_matrix.columns[j],
                'correlation': correlation_matrix.iloc[i,j]
            }
            correlations.append(corr)
    
    strongest_correlations = sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)[:10]
    weakest_correlations = sorted(correlations, key=lambda x: abs(x['correlation']))[:10]
    #--------------------------------------------------------------------------------------------------------#
    # Calculate total score and launch pad analysis
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
    
    # Create launch pad visualization
    launch_pad = go.Figure(data=[
        go.Scatter(
            x=[stat['mean_score'] for stat in launch_pad_stats],
            y=[stat['total_correlation'] for stat in launch_pad_stats],
            mode='markers+text',
            text=[stat['subject'] for stat in launch_pad_stats],
            textposition="top center",
            marker=dict(
                size=20,
                color=[stat['high_score_count'] for stat in launch_pad_stats],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Số lượng điểm cao (≥8)")
            )
        )
    ])
    
    launch_pad.update_layout(
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
        width=1030,
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
    
