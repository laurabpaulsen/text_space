"""
Prepares a dataframe for the plotly visualization with the appropriate columns and data.

Author: Laura Bock Paulsen (202005791@post.au.dk)
"""

from pathlib import Path
import pandas as pd
import argparse
import re

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
    """
    Preprocesses a list of lyrics by removing identifiers like chorus, verse, etc. and suggestions at the end

    Parameters
    ----------
    lyrics : list
        A list of strings containing the lyrics to preprocess

    Returns
    -------
    lyrics : list
        A list of strings containing the preprocessed lyrics
    """
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


def main():
    args = parse_args()
    path = Path(__file__) 

    txt_path = path.parents[2] / args.text_dir
    txts, filenames = load_txts(txt_path)

    # preprocess lyrics
    txts = preprocess_lyrics(txts)

    # keep only the first 1000 characters of the text for plotly
    texts = [text[:1000] + "..." for text in txts]
    
    # replace \n with <br> for plotly
    texts = [text.replace("\n", "<br>") for text in texts]

    # get authors and titles
    authors = [filename.split("-")[0] for filename in filenames]
    titles = [filename[:-4].replace("_"," ") for filename in filenames]
    titles = [title.replace("-"," - ") for title in titles]

    # dataframe for plotly
    data = {'title':titles, 'author':authors, 'text':texts, 'text_full': txts}
    df = pd.DataFrame(data)

    # save dataframe
    df.to_csv(path.parents[2] / "data" / "plotly_data.csv", index=False)


if __name__ == "__main__":
    main()