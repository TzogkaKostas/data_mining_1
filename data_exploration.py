import pandas as pd
import sys
from pandas import DataFrame, concat
import numpy as np

def has_empty_cell(df, column):
	for cell in df[column]:
		if (pd.isnull(cell)):
			return True
	return False


# for 'id' column
def identical_ids(df1, df2, column):
	if len(list(set(df1[column]) & set(df2[column]))) == len(df1[column]) == len(df2[column]):
		return True
	else:
		return False


def identical_columns(df1, df2, column):
	for ((index, row),(index2, row2)) in zip(df1.iterrows(), df2.iterrows()):
		if (row[column] != row2[column] and not pd.isnull(row[column]) 
				and not pd.isnull(row2[column])):
			return True
	return False

# check if we can fill null last_review values
def is_last_review_there():
	input = [(df1, df14, df15), (df1, df24, df25), (df3, df34, df35)]
	for (lis, rev, rev0) in input:
		for (index, row) in lis.iterrows():
			if (pd.isnull(row['last_review'])):
				if (row['id'] in rev or row['id'] in rev):
					return True
	return False

def get_empty_columns(df, columns):
	cols_with_null = []
	for c in columns:
		if has_empty_cell(df, c):
			cols_with_null.append(c)
	return cols_with_null

def get_sharable_columns(columns):
	dfs = [(df1, df12, df13, df14, df15),
		(df2, df22, df23, df24, df25),
		(df3, df32, df33, df34, df35)]
	sharable_cols = set()
	for (dfx, dfx2, dfx3, dfx4, dfx5) in dfs:
		cols_with_null = get_empty_columns(dfx, columns)
		for c in cols_with_null:
			if c in dfx2.columns or c in dfx3.columns or c in dfx4.columns or c in dfx5.columns:
				sharable_cols.add(c)
	return sharable_cols

data_path = "../data/"

listings_feb = data_path + "febrouary/listings.csv"
listings0_feb = data_path + "febrouary/listings0.csv"
calendar_feb = data_path + "febrouary/calendar.csv"
reviews_feb = data_path + "febrouary/reviews.csv"
reviews0_feb = data_path + "febrouary/reviews0.csv"

listings_march = data_path + "march/listings.csv"
listings0_march = data_path + "march/listings0.csv"
calendar_march = data_path + "march/calendar.csv"
reviews_march = data_path + "march/reviews.csv"
reviews0_march = data_path + "march/reviews0.csv"

listings_apr = data_path + "april/listings.csv"
listings0_apr = data_path + "april/listings0.csv"
calendar_apr = data_path + "april/calendar.csv"
reviews_apr = data_path + "april/reviews.csv"
reviews0_apr = data_path + "april/reviews0.csv"


df1 = pd.read_csv(listings_feb)
df12 = pd.read_csv(listings0_feb)
df13 = pd.read_csv(calendar_feb)
df14 = pd.read_csv(reviews_feb)
df15 = pd.read_csv(reviews0_feb)

df2 = pd.read_csv(listings_march)
df22 = pd.read_csv(listings0_march)
df23 = pd.read_csv(calendar_march)
df24 = pd.read_csv(reviews_march)
df25 = pd.read_csv(reviews0_march)

df3 = pd.read_csv(listings_apr)
df32 = pd.read_csv(listings0_apr)
df33 = pd.read_csv(calendar_apr)
df34 = pd.read_csv(reviews_apr)
df35 = pd.read_csv(reviews0_apr)

# only this are really needed
# columns = ['id', 'name', 'room_type', 'price', 'number_of_reviews', \
#		'neighbourhood', 'transit', 'description', 'last_review']

columns = ['id','zipcode','transit','bedrooms','beds','review_scores_rating',\
	'number_of_reviews','neighbourhood','name','latitude','longitude',\
	'last_review','instant_bookable','host_since','host_response_rate',\
	'host_identity_verified','host_has_profile_pic','first_review',\
	'description','city','cancellation_policy','bed_type','bathrooms',\
	'accommodates','amenities','room_type','property_type','price',\
	'availability_365','minimum_nights']

# 'neighbourhood', 'last_review' and 'name' are the only columns containing at
# least one null value and there is some other file containing that column too.
# sharable_cos = get_sharable_columns(columns)

