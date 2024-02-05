from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.graph_objs as go
import random
from datetime import datetime, timedelta

# Constants
WINDOW_SIZE = 20  # Define the window size here

# Layout of the page
layout = html.Div([
    html.H1('Predictive Analysis'),
    dcc.Graph(id='live-update-graph-predictive'),
    dcc.Interval(
        id='interval-component-predictive',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Function to update the graph
def update_graph(n_intervals):
    # Generate timestamps for each interval within the window, 1 day ahead
    now = datetime.now() + timedelta(days=1)
    times = [now - timedelta(seconds=i) for i in range(WINDOW_SIZE)][::-1]

    # Generate random values for the line
    values = [random.uniform(14300, 27934) for _ in range(WINDOW_SIZE)]
    trace = go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        line=dict(color='orange'),  # Set the line color to orange
        name='Orange Line'
    )

    return {'data': [trace], 'layout': go.Layout(
        xaxis=dict(title='Time', range=[min(times), max(times)]),
        yaxis=dict(range=[14300, 27934], title='Value'),
        title='Predictive Real Time Data Streaming'
    )}

# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        Output('live-update-graph-predictive', 'figure'),
        [Input('interval-component-predictive', 'n_intervals')]
    )
    def update_output(n_intervals):
        return update_graph(n_intervals)
