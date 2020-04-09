import pandas as pd
from pandas import DataFrame, concat
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from heapq import nsmallest
from operator import itemgetter
import nltk
from nltk.collocations import *
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures

def recommend(item_id, num):
	print("Recommending", num, "listings similar to ",
		temp_df[item_id == temp_df['id']]['name'].to_string())
	print("----------------------------------------------------------\n")

	best = distances[item_id]
	for t in best[0 : min(100, num)]:
		id = t[0]
		score = t[1]
		row = temp_df[id == temp_df['id']]

		name = row['name']
		description = row['description']
		print("Recommend:", name.to_string())
		print("Description:", description.to_string())
		print("(score:", score, ")\n")


def nbest_collocations(num):
	input = ' '.join(temp_df['union'])
	finder = BigramCollocationFinder.from_words(input.split())
	res = finder.nbest(nltk.collocations.BigramAssocMeasures().likelihood_ratio, num)
	for r in res:
		print(r)


df = pd.read_csv("../data/train.csv")

temp_df = df[['id', 'name', 'description']].drop_duplicates()[0 : 150]
temp_df['union'] = temp_df['name'].fillna('') + " " + temp_df['description'].fillna('')


# unigrams and bigrams
stop_words = ["word1", "word2"]
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words)
X = vectorizer.fit_transform(temp_df['union'])

# all distances between dataframe rows
distances = dict()
for (i, id1) in enumerate(temp_df['id']):
	for (j, id2) in enumerate(temp_df['id']):
		if (id1 != id2):
			score = cosine_similarity(X[i], X[j])[0][0]
			if (id1 in distances):
				distances[id1].append((id2, score))
			else:
				distances[id1] = [(id2, score)]

# for each row keep only the 100 smallest distances from the other rows
for i in temp_df['id']:
	distances[i] = nsmallest(100, distances[i], key=itemgetter(1))
 
recommend(10595, 2)

num = 10
print("The", num, "most used collocations:")
nbest_collocations(num)