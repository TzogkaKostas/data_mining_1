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

	best = distances[index]
	for t in best[0 : min(100, num)]:
		index = t[0]
		score = t[1]
		row = temp_df.iloc[index]

		name = row['name']
		description = row['description']
		print("Recommend:", name)
		print("Description:", description)
		print("(score:", score, ")\n")


def nbest_collocations(num):
	input = ' '.join(temp_df['union'])
	finder = BigramCollocationFinder.from_words(input.split())
	res = finder.nbest(nltk.collocations.BigramAssocMeasures().likelihood_ratio, num)
	for r in res:
		print(r)


df = pd.read_csv("../data/train.csv")


temp_df = df[['id', 'name', 'description']].drop_duplicates()[0: 10]
temp_df['union'] = temp_df['name'].fillna('') + " " + temp_df['description'].fillna('')


# unigrams and bigrams
stop_words = ["word1", "word2"]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words)
X = vectorizer.fit_transform(temp_df['union'])

size = temp_df.shape[0]

distances = dict()
for i in range(0, size):
	heap = []
	for j in range(i + 1, size):
		score = cosine_similarity(X[i], X[j])[0, 0]
		heappush(heap, (j, score))
		if (j in distances):
			heappush(distances[j], (i, score))
		else:
			distances[j] = []
			heappush(distances[j], (i, score))

	distances[i] = heap

# for each row keep only the 100 smallest distances from the other rows
for i in range(0, size):
	distances[i] = nsmallest(100, distances[i], key=itemgetter(1))


recommend(10595, 5)

# num = 10
# print("The", num, "most used collocations:")
# nbest_collocations(num)