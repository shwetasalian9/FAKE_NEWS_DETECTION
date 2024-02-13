import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
from src.helper import Helper
from dash.exceptions import PreventUpdate
from src.helper import Helper
from app import app

helper_obj = Helper()

layout = html.Div(
    children=[
        html.Div(children=[
            dbc.Row([
                    dbc.Col(html.Img(src="assets/fake-news.png", className="page-logo"),width=4),
                    dbc.Col(html.H2(children="Fake News Detection", className="header-title"),width=8)
                ]),
            html.P(children=("Elevating News Credibility with Expert Fake News Detection using AI !"),className="header-description")
            ], className = "header"),

            html.H3(children =" Check if news is real or fake !", className="h3container text-center"),
            html.Div(children = [
                dcc.Dropdown(id="newsList", placeholder="Start typing to search for a news...", className="form-control input-text"),
                html.Div(id='news-details', className = "card border-primary mb-3 card-details"
                ),
            ], className = "container justify-content-center"),

            html.Div(children=[html.Button("Predict", id="predict", className="btn btn-lg btn-primary btn:hover")],className = "predict"),
            html.Div(id="predict-result-1",className = "card border-primary mb-3 card-details container justify-content-center")
    ]
)

@app.callback(
    Output('newsList', 'options'),
    Output('predict-result-1', 'style'),
    Output('predict-result-1', 'children'),
    Input('newsList', 'search_value'),
    Input('predict', 'n_clicks')
)
def populate_news(search_value, n_clicks):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger_id == "newsList":
        style,children = helper_obj.predict(n_clicks=None)
        options = helper_obj.populate_news(search_value)
    else:
        options = []
        style,children = helper_obj.predict(n_clicks)
   
    return options, style, children

@app.callback(
    Output('news-details','style'),
    Output('news-details','children'),
    [Input('newsList', 'value',)]
)
def update_news_details(selected_value):
    return helper_obj.update_news_details(selected_value)
