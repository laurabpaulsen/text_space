"""
Uses a pretrained model as a feature extractor. PCA is used to reduce the dimensionality of the embeddings to 3D. The 3D embeddings are then plotted using plotly. 

"""
import numpy as np
from pathlib import Path
from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch
import re
import plotly.express as px
from sklearn.decomposition import PCA
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type = str, default="gpt2")

    return parser.parse_args()

def load_txts(directory: Path):
    """
    Loads all text files in a directory and returns a list of strings

    Parameters
    ----------
    directory : Path
        The directory to load the text files from

    Returns
    -------
    txts : list
        A list of strings containing the text from the text files
    filenames : list
        A list of strings containing the filenames of the text filess
    """
    txts = []
    filenames = []

    for file in directory.iterdir():
        with open(file, 'r') as f:
            txts.append(f.read())
        
        filenames.append(file.name)

    return txts, filenames
    
def preprocess_lyrics(lyrics: list):
    for i, lyric in enumerate(lyrics):
        #remove identifiers like chorus, verse, etc
        lyric = re.sub(r'(\[.*?\])*', '', lyric)

        # replace double linebreaks with single linebreaks
        lyric = re.sub('\n\n', '\n', lyric)  # Gaps between verses

        lyric = lyric.lower()
        # Remove everything before the first time it says "lyrics" (title of the song, contributor, etc.)
        start = lyric.find("lyrics")+7
       
        # Remove suggestions at the end
        stop = lyric.find("you might also like")
        
        lyrics[i] = lyric[start:stop]
        
    return lyrics


def load_model(model_name):
    if model_name.lower() == "gpt2":
        from transformers import GPT2LMHeadModel, GPT2Tokenizer

        # load tokenizer and model
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2LMHeadModel.from_pretrained('gpt2')

    elif model_name.lower() == "mt5":
        from transformers import MT5Tokenizer, MT5ForConditionalGeneration

        tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")
        model = MT5ForConditionalGeneration.from_pretrained("google/mt5-small")

    return model, tokenizer

def plot_embeddings_3d(embeddings, titles, authors, texts, savepath = None):
    pca = PCA(n_components=3)
    embeddings_3d = pca.fit_transform(embeddings)

    texts = [text[:1000] + "..." for text in texts]
    
    # replace \n with <br> for plotly
    texts = [text.replace("\n", "<br>") for text in texts]

    # dataframe for plotly
    data = {'x':embeddings_3d[:,0], 'y':embeddings_3d[:,1], 'z':embeddings_3d[:,2], 'title':titles, 'author':authors, 'text':texts}
    df = pd.DataFrame(data)

    # plotly
    fig = px.scatter_3d(df, x='x', y='y', z='z', color='author', hover_name='author', hover_data=['text'], text='title')

    fig.update_traces(textposition='top center', 
                      hovertemplate='Title: %{text}<br>' +
                                    'Lyrics: %{customdata[0]}<br>'
                      )
    
    fig.update_layout(
        height=800,
        title_text='SongScape',
        font_family="serif"
    )

    # no bounding box
    fig.update_layout(
        scene = dict(
            xaxis = dict(showbackground=False, showticklabels=False),
            yaxis = dict(showbackground=False, showticklabels=False),
            zaxis = dict(showbackground=False, showticklabels=False)
            )
    )
    
    
    fig.show()
    if savepath:
        fig.write_image(savepath)



def main():
    path = Path(__file__)

    lyrics, filenames = load_txts(path.parents[1] / "data" / "lyrics") 

    lyrics = lyrics[:100]
    filenames = filenames[:100]

    lyrics = preprocess_lyrics(lyrics)

    model, tokenizer = load_model("gpt2")

    # tokenize lyrics
    tokenized_lyrics = [tokenizer.encode(lyric, truncation=True) for lyric in lyrics]
    
    embeddings = []

    # loop through tokenized lyrics and get their embeddings
    for lyric in tokenized_lyrics:

        # pad sequence with max length of 1024
        lyric_padded = pad_sequences([lyric], maxlen=1024)


        # convert to torch tensor
        lyric_padded = torch.tensor(lyric_padded)

        # attention mask
        attention_mask = torch.where(lyric_padded != 0, 1, 0)

        # get embedding
        embedding = model(input_ids=lyric_padded, attention_mask = attention_mask, return_dict=True, output_hidden_states=True)

        # get last layer of embeddings (last hidden state)
        embedding = embedding.hidden_states[-1][:,0,:].detach().numpy().squeeze()

        # append to list of embeddings
        embeddings.append(embedding)

    # convert list of embeddings to numpy array
    embeddings = np.array(embeddings)


    # prepare titles for plotting
    artists = [filename.split("-")[0] for filename in filenames]
    titles = [filename[:-4].replace("_"," ") for filename in filenames]
    titles = [title.replace("-"," - ") for title in titles]

    # plot embeddings in 3D
    plot_embeddings_3d(embeddings, titles, artists, lyrics, savepath = path.parents[1] / "fig" / "embeddings_3d.png")


if __name__ == "__main__":
    main()
                     