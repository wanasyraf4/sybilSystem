
# pages/home.py
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta

# Constants
WINDOW_SIZE = 20  # Define the window size here

# Layout of the page
layout = html.Div([
    html.H1('Descriptive Analysis'),
    dcc.Graph(id='live-update-graph-home'),
    dcc.Interval(
        id='interval-component-home',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
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
        title='Real Time Data Streaming'
    )}

# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        Output('live-update-graph-home', 'figure'),
        [Input('interval-component-home', 'n_intervals')]
    )
    def update_output(n_intervals):
        return update_graph(n_intervals)