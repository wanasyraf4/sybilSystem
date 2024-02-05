import plotly.express as px
import numpy as np
from dash import html
from dash import  Dash, html, dcc, Input, Output, callback
import plotly.graph_objects as go

# Convert to numeric for sorting
val2 = np.array([0.05, 0.03, 0.09, 0.04, 0.08, 0.07, 0.01, 0.02, 0.04, 0.06, 0.034])
case2 = np.array(['misc_net', 'shopping_net', 'shopping_pos', 'grocery_net',
                 'grocery_post', 'gas_transported', 'food_dining', 'home',
                 'entertainment', 'personal_care', 'unknown'])

# Combine arrays into structured array for sorting
combined = np.core.records.fromarrays([val2, case2], names='val,case')

# Sort by 'val' in descending order
sorted_combined = np.sort(combined, order='val')[::1]

# Extract sorted arrays
sorted_val2 = sorted_combined['val']
sorted_case2 = sorted_combined['case']

figPredBar = px.bar(x=sorted_val2, y=sorted_case2, orientation='h', color_discrete_sequence=['orange'] * len(sorted_val2))
figPredBar.update_layout(
    title='Predicted Fraud Case by Category',
    xaxis_title='Fraud Percentage',
    yaxis_title='Fraud Category',
    plot_bgcolor='rgba(0,0,0,0)',  # Optional: Set plot background color (adjust or remove as needed)
    paper_bgcolor='rgba(0,0,0,0)',  # Optional: Set paper background color (adjust or remove as needed)
     font=dict(
        color='white'
    ),
    xaxis=dict(
        title_font=dict(
            color='white'
        ),
        tickfont=dict(
            color='white'
        )
    ),
    yaxis=dict(
        title_font=dict(
            color='white'
        ),
        tickfont=dict(
            color='white'
        )
    )
)


####
fraud_types = [
    "Phishing attacks", "Account Takeover Fraud", "Chargeback Fraud",
    "Merchant Identity Fraud", "Triangulation Fraud"
]
dates = ['2024-11-02', '2024-11-24', '2024-07-08', '2024-10-17', '2025-01-27']
figFraud = go.Figure(data=[go.Table(
    header=dict(values=["Fraud Type", "Predicted Date"]),
    cells=dict(values=[fraud_types, dates]))
])
figFraud.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
)

# DataHub page layout
layout = html.Div([
    html.H3('Predictive Analysis'),
    # Add your DataHub page content here
    html.Div([  # Bar container
        dcc.Graph(figure=figPredBar)
    ], className='PredBar-container'),
    
    html.Div('Predicted Threat Type', className='overview-title'),
    html.Div([
    html.H3("Fraudulent Case Prediction"),
    dcc.Graph(figure=figFraud)
])
])