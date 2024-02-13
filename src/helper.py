from dash.exceptions import PreventUpdate
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pickle
from models.model import Models
import tensorflow as tf

news_label = {}
news_full = {}

class Helper():

    def __init__(self):
        self.test_path = "data/test.csv"
        self.test_data = pd.read_csv(self.test_path)
        self.news_text = self.test_data["text"].array.fillna('')
        self.id = self.test_data["id"].array.fillna('')
        self.title = self.test_data["title"].array.fillna('')
        self.author = self.test_data["author"].array.fillna('')
        self.selected_news = None
        self.selected_id = None
        self.submit_path = "data/submit.csv"
        self.submit_data = pd.read_csv(self.submit_path)

        # Model and tokenizer for logistic regression
        self.log_reg_model = pickle.load(open('models/logistic/logistic_model.pkl', 'rb'))
        self.log_reg_tokenizer = pickle.load(open('models/logistic/tfidf_vectorizer.pkl', 'rb'))

        # Model and tokenizer for lstm regression
        self.lstm_model = tf.keras.models.load_model('models/lstm/lstm_model.h5')
        self.lstm_tokenizer = pickle.load(open('models/lstm/tokenizer_lstm.pkl', 'rb'))

        # Model and tokenizer for gnn regression
        self.gnn_model = tf.keras.models.load_model('models/gnn/modelgnn.h5')
        self.gnn_text_tokenizer = pickle.load(open('models/gnn/gnn_tokenizer_text.pickle', 'rb'))
        self.gnn_author_tokenizer = pickle.load(open('models/gnn/gnn_tokenizer_author.pickle', 'rb'))

    def calculate_credibility(self,models_obj,model_name):
        result = None
        if model_name == "logistic":
            print(type(news_full[int(self.selected_news)]))
            tokenized_text = models_obj.tokenize(model_name,self.log_reg_tokenizer, [news_full[int(self.selected_news)]])
            result = models_obj.predict_text(model_name, self.log_reg_model, tokenized_text)
        elif model_name == "lstm":
            tokenized_text = models_obj.tokenize(model_name,self.lstm_tokenizer, news_full[int(self.selected_news)])
            result = models_obj.predict_text(model_name, self.lstm_model, tokenized_text)
        elif model_name == "gnn":
            title = self.test_data.loc[self.test_data['id']==self.selected_id, 'title']
            title = title.iloc[0]
            text = news_full[int(self.selected_news)]
            stitched_text = title + ' ' + text            
            author = self.test_data.loc[self.test_data['id']==self.selected_id, 'author']
            author = author.fillna('Anonymous')
            author = author.iloc[0]           
            text_padded, author_padded = models_obj.tokenize_gnn(self.gnn_text_tokenizer,self.gnn_author_tokenizer,stitched_text,author)
            result = models_obj.predict_text(model_name, self.gnn_model, [text_padded,author_padded])
        if result <= 0.5:
            return "true"
        else:
            return "false"

    def predict(self,n_clicks):
        if n_clicks is None:
            style = {'display': 'none'}
            children = []
        else:
            models_obj = Models()
            linear_result = self.calculate_credibility(models_obj,"logistic")
            lstm_result = self.calculate_credibility(models_obj, "lstm")
            gnn_result = self.calculate_credibility(models_obj, "gnn")
            style = {'display': 'block'}
            children=[
                        dbc.Row([
                            dbc.Col([
                                html.Div("Logestic Regression", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src=f'assets/{linear_result}.png',className="true-false-indicator card-text")])],width=4),
                            dbc.Col([html.Div("LSTM", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src=f'assets/{lstm_result}.png',className="true-false-indicator card-text")])],width=4),
                            dbc.Col([html.Div("GNN", className="card-header"),
                                html.Div(className="card-body", children=[
                                html.Img(src=f'assets/{gnn_result}.png',className="true-false-indicator card-text")])],width=4)
                        ])
                    ]
        return style, children
        
    def update_news_details(self,selected_value):
        if selected_value is not None:
            self.selected_news = selected_value

            filtered_rows = self.test_data[self.test_data['text'] == news_full[int(self.selected_news)]]

            id = ""
            title = ""
            author = ""

            if not filtered_rows.empty:
                id = filtered_rows['id'].values[0]
                self.selected_id = id
                title = filtered_rows['title'].values[0]
                author = filtered_rows['author'].values[0]
                label_value = self.submit_data.loc[self.submit_data['id']==int(id), 'label']
                if label_value.iloc[0] == 0:
                    actual_value = "Reliable"
                elif label_value.iloc[0] == 1:
                    actual_value = "Unreliable"
                
            else:
                id, title, author = "NAN"
        
            style= {'display': 'block'}

            children=[
                        html.Div("News Details :", className="card-header"),
                        html.Div(className="card-body", children=[
                            html.P(f'ID : {id}',className="card-text"),
                            html.P(f'Title : {title}',className="card-text"),
                            html.P(f'Author : {author}',className="card-text"),
                            html.P(f'Full Text : {news_full[int(self.selected_news)]}',className="card-text"),
                            html.P(f'Actual Label : {actual_value}',className="card-text")
                        ])
                    ]
        else:
            style = {'display': 'none'}
            children = []

        return style, children

    def populate_news(self,search_value):
        if not search_value:
            raise PreventUpdate
        
        news_matched = [str(o) for o in self.news_text if search_value in str(o)]
        for i in range(0,len(news_matched)-1):
            news_label[i] = news_matched[i][:140]
            news_full[i] = news_matched[i]            
        return news_label