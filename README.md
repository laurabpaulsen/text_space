# TextSpace
This repository holds the code for the 5th and final project for Language Analytics (S2023). It contains a local Python package called `TextSpace` which allows for interactive exploration of a corpus of text documents. Futhermore it contains a demo of the package using a corpus of danish song lyrics, as well as a script for initialising a dash app for interactive exploration of the lyrics in embedding space projected unto 3 principal components.

![](examples/example.gif)

## Description of the data
To demonstrate the functionality of the package as collection of lyrics from danish songs from 10 artists were scraped from Genius.com. Up to 5 songs from each artist were scraped, but only the danish songs were saved. 

| Artist | Number of songs |
| ----------------- | -: |
| Anne Linnet       | 5 |
| Kim Larsen        | 5 |
| Guldimund         | 5 |
| Lis Sørensen      | 4 |
| Medina            | 3 |
| Nephew            | 3 |
| Sannne Salomonsen | 5 |
| The Minds of 99   | 4 |
| Zar Paulo         | 5 |
| **Total**         | **39**|

## Usage and reproducibility
The code was developed and tested on a MacBook Pro with macOS (Ventura v3.3., python v3.10.7). Furhermore, the pipeline was tested on [uCloud](https://cloud.sdu.dk/app/dashboard) (Ubuntu v22.10m, Coder python v1.77.3, python v3.10.7). Here all code runs as expected, except for the dash app which does not connect correctly to the host.


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
    - Use TextSpace to create 3d visualization of the lyrics using BoW, GPT2, latent dirichlet allocation and emotion embeddings

**Note:** As the repository holds all the files created by running the script you can skip running the following command if you just want to run the dash app.
```
bash run.sh
```

5. To run the dash app, run the following command
```
source env/bin/activate
python examples/src/dash_app.py
```


### Using your own corpus
If you want to display the embeddings of your own corpus, you can do so by simply providing a dataframe with the following columns:
- title
- author
- text_full

The `text_full` column should contain the full text of the document, while the `title` and `author` columns should contain the title and author of the document respectively. The `title` and `author` columns are used for labeling the documents in the visualization. The `text_full` column is used for calculating the embeddings. All columns should contain strings.

Place the dataframe in the `data` folder and name it "plotly_data.csv". Then you can both run `run.sh` or the `dash_app.py` script to visualize the embeddings of your own corpus.

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
│   │   ├── preprocess_lyrics.py
│   │   ├── scrape_songs.py
│   │   └── text_space.py
│   └── ...
├── TextSpace                                   <- Local python package
│   ├── __init__.py
│   ├── dash_application.py
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
To display the results of the example functionality of the package using the danish songs, follow the following links:
- [Emotion Embeddings](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_emotion.html)
- [GPT2 Embeddings](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_gpt2.html)
- [BoW Embeddings](http://htmlpreview.github.io/?https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_bow.html)
- [Latent dirichlet allocation](http://htmlpreview.github.io/??https://github.com/laurabpaulsen/text_space/blob/main/examples/plotly_topic.html)

These can also be found in the `examples` folder of the repository. 

Additionally the dash app provides an interactive way of exploring the corpus. It allows you to switch seemlessly between the types of embeddings and display the full text by clicking the songs. 