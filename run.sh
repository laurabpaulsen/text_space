# activate environment
source ./env/bin/activate

# scrape songs
echo "[INFO]: Scraping danish song lyrics..."
python examples/src/scrape_songs.py

# preprocess songs
echo "[INFO]: Preparing dataframe with song lyrics..."
python examples/src/preprocess_lyrics.py

# Use TextSpace to create 3d visualization of the lyrics using different embeddings
embeddings="emotion gpt2 topic bow"
for embedding in $embeddings; do
echo "[INFO]:Creating 3d visualization of the lyrics using $embedding embeddings..."
    python examples/src/text_space.py --embedding_type $embedding
done



