import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate


app = Dash(__name__,external_stylesheets=[dbc.themes.SUPERHERO],
           meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)
app.title = "FakeNewsDetection"