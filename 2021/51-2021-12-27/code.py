import string
import pandas as pd
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.pipeline import Pipeline

lyrics = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-12-14/lyrics.csv', encoding = "ISO-8859-1")

lyrics['tokens'] = lyrics.line.apply(lambda x : list(parser(x)))

song_words = lyrics.explode('tokens').groupby(["song_name", "tokens"])["tokens"].count()

total_words = song_words.groupby("song_name")[""]





# Create our list of punchuationmarks
punctuations = string.punctuation

# Create our list of stop words
nlp = spacy.load('en_core_web_sm')
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# Load English tokenizer, tagger, parser, NER and word vector
parser = English()

# Creating our tokenzer function
def spacy_tokenizer(sentence):
    """This function will accepts a sentence as input and processes the sentence into tokens, performing lemmatization, 
    lowercasing, removing stop words and punctuations."""
    
    # Creating our token object which is used to create documents with linguistic annotations
    mytokens = parser(sentence)
    
    # lemmatizing each token and converting each token in lower case
    # Note that spaCy uses '-PRON-' as lemma for all personal pronouns lkike me, I etc
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    
    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations]
    
    # Return preprocessed list of tokens
    return mytokens    




# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        """Override the transform method to clean text"""
        return [clean_text(text) for text in X]
    
    def fit(self, X, y= None, **fit_params):
        return self
    
    def get_params(self, deep= True):
        return {}

# Basic function to clean the text
def clean_text(text):
    """Removing spaces and converting the text into lowercase"""
    return text.strip().lower()    




bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range = (1,1))

tfidf_vector = TfidfVectorizer(tokenizer = spacy_tokenizer)

# Create pipeline using Bag of Words
pipe = Pipeline ([("cleaner", predictors()),
                 ("vectorizer", bow_vector),
                 ("classifier", classifier)])
                 
