import pandas as pd
import numpy as np
from collections import defaultdict, Counter

from nltk.corpus import stopwords
# from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

import string
import pickle

import spacy
#from spacymoji import Emoji

# Read in reviews
reviews = pd.read_csv('./data/reviews_final.csv')

nlp = spacy.load('en_core_web_lg')

#log file path
log_file = open("./data/log_output.txt", "a")

# Group Reviews
# bad_test = reviews[(reviews['rating'] <= 2) & (reviews['id'] == 281796108)]

bad_reviews = reviews[reviews['rating'] <= 2]  # Select all reviews under or equal to 2 stars
bad_reviews = bad_reviews[['id', 'review']]  # Drop columns not used
bad_reviews = bad_reviews.dropna()  # Drop NA's

# grouped = bad_reviews.groupby(['id']).sum()  # Group by ID, concat the reviews
bad_grouped = bad_reviews.groupby(['id'])

good_reviews = reviews[reviews['rating'] > 3]  # Select all reviews over 3 stars
good_reviews = good_reviews[['id', 'review']]  # Drop columns not used
good_reviews = good_reviews.dropna()  # Drop NA's

good_grouped = good_reviews.groupby(['id'])

# Preprocessing Function
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS #import the spacy stop words library
customize_stop_words = ['chrome', 'safari', 'ios', 'app', ' ', '..', 'google', 'tabs', 'open', 'closed', 'browser', 'use', 'game']  # set of custom stop words

STOPWORDS = set(stopwords.words('english') + list(spacy_stopwords) + list(customize_stop_words))
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "”"]
ESCAPE_CHAR = ['\n', '\n\n']

#emoji_handler = Emoji(nlp) #calling the emoji function from spacy and adding the nlp object
#nlp.add_pipe(emoji_handler, first=True)


def preprocess_tokens(token):
    print("token TEST: " + token.text + " || "+ str(token.pos_), file=log_file)
    # Check latin character
    try:
        token.text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        print("UnicodeDecodeError token TEST: " + token.text , file=log_file)
        return False
    # Stopwords/Symbols/\n
    if token.text in STOPWORDS or token.text.lower() in STOPWORDS or token.text.upper() in STOPWORDS:
        print("STOPWORDS token TEST: " + token.text, file=log_file)
        return False
    elif token.text in SYMBOLS:
        print("SYMBOLS token TEST: " + token.text , file=log_file)
        return False
    elif token.text in ESCAPE_CHAR:
        print("ESCAPE_CHAR token TEST: " + token.text , file=log_file)
        return False
    elif token.like_num:
        print("NUMBER CHECK token TEST: " + token.text + " || " + str(token.like_num) , file=log_file)
        return False
    elif token.pos_ == 'PROPN':
        print("PROPER NOUN CHECK token TEST: " + token.text + " || " + str(token.pos_) , file=log_file)
        return False
    #elif token._.is_emoji:
    #    print("Emoji token TEST: " + token.text)
    #    return False
    else:
        return True


#  ---Create Dict of tokens per ID for counts---
# Bad Tokens
bad_nlp_dict = {}
for name, group in bad_grouped:
    print("App_ID : " + str(name) , file=log_file)
    texts = group['review'].to_numpy().tolist()
    print("*** texts *** " , file=log_file)
    print(*texts, sep=", " , file=log_file)
    words = []
    bad_nlp_dict[name] = words
    pipe = nlp.pipe(texts, disable=['parser'])
    for doc in pipe:
        print("doc TEST: " + doc.text , file=log_file)
        words.extend([token.text for token in doc if preprocess_tokens(token) is True])

# Good Tokens
good_nlp_dict = {}
for name, group in good_grouped:
    texts = group['review'].to_numpy().tolist()
    words = []
    good_nlp_dict[name] = words
    pipe = nlp.pipe(texts, disable=['parser'])
    for doc in pipe:
        words.extend([token.text for token in doc if preprocess_tokens(token) is True])


# Save dictionaries to pickle files
f = open('./data/bad_dict.pkl', 'wb')
pickle.dump(bad_nlp_dict, f)
f.close()

f = open('./data/good_dict.pkl', 'wb')
pickle.dump(good_nlp_dict, f)
f.close()

# Quick visualize Look at the most common terms in a key
Counter(bad_nlp_dict[535886823]).most_common(100)

# ---Load Pickled Dict---
in_bad_file = open('./data/bad_dict.pkl', 'rb')
bad_loaded_dict = pickle.load(in_bad_file)

in_good_file = open('./data/good_dict.pkl', 'rb')
good_loaded_dict = pickle.load(in_good_file)

# Export to CSV for R WordCloud loading
df = pd.DataFrame([bad_loaded_dict]).transpose()
df['words'] = df[0]
df = df[['words']]
pd.DataFrame.to_csv(df, './data/bad_terms_df.csv')

df = pd.DataFrame([good_loaded_dict]).transpose()
df['words'] = df[0]
df = df[['words']]
pd.DataFrame.to_csv(df, './data/good_terms_df.csv')
