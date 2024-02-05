# index.py
import dash
from dash.dependencies import Input, Output
from dash import html, dcc
import pages.overview  # Import the Overview page
import pages.datahub  # Import the DataHub page
import pages.home  # Import the Home page

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([  # This div represents the top bar
        html.Img(src=app.get_asset_url('logo.gif'), style={'height': '3rem', 'margin-right': '2rem'}),  # Adjust 'height' as needed
        html.H2('Sybil System', style={'display': 'inline-block', 'margin-right': '2rem', 'vertical-align': 'middle'}),
        dcc.Link('Home', href='/', className='link-button'),
        dcc.Link('Overview', href='/overview', className='link-button'),
        dcc.Link('DataHub', href='/datahub', className='link-button'),
        # ... Add more links or interactive components here if needed ...
    ], className='topbar'),
    html.Div(id='page-content', className='content')  # Add 'content' class for main content area
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/overview':
        return pages.overview.layout
    elif pathname == '/datahub':
        return pages.datahub.layout
    elif pathname == '/':  # Make sure this condition is handling the root path
        return pages.home.layout
    else:
        return '404 Page Not Found'  # Optional: Handle unmatched paths

if __name__ == '__main__':
    app.run_server(debug=True)
