import plotly.express as px
from data import TextSpaceData

def plot_embeddings_3d(data:TextSpaceData):
    # plotly
    fig = px.scatter_3d(data.get_plot_data(), x='x', y='y', z='z', 
                        color='author', hover_name=data.author_col, 
                        text=data.title_col,
                        size_max=10, opacity=0.7)

    fig.update_traces(textposition='top center')

    # only show the title when hovering over a point (not the author or the coordinates)
    fig.update_traces(hovertemplate="<b>%{text}</b><br><br>",
                        selector=dict(type='scatter3d')) 
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="serif"))

    
    fig.update_layout(
        height=800,
        font_family="serif",
        font_size=18,
        title_font_family="serif",
        title_font_size=30,
        legend_title_font_size=20,
        legend_font_size=16,

        # remove ticks and background
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showticklabels=False, title="")
            )

    )


    
    return fig