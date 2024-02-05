# import dash
import dash_daq as daq
from dash.dependencies import Input, Output
import pages.overview, pages.Descriptive, pages.home , pages.Predictive # Ensure pages.home is imported
import pandas as pd
import json
from dash import Dash

# from myapp import app
from urllib.request import urlopen
from dash import  Dash, html, dcc, Input, Output, callback


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server 

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([  # This div represents the top bar
        html.Img(src=app.get_asset_url('logo.gif'), style={'height': '3rem', 'margin-right': '2rem'}),  # Adjust 'height' as needed
        html.H2('Sibyl System', style={'display': 'inline-block', 'margin-right': '2rem', 'vertical-align': 'middle'}),
        
        dcc.Link('Overview', href='/overview', className='link-button'),
        # dcc.Link('Descriptive', href='/Descriptive', className='link-button'),
        dcc.Link('Descriptive', href='/', className='link-button'),
        dcc.Link('Predictive', href='/Predictive', className='link-button'),
        # ... Add more links or interactive components here if needed ...
    ], className='topbar'),
    html.Div(id='page-content', className='content')  # Add 'content' class for main content area
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/overview':
        return pages.overview.layout
    # elif pathname == '/Descriptive':
    #     return pages.Descriptive.layout
    elif pathname == '/Predictive':
        return pages.Predictive.layout
    elif pathname == '/':  # Make sure this condition is handling the root path
        return pages.home.layout
    else:
        return '404 Page Not Found'  # Optional: Handle unmatched paths


# Register the callbacks for the home page
from pages.home import register_callbacks as register_home_callbacks
register_home_callbacks(app)


# Register the callbacks for the overview
from pages.overview import layout as overview_layout, register_callbacks_overview
# app.layout = overview_layout
register_callbacks_overview(app)

# Only run the server if this file is executed directly (not imported)
if __name__ == '__main__':
    app.run_server(debug=True)



# if __name__ == '__main__':
#     from pages.home import layout, register_callbacks  # Adjusted import
#     app.layout = layout
#     register_callbacks(app)
#     app.run_server(debug=True)
