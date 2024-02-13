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
            html.H3(children ="Comparison Overview", className="h3container text-center"),
            html.Div(id="overview-div",className = "card border-primary mb-3 card-details container justify-content-center",
                     children=[
                        dbc.Row([
                            dbc.Col([
                                html.Div("Logestic Regression", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/logistic-logo.png',className="true-false-indicator card-text")])],width=4),
                            dbc.Col([html.Div("LSTM", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/lstm-logo.png',className="true-false-indicator card-text")])],width=4),
                            dbc.Col([html.Div("GNN", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/gnn-logo.png',className="true-false-indicator card-text")])],width=4)
                        ])
                    ]),
            html.Div(id="metrics-comparison",className = "card border-primary mb-3 card-details container justify-content-center",
                children=[
                        dbc.Row([
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/metrics_logistic_prediction.png',className="metric_graph card-text")])],width=4),
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/metrics_lstm_prediction.png',className="metric_graph card-text")])],width=4),
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/metrics_gnn_prediction.png',className="metric_graph card-text")])],width=4)
                        ])
                    ]),
            html.Div(id="cm-comparison",className = "card border-primary mb-3 card-details container justify-content-center",
                children=[
                        dbc.Row([
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/logistic_cm.png',className="metric_graph card-text")])],width=4),
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/lstm_cm.png',className="metric_graph card-text")])],width=4),
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/gnn_cm.png',className="metric_graph card-text")])],width=4)
                        ])
                    ]),
            html.Div(id="test-results", className = "card border-primary mb-3 card-details container justify-content-center",
                     children=[
                        dbc.Row([
                            dbc.Col([
                                html.Div(className="card-body", children=[
                                html.Img(src='assets/num_predictions.jpeg',className="metric_graph_common card-text")])],width=4)
                        ])
                    ])
    ]
)

