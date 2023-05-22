"""
Using Dash to create a web app for the project
"""

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parents[2] / "TextSpace")) 
from plot3D import plot_embeddings_3d
from data import TextSpaceData

import os


path = Path(__file__)
# read plotly data
df = pd.read_csv(path.parents[2] / 'data' / 'plotly_data.csv')

load_figure_template("LUX")

# create TextSpaceData object
TextSpace_emotion = TextSpaceData(df, embedding_type="emotion")
fig_emotion = plot_embeddings_3d(TextSpace_emotion)
#TextSpace_gpt2 = TextSpaceData(df, embedding_type="gpt2")
#fig_gpt2 = plot_embeddings_3d(TextSpace_gpt2)
#TextSpace_bow = TextSpaceData(df, embedding_type="bow")
#fig_bow = plot_embeddings_3d(TextSpace_bow)
#TextSpace_topic = TextSpaceData(df, embedding_type="topic")
#fig_topic = plot_embeddings_3d(TextSpace_topic)


app = Dash(external_stylesheets=[dbc.themes.LUX])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "1rem 1rem",
    "background-color": "#ABD699",
    "width": "20rem",
}

sidebar = html.Div(
    [
        html.H4("Embedding type"),
        html.Hr(),

        dbc.Nav(
            [
                dcc.Dropdown(id="embedding-type",
                    options=[
                        {'label': 'Emotion', 'value': 'emotion'},
                        {'label': 'GPT2', 'value': 'gpt2'},
                        {'label': 'Bag of words', 'value': 'bow'},
                        {'label': 'Latent Dirichlet Allocation', 'value': 'topic'}
                    ],
                    value='emotion',
                    clearable=False,
                    style={'width': '100%'}
                ),
            ],
            vertical=True,
            pills=True,
        ),

        # padding no line
        html.Hr(style={"border-top": "1px solid #ABD699"}),
        # include text area
        html.Div(
            [
                html.H4("Text"),
                html.Hr(),
                dcc.Textarea(
                    id="text-area",
                    value="Click on a point to view the text",
                    readOnly=True,
                    draggable=True,
                    style={'width': '100%', 'height': 500}
                )
            ])
    ],
    style=SIDEBAR_STYLE,
)


app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H1("TextSpace", className="text-center", style={"padding-top": "1rem"}),
            width=12
        )
    ),

    dbc.Row(
        [
            dbc.Col(sidebar),
            dbc.Col(dcc.Graph(id='3d-plot', figure={}), width=8)
        ]
    ),

])

@app.callback(
    Output('3d-plot', 'figure'),
    Input('embedding-type', 'value')
)

def update_plot(embedding_type):
    if embedding_type == "emotion":
        return fig_emotion
    elif embedding_type == "bow":
        return fig_bow
    elif embedding_type == "topic":
        return fig_topic
    else:
        return fig_gpt2

@app.callback(
    Output('text-area', 'value'),
    Input('3d-plot', 'clickData')
)

def update_text(clickData):
    if clickData is None:
        return "Click on a point to see the text"
    else:
        title = clickData['points'][0]['text']
        
        # get the full text
        full_text = df[df['title'] == title]["text_full"].values[0] 

        return_text = title + "\n\n" + full_text
        return return_text
    




if __name__ == '__main__':
    print("Running Dash app...")
    print("Go to the link provided in the terminal when the app is done opening.")
    print("Press CTRL+C to stop the app.")
    app.run_server(debug=False)