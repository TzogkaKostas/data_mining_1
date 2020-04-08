import pandas as pd
from pandas import DataFrame, concat
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("../data/train.csv")
df1 = pd.read_csv("../data/febrouary/updated_feb.csv")
df2 = pd.read_csv("../data/march/updated_march.csv")
df3 = pd.read_csv("../data/april/updated_april.csv")


temp_df = df[['id', 'name', 'description']].drop_duplicates()

# res = wordcloud = WordCloud(
# 	stopwords=STOPWORDS,
# 	background_color='white', include_numbers=True) \
#     .process_text(temp_df['description'].dropna().to_string())

# # res = wordcloud.process_text(temp_df['description'].to_string())

# print(res)

vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words=STOPWORDS)
X = vectorizer.fit_transform(temp_df['description'].dropna())

my_df = pd.DataFrame(X.toarray(), columns = vectorizer.get_feature_names())
print(my_df)
print(my_df[0])


# print(vectorizer.get_feature_names())
# print(X.shape)

