from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd

from plot3D import plot_embeddings_3d
from data import TextSpaceData

from pathlib import Path

def prep_data_dash(data_path:Path):
    """
    Prepares the data for the dash app by creating a dictionary of TextSpaceData objects

    Parameters
    ----------
    data_path : str
        Path to the data file
    
    Returns
    -------
    TextSpace_dict : dict
        Dictionary of TextSpaceData objects
    """
    # read plotly data
    df = pd.read_csv(data_path)

    load_figure_template("LUX")

    TextSpace_dict = {}

    for embedding_type in ["emotion", "gpt2", "bow", "topic"]:
        # create TextSpaceData object
        TextSpace_dict[embedding_type] = TextSpaceData(df, embedding_type=embedding_type)

    return TextSpace_dict

def dropdown_options(TextSpace_dict):
    """
    Returns the dropdown options for the dash app
    """

    options = []
    for embedding_type in TextSpace_dict.keys():
        options.append({'label': embedding_type, 'value': embedding_type})

    return options

def dict_plot_embeddings_3d(TextSpace_dict):
    """
    
    """
    plot_dict = {}
    for embedding_type in TextSpace_dict.keys():
        fig = plot_embeddings_3d(TextSpace_dict[embedding_type])
        plot_dict[embedding_type] = fig

    return plot_dict

def get_dash_app(data_path=None):
    """
    Returns a Dash app for the project

    Parameters
    ----------
    data_path : str
        Path to the data file

    Returns
    -------
    app : Dash app
        Dash app for the project
    """
    TextSpaceData_dict = prep_data_dash(data_path)
    
    load_figure_template("LUX")

    # dropdown options
    options = dropdown_options(TextSpaceData_dict)

    # create figures
    plot_dict = dict_plot_embeddings_3d(TextSpaceData_dict)


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
                        options=options,
                        value=options[0]['value'],
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
        return plot_dict[embedding_type]

    @app.callback(
        Output('text-area', 'value'),
        Input('3d-plot', 'clickData')
    )

    def update_text(clickData):
        if clickData is None:
            return "Click on a point to see the text"
        else:
            df = TextSpaceData_dict["emotion"].df
            text_col = TextSpaceData_dict["emotion"].text_col

            title = clickData['points'][0]["text"]
            # get the full text
            full_text = df[df['title'] == title][text_col].values[0] 

            return_text = title + "\n\n" + full_text
            return return_text
    
    return app
        



