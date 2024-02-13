# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import overview, test_news

# Connect the navbar to the index
from comp import navbar

# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # This url is to display overall statistics of the three models
    if pathname == '/Overview':
        return overview.layout
    # This url is to test one particular news and compare results of all three models
    if pathname == '/TestNews':
        return test_news.layout
    else: # if redirected to unknown link
        return overview.layout

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)