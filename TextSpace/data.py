import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

# data class for TextSpace
class TextSpaceData:
    def __init__(self, df, author_col = "author", text_col = "text", title_col = "title", embedding_type = "gpt2"):
        """
        The TextSpaceData class is used to prepare data for the TextSpace visualization. It takes a dataframe as input and prepares it for the visualization by extracting the embeddings and performing PCA on them.

        Parameters
        ----------
        df : pandas dataframe
            A pandas dataframe containing the data
        author_col : str
            The name of the column containing the author names. Default is "author"
        text_col : str
            The name of the column containing the texts. Default is "text"
        title_col : str
            The name of the column containing the titles. Default is "title"
        embedding_type : str
            The type of embeddings to use. Either 'gpt2' or 'emotion'. Default is 'gpt2'
        
        Raises
        ------
        ValueError
            If the dataframe does not contain the specified columns or if the columns contain NaN values
        """
        self.df = df
        self.author_col = author_col
        self.text_col = text_col
        self.title_col = title_col
        self.embedding_type = embedding_type

        # check that the dataframe has the correct columns
        for col in [self.author_col, self.text_col, self.title_col]:
            self._check_col(col)

        # prepare pca components for plotly visualization
        self.pca = self.get_pca(self.embedding_type)

    def _check_col(self, col):
        """
        Checks that the dataframe has the correct columns
        """
        if col not in self.df.columns:
            raise ValueError(f"Column '{col}' not in dataframe")
        
        if self.df[col].isnull().values.any():
            raise ValueError(f"Column '{col}' contains NaN values")
    
    def get_gpt2_embeddings(self):
        """
        Gets the embeddings for a list of texts using GPT2 model

        Returns
        -------
        embeddings : numpy array
            A numpy array containing the embeddings for the texts
        """
        # import gpt2 tokenizer and model
        from transformers import GPT2Tokenizer, GPT2Model
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        import torch

        # load tokenizer and model
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        model = GPT2Model.from_pretrained('gpt2')

        tokenized_txts = [tokenizer.encode(text, truncation=True) for text in self.df[self.text_col]]

        embeddings = []

        # loop through tokenized texts and get their embeddings
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
    
    def get_emotion_embeddings(self):
        """
        Classifies the texts into 6 emotions using the emotion-english-distilroberta-base model and returns the embeddings
        """
        from transformers import pipeline
        
        nlp = pipeline("text-classification", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    top_k=None)

        emotion_labels = ['neutral', 'disgust', 'anger', 'fear', 'sadness', 'joy', 'surprise']
        data = pd.DataFrame(columns = emotion_labels)

        for i, txt in enumerate(self.df[self.text_col]):
            emotion_scores = nlp(txt[:512])

            # get emotion scores
            for emotion_score in emotion_scores[0]:
                data.loc[i, emotion_score['label']] = emotion_score['score']


        embeddings = np.array(data)
        
        return embeddings.transpose()

    def get_bow_embeddings(self):
        """
        Gets the embeddings for a list of texts using bag-of-words

        Returns
        -------
        embeddings : numpy array
            A numpy array containing the embeddings for the texts
        """
        from sklearn.feature_extraction.text import CountVectorizer

        # initialize count vectorizer
        vectorizer = CountVectorizer()

        # fit and transform texts
        embeddings = vectorizer.fit_transform(self.df[self.text_col])

        # convert to numpy array
        embeddings = embeddings.toarray()

        return embeddings
    
    def get_pca(self, embedding_type, n_components = 3):
        """
        Performs PCA on the embeddings

        Parameters
        ----------
        embedding_type : str
            The type of embeddings to use. Either 'gpt2' or 'emotion'
        n_components : int
            The number of components to keep

        Returns
        -------
        pca : PCA object
            A PCA object
        """
        if embedding_type == "gpt2":
            embeddings = self.get_gpt2_embeddings()
        elif embedding_type == "emotion":
            embeddings = self.get_emotion_embeddings()
        elif embedding_type == "bow":
            embeddings = self.get_bow_embeddings()
        else:
            raise ValueError("embedding_type must be either 'gpt2' or 'emotion'")
        
        pca = PCA(n_components = n_components)
        pca.fit(embeddings)

        return pca
    
    def get_plot_data(self):
        """
        Returns the dataframe with the pca components
        """
        data = self.df.copy()

        # add columns with pca components
        new_dat = {"x": self.pca.components_[0], "y": self.pca.components_[1], "z": self.pca.components_[2]}
        pca_data = pd.DataFrame(new_dat)

        data = pd.concat([data, pca_data], axis = 1)

        return data






