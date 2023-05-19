import plotly.express as px
from data import TextSpaceData

def plot_embeddings_3d(data:TextSpaceData):
    # plotly
    fig = px.scatter_3d(data.get_plot_data(), x='x', y='y', z='z', 
                        color='author', hover_name=data.author_col, 
                        hover_data=[data.text_col], text=data.title_col,
                        size_max=10, opacity=0.7)

    fig.update_traces(textposition='top center', 
                      hovertemplate='Title: %{text}<br>' +
                                    'Lyrics: %{customdata[0]}<br>'
                      )
    
    fig.update_layout(
        height=800,
        title_text="TextSpace" + " " + data.embedding_type,
        font_family="serif",
        font_size=18,
        title_font_family="serif",
        title_font_size=30,
        legend_title_font_size=20,
        legend_font_size=16,
        scene = dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    return fig
