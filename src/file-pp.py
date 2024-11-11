import pandas as pd

# File locations of the dataset - Change them for your machine to get the program to run
br_file = '../Data/Books_rating.csv'
bd_file = '../Data/books_data.csv'

# Loading datasets into dataframes
br_df = pd.read_csv(br_file)
bd_df = pd.read_csv(bd_file)

# Merging the data sets
books = pd.merge(br_df, bd_df, on = 'Title')
print("Datasets merged!")
# Pre-Processing steps to remove duplicate values and empty values
# Only using relevant columns
df = books[ ['Title', 'review/score', 'review/text', 'authors', 'categories', 'ratingsCount']]
df.drop_duplicates(inplace=True)
print("Duplicate values dropped!")
df.dropna(inplace=True)
print("Null values dropped")
# Removing brackets and colons from authors name
df['authors'] = df['authors'].str.extract(r'\'(.*)\'')
print("Brackets and colons removed from authors")
# Removing brackets and colons from categories
df['categories'] = df['categories'].str.extract(r'\'(.*)\'')
print("Brackets and colons removed from categories")
