# activate environment
#source ./env/bin/activate

# scrape songs
echo "[INFO]: Scraping danish song lyrics..."
python src/scrape_songs.py

# preprocess songs
echo "[INFO]: Preparing dataframe with song lyrics..."
python src/preprocess_lyrics.py

# Use TextSpace to create 3d visualization of the lyrics (using both emotion and gpt2 embeddings)
embeddings="emotion gpt2"
for embedding in $embeddings; do
echo "[INFO]:Creating 3d visualization of the lyrics using $embedding embeddings..."
    python src/text_space.py --embedding_type $embedding
done



