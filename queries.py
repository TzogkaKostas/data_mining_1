import pandas as pd
from pandas import DataFrame, concat
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def create_wordcloud(name, string):
	wordcloud = WordCloud(background_color='white', include_numbers=True).generate(string)
	fig = plt.figure(1)
	plt.imshow(wordcloud)
	plt.axis('off')
	plt.show()
	fig.savefig(name, dpi=1200)



df = pd.read_csv("../data/merged.csv")

# query 1
# print("Most common room type is:", df['room_type'].value_counts().idxmax())

# query 3
# res = df['neighbourhood'].value_counts().nlargest(5).index
# print("The 5 most reviewed neighborhoods:\n" + '\n'.join(res))

# query 5
df1 = pd.read_csv("../data/febrouary/updated_feb.csv")
df2 = pd.read_csv("../data/march/updated_march.csv")
df3 = pd.read_csv("../data/april/updated_april.csv")
feb = df1['neighbourhood'].value_counts().to_string()
march = df2['neighbourhood'].value_counts().to_string()
april = df3['neighbourhood'].value_counts().to_string()
print("\t\tFebruary\n%s\n\t\tMarch\n%s\n\t\tApril\n%s" % (feb, march, april))

# query 9
# position = df['price'].idxmax()
# print("The most expensive room type is:", df['room_type'][position])

# query 11
# create_wordcloud("wordcloud_neigh", df['neighbourhood'].dropna().to_string())
# create_wordcloud("wordcloud_transit", df['transit'].dropna().to_string())
# create_wordcloud("wordcloud_descr", df['description'].dropna().to_string())
# create_wordcloud("wordcloud_last", df['last_review'].dropna().to_string())