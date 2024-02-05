
# pages/home.py
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta
from dash import dash_table
import pandas as pd


# Constants
WINDOW_SIZE = 20  # Define the window size here

# Data in array form
analyst = ['Bernard Dixon', 'Carolyn Gilbert', 'Catherine Watkins', 'Courtney Richardson', 'Daryl Hopkins']
viewed = [105, 65, 64, 45, 170]
dismissed = [0, 0, 0, 0, 0]
open_case = [42, 12, 1, 1, 14]
closed_case = [32, 8, 1, 1, 13]

figTable = go.Figure(data=[go.Table(
    header=dict(values=['Analyst', 'Viewed', 'Dismissed', 'Open Case', 'Closed Case'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[analyst, viewed, dismissed, open_case, closed_case],
               fill_color='lavender',
               align='left'))
])
figTable.update_layout(
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
)

# Layout of the page
layout = html.Div([
    html.H1('Descriptive Analysis'),
    dcc.Graph(id='live-update-graph-home'),
    dcc.Interval(
        id='interval-component-home',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    
    html.Div('Current Threat', className='overview-title'),
    html.Div([
         # First row of cards
         html.Div([
             html.Div('Account Impacted', className='card-title'),
             html.Div('15', className='card-value')
         ], className='card'),
         html.Div([
             html.Div('Immediate Risk Exposure', className='card-title'),
             html.Div('$159,637', className='card-value')
         ], className='card'),
         # Second row of cards
         html.Div([
             html.Div('Account Protected', className='card-title'),
             html.Div('50', className='card-value')
         ], className='card'),
         html.Div([
             html.Div('Total Value Protected', className='card-title'),
             html.Div('$300,367', className='card-value')
         ], className='card'),
         
     ], className='card-container'),
    
    
    
    html.Div('Fraud Analyst Team', className='overview-title'),
    html.H3('Fraud Analyst Team'),
    dcc.Graph(figure=figTable)


])

# Function to update the graph
def update_graph(n_intervals):
    # Generate timestamps for each interval within the window
    now = datetime.now() + timedelta(hours=16)
    times = [now - timedelta(seconds=i) for i in range(WINDOW_SIZE)][::-1]

    # Generate random values within a smaller range for less fluctuation
    # Adjust the range (e.g., 20000 to 22000) to reduce the fluctuation
    min_val, max_val = 20000, 22000
    values = [random.uniform(min_val, max_val) for _ in range(WINDOW_SIZE)]

    trace = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers'
    )
    return {'data': [trace], 'layout': go.Layout(
        xaxis=dict(title='Time', range=[min(times), max(times)]),
        yaxis=dict(range=[min_val, max_val], title='Value'),
        title='Real Time Total Transaction Data Stream'
    )}

# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        Output('live-update-graph-home', 'figure'),
        [Input('interval-component-home', 'n_intervals')]
    )
    def update_output(n_intervals):
        return update_graph(n_intervals)