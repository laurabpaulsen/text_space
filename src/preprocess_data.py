"""
Prepares a dataframe for the plotly visualization with the appropriate columns and data.
"""

from pathlib import Path
import pandas as pd
import argparse
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from sklearn.decomposition import PCA
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text_dir", type = str, default="data/lyrics/")

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


def find_embeddings(texts: list, model, tokenizer):
    
    tokenized_txts = [tokenizer.encode(text, truncation=True) for text in texts]
    
    embeddings = []

    # loop through tokenized lyrics and get their embeddings
    for txt in tokenized_txts:

        # pad sequence with max length of 1024
        txts_padded = pad_sequences([txt], maxlen=1024)


        # convert to torch tensor
        txts_padded = torch.tensor(txts_padded)

        # attention mask
        attention_mask = torch.where(txts_padded != 0, 1, 0)

        # get embedding
        embedding = model(input_ids=txts_padded, attention_mask = attention_mask, return_dict=True, output_hidden_states=True)

        # get last layer of embeddings (last hidden state)
        embedding = embedding.hidden_states[-1][:,0,:].detach().numpy().squeeze()

        # append to list of embeddings
        embeddings.append(embedding)

    # convert list of embeddings to numpy array
    embeddings = np.array(embeddings)

    return embeddings


def main():
    args = parse_args()
    path = Path(__file__) 

    txt_path = path.parents[1] / args.text_dir
    txts, filenames = load_txts(txt_path)

    # load tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # preprocess lyrics
    txts = preprocess_lyrics(txts)

    # get embeddings
    embeddings = find_embeddings(txts, model, tokenizer)

    # transform embeddings to 3d
    pca = PCA(n_components=3)
    embeddings_3d = pca.fit_transform(embeddings)

    # keep only the first 1000 characters of the text for plotly
    texts = [text[:1000] + "..." for text in txts]
    
    # replace \n with <br> for plotly
    texts = [text.replace("\n", "<br>") for text in texts]

    # get authors and titles
    authors = [filename.split("-")[0] for filename in filenames]
    titles = [filename[:-4].replace("_"," ") for filename in filenames]
    titles = [title.replace("-"," - ") for title in titles]

    # dataframe for plotly
    data = {'x':embeddings_3d[:,0], 'y':embeddings_3d[:,1], 'z':embeddings_3d[:,2], 'title':titles, 'author':authors, 'text':texts, 'text_full': txts}
    df = pd.DataFrame(data)

    # save dataframe
    df.to_csv(path.parents[1] / "data" / "plotly_data.csv", index=False)


if __name__ == "__main__":
    main()