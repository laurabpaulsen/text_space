# activate environment
source ./env/bin/activate

# scrape songs
echo "[INFO]: Scraping danish song lyrics..."
python src/scrape_songs.py

# preprocess songs
echo "[INFO]: Preparing dataframe with song lyrics..."
python src/preprocess_songs.py

# Use TextSpace to create 3d visualization of the lyrics (using both emotion and gpt2 embeddings)
echo "[INFO]: Creating 3d visualization of the lyrics..."

embeddings="emotion gpt2"
for embedding in $embeddings; do
    python src/textspace.py --embedding_type $embedding
done

python src/textspace.py


