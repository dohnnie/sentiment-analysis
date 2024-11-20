import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# File locations of the dataset - Change them for your machine to get the program to run
br_file = '../Data/Books_rating.csv'
bd_file = '../Data/books_data.csv'

# Loading datasets into dataframes
print('Loading datasets!')
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

df['word_count'] = df['review/text'].apply(lambda x: len(x.split(' ')))

print('Making pie chart!')
# Pie Chart for distrubtion of books based on genre
plt.figure(figsize=(7,7))
labels = ['Fiction', 'Juvenile Fiction', 'Biography & Autobiography', 'Religion', 'History', 'Business & Economics', 'Computers', 'Cooking', 'Social Science', 'Family & Relationships']
plt.pie(df['categories'].value_counts().head(10), labels=labels, autopct='%1.1f%%') 
plt.title('Distribution of Books Based on Genre', fontsize=20)
plt.axis('off')
plt.legend()
plt.show()

print('Making word cloud!')
# Word cloud
wc = WordCloud(width=500, height=500, min_font_size=15, background_color='white')
spam_wc = wc.generate(df[df['review/score'] > 3]['review/text'].str.cat(sep=" "))
plt.figure(figsize=(7, 7))
plt.axis('off')
plt.imshow(spam_wc)
print('Word cloud made!')

print('Making bar chart!')
# Most reviewed books
plt.figure(figsize=(7,7))
count = df[df['word_count'] > 1707][['Title', 'word_count']].sort_values(by='word_count', ascending=False)
colors = sns.color_palette('husl', n_colors=len(count))
bars = plt.bar(count['Title'], count['word_count'], color=colors)
plt.title('Most Reviewed Books by Word Count', fontsize=20)
plt.xticks(rotation=90)
plt.show()

print('Making bar chart!')
# Highest Rated Books with over 4000 ratings each book
plt.figure(figsize=(7, 7))
rating_counts = df[df['ratingsCount'] > 4000][['Title', 'ratingsCount']].drop_duplicates()
plt.bar(rating_counts['Title'], rating_counts['ratingsCount'])
plt.title('Highest Rated Books with over 4000 ratings each Books', fontsize= 15)
plt.xticks(rotation=90)
plt.show()

print('Bar chart created!')
# Average Ratings on Vook genres
# Convert 'review/score' column to numeric (if applicable)
print('Converting scores!')
df['review/score'] = pd.to_numeric(df['review/score'], errors='coerce')

# Filter out non-numeric values (if any)
print('Filtering non-numeric values')
numeric_data = df.dropna(subset=['review/score'])


# Group by 'categories' and compute the mean of 'review/score'
print('Grouping and computing mean')
avg_cat_rating = numeric_data.groupby('categories')['review/score'].mean().sort_values(ascending=False).head(10)
avg_cat_rating_d = numeric_data.groupby('categories')['review/score'].mean().sort_values().head(10)

print('Making bar chart!')
# Plot the bar chart for top and bottom categories
plt.figure(figsize=(10,10))
plt.bar(avg_cat_rating.index, avg_cat_rating, color='blue', label='Top 10')
plt.bar(avg_cat_rating_d.index, avg_cat_rating_d, color='red', label='Bottom 10')
plt.title('Average Ratings on Book Genres', fontsize=15)
plt.xticks(rotation='vertical')
plt.ylabel('Ratings')
plt.legend()
plt.show()
print('Bar chart created!')

# Top 10 Authors with highest average ratings
# Convert 'review/score' column to numeric, coercing erros to NaN
print('Converting!')
df['review/score'] = pd.to_numeric(df['review/score'], errors='coerce')

# Group by 'authors', compute the mean of 'review/score', and plot the top 10 authors
print('Grouping!')
top_authors = df.groupby('authors')['review/score'].mean().nlargest(10)

print('Making bar chart!')
top_authors.plot(kind='barh', figsize=(7,7))
plt.title('Top 10 Authors with Highest Average Ratings')
plt.xlabel('Average Ratings')
plt.ylabel('Authors')
print('Bar chart created!')
plt.show()

# Top 10 Authors with 1 star ratings
# Grouping the data by authors and calculating the mean review score for each author
print('Grouping!')
average_scores_by_author = df.groupby('authors')['review/score'].mean()

# Sorting the authors based on their average review scores and selecting the bottom 10 (lowest scores)
print('Sorting!')
bottom_10_authors = average_scores_by_author.sort_values(ascending=True).head(10)

# Creating a horizontal bar plot to show the top 10 authors with the lowest average review scores
print('Making bar chart!')
bottom_10_authors.plot(kind='barh', figsize=(7, 7))
print('Bar chart created!')

# Setting the title for the plot
plt.title('Top 10 Authors with 1-star Ratings', fontsize=15)

# Displaying the plot
plt.show()

print('Making bar chart!')
# Number of Books written by each Author
df['authors'].value_counts().head(20).sort_values(ascending=True).plot(kind='barh', figsize=(7,7))
plt.title('Number of Books written by the Authors', fontsize=15)
plt.ylabel('Name of Author')
plt.xlabel('Number of Books Written')
print('Bar chart created!')
plt.show()
