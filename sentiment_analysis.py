from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib

import spacy

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from textblob import TextBlob

import pandas as pd
import numpy as np

# Read in reviews
reviews = pd.read_csv('reviews_final.csv')

# Vader
test = reviews.iloc[0]["review"]
sid = SentimentIntensityAnalyzer()

# TextBlob
tb = TextBlob(test)
tb.sentiment_assessments

# Most Common Terms in bad reviews
stop_words = set(stopwords.words('english'))

bad_test = reviews[(reviews['rating'] <= 2) & (reviews['id'] == 281796108)]
bad_test['words'] = bad_test['review'].map(word_tokenize)
bad_test['stop'] = bad_test['words'].apply(lambda x: [w for w in x if w not in stop_words])
freq = nltk.FreqDist(sum(bad_test['stop'], []))
freq.plot(20)

#Spacy