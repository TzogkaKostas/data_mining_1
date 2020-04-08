import pandas as pd
import sys
from pandas import DataFrame, concat
import numpy

def empty_cell(df, column):
	for cell in df[column]:
		if (pd.isnull(cell)):
			return True
	return False


# for 'id' column
def identical_columns(df1, df2, column):
	if len(list(set(df1[column]) & set(df2[column]))) == len(df1[column]) == len(df2[column]):
		return True
	else:
		return False

listings_feb = "../data/febrouary/listings.csv"
listings0_feb = "../data/febrouary/listings0.csv"
listings_march = "../data/march/listings.csv"
listings0_march = "../data/march/listings0.csv"
listings_apr = "../data/april/listings.csv"
listings0_apr = "../data/april/listings0.csv"

df1 = pd.read_csv(listings_feb)
df12 = pd.read_csv(listings0_feb)
df2 = pd.read_csv(listings_march)
df22 = pd.read_csv(listings0_march)
df3 = pd.read_csv(listings_apr)
df32 = pd.read_csv(listings0_apr)


df1.update(df12['price'])
df2.update(df22['price'])
df3.update(df32['price'])
 
df1.update(df12['neighbourhood'])
df2.update(df22['neighbourhood'])
df3.update(df32['neighbourhood'])

#convert 'last_review' column. e.g. 2019-04-08' to 08-04-19. 
df3['last_review'] = pd.to_datetime(df3["last_review"]).dt.strftime('%d-%m-%y')


needed_columns = ['id', 'name', 'room_type', 'price', 'number_of_reviews', \
		'neighbourhood', 'transit', 'description', 'last_review']

df1 = df1[needed_columns]
df2 = df2[needed_columns]
df3 = df3[needed_columns]


with open("../data/febrouary/updated_feb.csv", 'w+') as file:
	file.write(df1.to_csv(index=False))
 
with open("../data/march/updated_march.csv", 'w+') as file:
	file.write(df2.to_csv(index=False))
 
with open("../data/april/updated_april.csv", 'w+') as file:
	file.write(df3.to_csv(index=False))

# merge, sort and drop duplicate rows
merged = pd.concat([df1, df2, df3]).drop_duplicates().sort_values('id')

with open("../data/train.csv", 'w+') as file:
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
# opote tou apriliou theloun convert