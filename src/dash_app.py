"""
Using Dash to create a web app for the project
"""

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parents[1] / "TextSpace")) 
from plot3D import plot_embeddings_3d
from data import TextSpaceData


path = Path(__file__)
# read plotly data
df = pd.read_csv(path.parents[1] / 'data' / 'plotly_data.csv')

load_figure_template("LUX")
# only few points for testing
df = df.sample(10)

# create TextSpaceData object
TextSpace_emotion = TextSpaceData(df, embedding_type="emotion")
fig_emotion = plot_embeddings_3d(TextSpace_emotion)
TextSpace_gpt2 = TextSpaceData(df, embedding_type="gpt2")
fig_gpt2 = plot_embeddings_3d(TextSpace_gpt2)


app = Dash(external_stylesheets=[dbc.themes.LUX])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#ABD699",
}

sidebar = html.Div(
    [
        html.H2("Embedding type"),
        html.Hr(),

        dbc.Nav(
            [
                dcc.Dropdown(id="embedding-type",
                    options=[
                        {'label': 'Emotion', 'value': 'emotion'},
                        {'label': 'GPT2', 'value': 'gpt2'}
                    ],
                    value='emotion',
                    clearable=False,
                    style={'width': '100%'}
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2("TextSpace", className="text-center"),
            width=12)
        ),

    dbc.Row(
            [dbc.Col(sidebar, width=3),
            # insert the graph here
            dbc.Col(dcc.Graph(id='3d-plot',figure={}), width=9),
        
            #
            dcc.RadioItems(id="chosen-point",options=[],value=[]),

            ]
        ),
    

    
    # new row for displaying the lyrics
    dbc.Row(
        dbc.Col(
            dcc.Textarea(
                id="lyrics",
                value="Click on a point to see the text",
                readOnly=True,
                style={'font-size': 20, 'border': 'none','outline': 'none','background-color': '#f5f5f5'}))
        )
    

    ])





@app.callback(
    Output('3d-plot', 'figure'),
    Input('embedding-type', 'value')
)

def update_plot(embedding_type):
    if embedding_type == "emotion":
        return fig_emotion
    else:
        return fig_gpt2

# callback for table
# when clicking on a point, show the lyrics of that song in a table
@app.callback(
    Output('lyrics', 'value'),
    Input('3d-plot', 'clickData')
)

def update_table(clickData):
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
    app.run_server(debug=True)