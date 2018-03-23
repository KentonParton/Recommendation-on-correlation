import numpy as np
import pandas as pd

frame =  pd.read_csv('rating_final.csv')
cuisine = pd.read_csv('cuisine.csv')
geodata = pd.read_csv('places.csv', encoding = "ISO-8859-1") #for windows || geodata = pd.read_csv('geoplaces2.csv', encoding = "mbcs")

# names of restaurants
places =  geodata[['placeID', 'name']]

# avg of restaurant ratings
rating = pd.DataFrame(frame.groupby('placeID')['rating'].mean())

# counts number of reviews
rating['rating_count'] = pd.DataFrame(frame.groupby('placeID')['rating'].count())

# top rated resaurant
top_rated = rating.sort_values('rating_count', ascending=False).head().iloc[0].name


places_crosstab = pd.pivot_table(data=frame, values='rating', index='userID', columns='placeID')


ratings_of_top_rated = places_crosstab[top_rated]
ratings_of_top_rated[ratings_of_top_rated>=0]

# restaurants which are similar to the top rated restaurant
similar_to_top_rated = places_crosstab.corrwith(ratings_of_top_rated)

# what is the correlation between top_rated and similar_to_top_rated
corr_top_rated = pd.DataFrame(similar_to_top_rated, columns=['PearsonR'])
# remove nulls
corr_top_rated.dropna(inplace=True)

# cleaned data (nulls removed)
top_rated_corr_summary = corr_top_rated.join(rating['rating_count'])

# shows top 10 alternatives to top_rated. Decending order
top_rated_corr_summary = top_rated_corr_summary[top_rated_corr_summary['rating_count']>=10].sort_values('PearsonR', ascending=False).head(10)

# list of placeID
top_rated_corr_list = []

# appends alternatives to placeID list
for i in range(len(top_rated_corr_summary)):
    top_rated_corr_list.append(top_rated_corr_summary.iloc[i].name)


places_corr_top_rated = pd.DataFrame(top_rated_corr_list, index = np.arange(10), columns=['placeID'])

# provides final results of the top alternatives
summary = pd.merge(places_corr_top_rated, cuisine,on='placeID')



print('================================')
print(summary)
print('================================')


'''
Seeing that Tortas(top_rated) is fast food and there is another fast food
restaurant was also recommended within our summary, we know that the program
is working correctly.
 '''

# top rated restaurant
print('Top Rated Restaurant: \n' + str(places[places['placeID'] == 135085]))
print('================================')
# The other fast food restaurant
print('Another Fast Food Restaurant: \n' + str(places[places['placeID'] == 135046]))
print('================================')
print (cuisine['Rcuisine'].describe())