######################################## NEIGHBOURHOOD ########################################
df1.update(df12['neighbourhood'])
df2.update(df22['neighbourhood'])
df3.update(df32['neighbourhood'])

#check if the are null neighborhood values
# has_empty_cell(df1) # == False 
# has_empty_cell(df2) # == False
# has_empty_cell(df3) # == False


######################################## LAST_REVIEW ########################################
#convert 'last_review' column. e.g. 2019-04-08' to 08-04-19. 
df3['last_review'] = pd.to_datetime(df3["last_review"]).dt.strftime('%d-%m-%y')
df14['date'] = pd.to_datetime(df14["date"]).dt.strftime('%d-%m-%y')
df24['date'] = pd.to_datetime(df24["date"]).dt.strftime('%d-%m-%y') 
df34['date'] = pd.to_datetime(df34["date"]).dt.strftime('%d-%m-%y')

# drop comments corresponding to the same room and date
df14 = df14[['listing_id', 'date', 'comments']].drop_duplicates(subset=['listing_id', 'date'])
df24 = df24[['listing_id', 'date', 'comments']].drop_duplicates(subset=['listing_id', 'date'])
df34 = df34[['listing_id', 'date', 'comments']].drop_duplicates(subset=['listing_id', 'date'])

df1 = df1.merge(df14, left_on=['id', 'last_review'], right_on=['listing_id', 'date'], how='left')
df2 = df2.merge(df24, left_on=['id', 'last_review'], right_on=['listing_id', 'date'], how='left')
df3 = df3.merge(df34, left_on=['id', 'last_review'], right_on=['listing_id', 'date'], how='left')

# check if there are any comments in reviews and reviews0 corresponding to any
# room that its 'last_review' column is null
# is_last_review_there() # == False

######################################## NAME ########################################
# 'name' column is containted only in the listings and listing0 files. Check if
# those null values can be filled.
# identical_columns(df1, df12) # == True
# identical_columns(df1, df12) # == True
# identical_columns(df1, df12) # == True

######################################## PRICE ########################################
df1.update(df12['price'])
df2.update(df22['price'])
df3.update(df32['price'])


# keep only the needed columns
df1 = df1[columns + ['comments']]
df2 = df2[columns + ['comments']]
df3 = df3[columns + ['comments']]

with open(data_path + "/febrouary/updated_feb.csv", 'w+') as file:
	file.write(df1.to_csv(index=False))
 
with open(data_path + "march/updated_march.csv", 'w+') as file:
	file.write(df2.to_csv(index=False))
 
with open(data_path + "april/updated_april.csv", 'w+') as file:
	file.write(df3.to_csv(index=False))

# merge, sort and drop duplicate rows
merged = pd.concat([df1, df2, df3]).drop_duplicates().sort_values('id')

with open(data_path + "train.csv", 'w+') as file:
	file.write(merged.to_csv(index=False))



# ta ids einai komple. einai ta idia se kathe arxeio gia olous tous mines.

# to room_type einai komple.

# sto price den lupei tipota. Omws sta arxeia listings einai se morfi string
# ($77.00) enw sta listings0 se int (77). volevei diladi to deftero

# sto number_of_reviews ola komple.

# sto neighborhood uparxoun kena mono sta listings (agglika).
# ta listings0 (ellinika) einai ola komple.

# to transit periexei kena omws uparxei mono sta listings opote den mporoume na
# ta sumplirwsoume.

# to description periexei kena omws uparxei mono sta listings opote den mporoume na ta sumplirwsoume.

# to last_review periexei ta akrivws idia kena sta listings kai listings0.
# opote den mporume na ta sumplirwsoume. OMWS ta listings kai listings0 martiou
# gia kapoio logo ta diavazei me allo format. opote prepei na kanoume to parakatw: 
# df22['last_review'] = pd.to_datetime(df22["last_review"]).dt.strftime('%d-%m-%y').
# episis ta fevruarouariou einai se morfi %d-%m-%y enw apriliou se %Y-%m-%d.
# opote tou apriliou theloun convert. Uparxoun diaforetika comments pou antistoixoun
# sto idio dwmatio tin idia imerominia