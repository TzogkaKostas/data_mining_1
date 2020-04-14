import pandas as pd
from pandas import DataFrame, concat
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def create_wordcloud(name, string):
	wordcloud = WordCloud(
		stopwords=STOPWORDS,
		background_color='white', include_numbers=True).generate(string)
	wordcloud.to_file(name)
	# fig = plt.figure(1)
	# plt.imshow(wordcloud)
	# plt.axis('off')
	# plt.show()
	# fig.savefig(name, dpi=1200)


def identical_columns(df1, df2, column):
	if len(list(set(df1[column]) & set(df2[column]))) == len(df1[column]) == len(df2[column]):
		return True
	else:
		return False



df = pd.read_csv("../data/train.csv")
df1 = pd.read_csv("../data/febrouary/updated_feb.csv")
df2 = pd.read_csv("../data/march/updated_march.csv")
df3 = pd.read_csv("../data/april/updated_april.csv")

# query 1
# temp_df = df[['id', 'room_type']].drop_duplicates()
# print("The most common room type is:", temp_df['room_type'].value_counts().idxmax())


# query 3
# temp_df = df[['id', 'neighbourhood', 'number_of_reviews']].drop_duplicates()
# # for each apartment keep the maximum number of reviews
# temp_df = temp_df.groupby(['id', 'neighbourhood'], as_index=False).max()
# # for each neighbourhood get the sum of reviews. Then get the 5 largest
# temp_df = temp_df.groupby(['neighbourhood'])['number_of_reviews'].agg('sum').nlargest(5)
# print("The 5 most reviewed neighborhoods:")
# for v in temp_df.index.values:
# 	print(v)
# uncomment to print number of the most reviewed neighborhoods
# print("The 5 most reviewed neighborhoods:\n" + temp_df.to_string(header=False))

# query 4
# uniqueValues = df['neighbourhood'].unique()
# max_value = -1
# result = ""
# for i in uniqueValues:
#     # print(i)
#     temp = df.loc[df['neighbourhood'] == i, 'number_of_reviews'].sum()
#     if temp > max_value:
#         max_value = temp
#         result = i
# print(max_value, "->", result)


# query 5
# feb = df1['neighbourhood'].value_counts().to_string()
# march = df2['neighbourhood'].value_counts().to_string()
# april = df3['neighbourhood'].value_counts().to_string()
# print("Number of apartments per month")
# print("\t\tFebruary\n%s\n\t\tMarch\n%s\n\t\tApril\n%s" % (feb, march, april))


# query 7
# temp_df = df[['id', 'neighbourhood', 'room_type']].drop_duplicates()
# groupsby = temp_df.groupby('neighbourhood')

# print("The most common room type per neighbourhood:")
# for group in groupsby.groups:
	# most_common = groupsby.get_group(group)['room_type'].value_counts().idxmax()
	# print("%s: %s" % (group, most_common))

# query 8
# temp_df = df[['id', 'price', 'room_type']].drop_duplicates()
# result = temp_df.groupby('room_type').mean().nlargest(1, "price")
# print("The most expensive (based on average price) room type is:", result.index.values[0])

# query 10
# temp_df = df[['id', 'neighbourhood']].drop_duplicates()
# create_wordcloud("wordcloud_neigh.png", temp_df['neighbourhood'].dropna().to_string())

# temp_df = df[['id', 'transit']].drop_duplicates()
# create_wordcloud("wordcloud_transit.png", temp_df['transit'].dropna().to_string())

# temp_df = df[['id', 'description']].drop_duplicates()
# create_wordcloud("wordcloud_descr.png", temp_df['description'].dropna().to_string())

# temp_df = df[['id', 'last_review']].drop_duplicates()
# create_wordcloud("wordcloud_last", temp_df['last_review'].dropna().to_string())

temp_df = df[['id', 'comments']].drop_duplicates()
create_wordcloud("wordcloud_last2.png", temp_df['comments'].dropna().to_string())	

# query 12
# temp_df = df[['id', 'neighbourhood', 'number_of_reviews']].drop_duplicates()
# 
# result = temp_df.groupby(['neighbourhood'])[['id', 'number_of_reviews']].max().reset_index()
# print("The most reviewed apartment per neighbourhood:")
# print(result[['neighbourhood', 'id']].to_string(index=False))