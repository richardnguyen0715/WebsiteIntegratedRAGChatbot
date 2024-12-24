from Libraries import *
from Shared_Functions import *
import pandas as pd
import plotly.graph_objects as go
import json
import seaborn as sns

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
        textfont={"size": 12, "color": "black"},
        hoverongaps=False,
        colorscale='RdBu',
        zmid=0
    ))

    heatmap.update_layout(
        width=900,
        height=700,
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font={'color': 'black'},
        xaxis={'showgrid': False},
        yaxis={'showgrid': False},
        margin=dict(
            l=50,    
            r=50,    
            t=100,   
            b=50,    
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
    
    return heatmap_json, strongest_correlations, weakest_correlations
    
    return heatmap_json, correlations