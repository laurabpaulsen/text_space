# TextSpace
This repository holds the code for the 5th and final project for Language Analytics (S2023). It contains a local Python package called `TextSpace` which allows for interactive exploration of a corpus of text documents. Futhermore it contains a demo of the package using a corpus of danish song lyrics, as well as a script for initialising a dash app for visualizing the embeddings of the lyrics.

![](examples/example.gif)
## Description of the data
To demonstrate the functionality of the package as collection of lyrics from danish songs from 10 artists were scraped from Genius.com.

## Usage and reproducibility
To reproduce the results of the example functionality of the package using the danish songs, follow the steps below. All terminal commands should be run from the root directory of the repository.

1. Clone the repository
2. Aquire a Genius API key and paste it into the `TOKEN.txt` file
3. Create a virtual environment and install requirements
```
bash setup.sh
```
4. Run the `run.sh` script to:
    - Scrape danish song lyrics from Genius
    - Preprocess the lyrics and prepare dataframe with appropriate columns for TextSpace
    - Use TextSpace to create 3d visualization of the lyrics (using both emotion and gpt2 embeddings)
```
bash run.sh
```

5. To run the dash app, run the following command
```
source env/bin/activate
python src/dash_app.py
```


### Using your own corpus
If you want to display the embeddings of your own corpus, you can do so by simply providing a dataframe with the following columns:
- title
- author
- text_full

The `text_full` column should contain the full text of the document, while the `title` and `author` columns should contain the title and author of the document respectively. The `title` and `author` columns are used for labeling the documents in the visualization. The `text_full` column is used for calculating the embeddings. The `text_full` column should be a string.

Place the dataframe in the `data` folder and name it "plotly_data.csv". Then you can both run the `run.sh` script or the `dash_app.py` script to visualize the embeddings of your own corpus.

## Repository structure
```
├── data 
│   ├── plotly_data.csv
│   ├── lyrics
│   │   ├── Anne_Linnet-Barndommens_Gade.txt
│   │   └── ...
├── env                                         <- Not included in repo
├── examples
│   ├── src
│   │   ├── dash_app.py
│   │   └── ...
│   ├── plotly_bow.html
│   └── ...
├── TextSpace                                   <- Local python package
│   ├── __init__.py
│   ├── data.py
│   └── plot3D.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.sh
├── setup.sh
└── TOKEN.txt                                   <- Remember to add your own Genius API key

```


## Results
To display the emotion embeddings, follow this [link](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_emotion.html)
To display the gpt2 embeddings, follow this [link](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_gpt2.html)
To display the bow embeddings, follow this [link](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_bow.html)
