#pages/overview.py
from dash import  Dash, html, dcc, Input, Output, callback
import dash_daq as daq
import numpy as np
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta
# from app import app  # Import the Dash app instance
from dash.dependencies import Input, Output
import random
from datetime import datetime, timedelta

# Function to update the graph
def update_graph(n_intervals):
    now = datetime.now()

    # Append new time and value
    x_values.append(now)
    y_values.append(random.uniform(6300, 27934))

    # Limit the number of points
    if len(x_values) > MAX_POINTS:
        x_values.pop(0)
        y_values.pop(0)

    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers'
    )
    return {
        'data': [trace],
        'layout': go.Layout(
            xaxis=dict(title='Time'),
            yaxis=dict(range=[22300, 25934], title='Value'),
            title='Anomaly Detection',
            #height=300  # Set the height you want here
        )
    }

# Function to register callbacks for the real-time graph on the overview page
def register_callbacks_overview(app):
    @app.callback(
        Output('live-update-graph-overview', 'figure'),  # Match the ID of the Graph component
        [Input('interval-component-overview', 'n_intervals')]  # Match the ID of the Interval component
    )
    def update_output_overview(n_intervals):
        return update_graph(n_intervals)


# Constants
MAX_POINTS = 1000  # Maximum number of points to display

# Lists to store x and y values
x_values = []
y_values = []

## Chloropeth
# Load GeoJSON for counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Example DataFrame with data
df = pd.DataFrame({
    "fips": [
        "01001", "01003", "01005", "06045",
        "41001", "36085", "06075", "42053",
        "12053", "48201", "13135", "06087",
        "41085", "08009", "25025", "06065",
        "36061", "60029", "53069", "48495"
    ],
    "fraud_percentage": [
        0.1, 0.2, 0.05, 0.62, 0.31, 0.54, 0.63, 0.67,
        0.77, 0.24, 0.87, 0.98, 0.62, 0.54, 0.36, 0.82,
        0.52, 0.4, 0.9, 0.88
    ]
})


# Create the Plotly figure
figMap = px.choropleth(df, geojson=counties, locations='fips', color='fraud_percentage',
                    color_continuous_scale="RdYlGn",
                    range_color=(0, 0.3),
                    scope="usa",
                    labels={'fraud_percentage': 'Fraud Percentage'},
                    title='Locationwise Fraudulent Transaction',
                   )
figMap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Update the Choropleth figure to have a dark theme
figMap.update_layout(
    geo=dict(
        bgcolor='rgba(240, 240, 240, 1)',  # Map background color
        lakecolor='rgba(211, 211, 211, 1)',  # Color of lakes, if any
        landcolor='rgba(211, 211, 211, 1)',  # Land color
    ),
    paper_bgcolor='rgba(18, 18, 18, 0.5)',  # Dark background color of the paper
    plot_bgcolor='rgba(0,0,0,0.5)',  # Dark background color of the plot
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title='Fraud Percentage',  # Title for the colorbar
        title_font=dict(color='white'),  # Font color for the title
        tickfont=dict(color='white'),  # Font color for the tick labels
    ),
)
##

val = np.array([0.07, 0.1, 0.09, 0.07, 0.06, 0.04, 0.04, 0.03, 0.02, 0.01])
case = np.array(['misc_net','shopping_net','shopping_pos','grocery_net',
                 'grocery_post', 'gas_transported', 'food_dining', 'home',
                 'entertainment', 'personal_care'])
figBar = px.bar(df, x=val, y=case, orientation='h',
                title='Fraud Percentage by Category')
figBar.update_layout(
    title={
        'text': 'Fraud Percentage by Category',
        'font': {
            'size': 18,
            'color': 'white'
        }
    },
    xaxis=dict(
        title='Fraud Percentage',
        tickformat='.0%'
    ),
    yaxis=dict(
        title='Fraud Category'
    )
)

# Update the Bar chart figure to have a dark theme
figBar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Background color of the plot
    paper_bgcolor='rgba(0,0,0,0)',  # Background color of the paper
    title=dict(x=0.5, xanchor='center'),  # Center the title
    xaxis=dict(
        title='Fraud Percentage',
        tickformat='.0%',
        color='white'  # X-axis title and tick labels color
    ),
    yaxis=dict(
        title='Fraud Category',
        color='white'  # Y-axis title and tick labels color
    )
)

