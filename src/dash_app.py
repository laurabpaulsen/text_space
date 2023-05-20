"""
Using Dash to create a web app for the project
"""

from dash import Dash, html, dash_table, dcc, dependencies, Output, Input
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parents[1] / "TextSpace")) 
from plot3D import plot_embeddings_3d
from data import TextSpaceData


path = Path(__file__)
# read plotly data
df = pd.read_csv(path.parents[1] / 'data' / 'plotly_data.csv')

# only few points for testing
#df = df.sample(5)

# create TextSpaceData object
TextSpace_emotion = TextSpaceData(df, embedding_type="emotion")
fig_emotion = plot_embeddings_3d(TextSpace_emotion)
TextSpace_gpt2 = TextSpaceData(df, embedding_type="gpt2")
fig_gpt2 = plot_embeddings_3d(TextSpace_gpt2)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(className='row', children='TextSpace'),

    html.Hr(),

    dcc.RadioItems(
        id='embedding-type',
        options=[
            "emotion", "gpt2"
        ],
        value='emotion'
    ),

    html.Div(className='row', children = [
        html.Div(className='eight columns', children = [
            dcc.Graph(
                id='3d-plot',
                figure={})
            ]),

        dcc.RadioItems(
            id="chosen-point",
            options=[],
            value=[]
        ),
        
        # a bit less wide than the graph
        html.Div(className='four columns', children = [
            dcc.Textarea(
                id="lyrics",
                value="Click on a point to see the text",
                style={'width': '100%', 'height': 700, 'font-size': 20, 'font-family': 'serif'})
        ]),

    ])
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
    app.run_server(debug=True)