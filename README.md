# TextSpace
This repository holds the code for the 5th and final project for Language Analytics (S2023). It contains a local Python package called `TextSpace` which allows for interactive exploration of a corpus of text documents.

## Description of the data
To demonstrate the functionality of the package as collection of lyrics from danish songs were scraped from Genius.com.

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


## Repository structure


## Results

To display the emotion embeddings, follow this [link]()
To display the gpt2 embeddings, follow this [link]()