## donut chart

case = np.array(['fraud_loss', 'fraud_without_loss','unclassified', 'default entry','not_fraud'])
case_num = np.array([3,8,2,7,153])

figDonut = px.pie(
    names=case,
    values=case_num,
    hole=0.3,  # Adjust the size of the hole to turn the pie chart into a donut chart
    title="Case Distribution"
)

figDonut.update_traces(textinfo='percent+label')  # Display percentage and label on the chart
figDonut.update_layout(
    paper_bgcolor='#121212',  # Background color of the outer area of the figure
    plot_bgcolor='#121212',  # Background color of the plotting area
    font_color='white'  # Update the font color for better contrast with the dark background
)

# #######  Overview page layout  #############
layout = html.Div([
    html.Div('Overview Page', className='overview-title'),

    dcc.Graph(id='live-update-graph-overview',
              style={'height': '350px'},),
    dcc.Interval(
        id='interval-component-overview',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    
    html.Div([
    daq.Gauge(
        id='my-gauge-1',
        className='gauge-title',
        label="% Success",
        min=0,  # Set the minimum value of the gauge scale
        max=100,
        value=89,
        style={'width': '30%', 'display': 'inline-block'}  # Adjust the width as necessary
    
    ),
    html.Div(style={'width': '2%', 'display': 'inline-block'}), 
    daq.Gauge(
        id='my-gauge-2',
        className='gauge-title',
        label="% Alert",
        min=0,  # Set the minimum value of the gauge scale
        max=100,
        value=8,
        style={'width': '30%', 'display': 'inline-block'}  # Adjust the width as necessary
    
    ),
    html.Div(style={'width': '2%', 'display': 'inline-block'}), 
    daq.Gauge(
        id='my-gauge-3',
        className='gauge-title',
        label="% Declined",
        min=0,  # Set the minimum value of the gauge scale
        max=100,
        value=3,
        style={'width': '30%', 'display': 'inline-block'}  # Adjust the width as necessary
    
    ),
    ], ),
    
    # html.Div([
    # daq.Gauge(
    #     id='my-gauge-1',
    #     className='gauge-title',
    #     label="Default",
    #     value=6
    # ),
    # daq.Gauge(
    #     id='my-gauge-1',
    #     className='gauge-title',
    #     label="Default",
    #     value=6
    # ),
    # ], className='gauge-container'),
    
    html.Div([
         # First row of cards
         html.Div([
             html.Div('Profile Analysed', className='card-title'),
             html.Div('153k', className='card-value')
         ], className='card'),
         html.Div([
             html.Div('Suspicious Transaction', className='card-title'),
             html.Div('43k', className='card-value')
         ], className='card'),
         # Second row of cards
         html.Div([
             html.Div('% Fraud Detected', className='card-title'),
             html.Div('20', className='card-value')
         ], className='card'),
         html.Div([
             html.Div('Concept Drift', className='card-title'),
             html.Div('2e-3', className='card-value')
         ], className='card'),
         
     ], className='card-container'),
    
    
    
    html.Div('Root Cause Analysis', className='overview-title'),
    
    html.Div([  # Parent container for bar and map
    html.Div([  # Bar container
        dcc.Graph(figure=figBar)
    ], className='bar-container'),

    html.Div([  # Map container
        dcc.Graph(figure=figMap, id='choropleth-map')
    ], className='map-container'),
    ], style={'display': 'flex'}),
    
    html.Div(style={'height': '150px'}), 
    
    html.Div('Fraudulent Case Breakdown', className='overview-title'),
    html.Div([  # Bar container
        dcc.Graph(figure=figDonut)
    ], className='Donut-container'),
    
    ##
    
    # html.Div([  # Bar container
    #     dcc.Graph(figure=figBar),
    # ], className='bar-container'),
    
    # html.Div([  # Map container
    #     dcc.Graph(figure=figMap, id='choropleth-map')
    # ], className='map-container'),
    
], className='dashboard-container'),