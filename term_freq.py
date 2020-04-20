import pandas as pd
from pandas import DataFrame, concat
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from heapq import heappush, nsmallest
from operator import itemgetter
import nltk
from nltk.collocations import *
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
import heapq
import numpy as np
from scipy.sparse.linalg import LinearOperator
from scipy.sparse.linalg import norm
from scipy.sparse import csr_matrix
import scipy


def recommend(item_id, num):
	index = temp_df.index[temp_df['id'] == item_id].tolist()[0]
	print("Recommending", num, "listings similar to ",
		temp_df.iloc[index]['name'])
	print("----------------------------------------------------------\n")

	best = similarities[index]
	for t in best[::-1][1:min(100, num + 1)]:
		index = t[0]
		score = t[1]
		row = temp_df.iloc[index]

		name = row['name']
		description = row['description']
		print("Recommend:", name)
		print("Description:", description)
		print("(score:%f)\n" % score)


def nbest_collocations(num):
	input = ' '.join(temp_df['union'])
	finder = BigramCollocationFinder.from_words(input.split())
	res = finder.nbest(nltk.collocations.BigramAssocMeasures().likelihood_ratio, num)
	for r in res:
		print(r)


df = pd.read_csv("../data/train.csv")
temp_df = df[['id', 'name', 'description']].drop_duplicates(subset='id')
temp_df['union'] = temp_df['name'].fillna('') + " " + temp_df['description'].fillna('')

# unigrams and bigrams
import warnings
warnings.filterwarnings('ignore') 
stop_words = [u'minute',u'right',u'two',u'square meter',u'1st',u'2nd',u'3rd',u'4th',u'5th',
u'floor',u'κοντά σε',u'city',u'place close',u'space',u'top floor',
u'square meter',u'th',u'penthouse',u'room',u'house',u'bedroom',u'sq',u'welcome',
u'Welcome',u'studio',u'area',u'one',u'sqm',u'near',u'heart',u'recently',u'home',
u'fully',u'metro',u'center',u'central',u'μου',u'είναι',u'situated',u'located',
u'Athen',u'Athens',u'apartment',u'flat'] + list(STOPWORDS)
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words)
X = vectorizer.fit_transform(temp_df['union'])

_similarities = cosine_similarity(X)

n_best = 100
size = temp_df.shape[0]
# for each row keep only the n_best most similar from the other rows
similarities = dict()
for (i, row) in enumerate(_similarities):
	idx = np.argsort(-row)
	similarities[i] = []
	for j in range(n_best):
		similarities[i] = [(idx[j], row[idx[j]])] + similarities[i]


recommend(10595, 2)

# num = 10
# print("The", num, "most used collocations:")
# nbest_collocations(num)