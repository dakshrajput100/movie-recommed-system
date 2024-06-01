import numpy as np
import pandas as pd

# links.csv file ko read kar ke links_df dataframe me store kar rahe hain
links_df = pd.read_csv('data/links.csv')

# movies.csv file ko read kar ke movies_df dataframe me store kar rahe hain
movies_df = pd.read_csv('data/movies.csv')

# ratings.csv file ko read kar ke ratings_df dataframe me store kar rahe hain
ratings_df = pd.read_csv('data/ratings.csv')

# tags.csv file ko read kar ke tags_df dataframe me store kar rahe hain
tags_df = pd.read_csv('data/tags.csv')

# movies_df aur ratings_df ko movieId ke basis par merge kar rahe hain
df = movies_df.merge(ratings_df, on='movieId')

# Target movie ka title define kar rahe hain
M_j = 'John Wick (2014)'

# Recommended movies ki list ko initialize kar rahe hain
recommended_movies = []

# Target movie ka data filter kar rahe hain aur rating ke hisaab se sort kar rahe hain
movie_db = df[df['title'] == M_j].sort_values(by='rating', ascending=False)

# Top 5 users jo is movie ko like karte hain unhe select kar rahe hain
for user in movie_db.iloc[:5]['userId'].values:
    # Selected user ke rated movies ko filter kar rahe hain
    rated_movies = df[df['userId'] == user]
    # Target movie ko exclude karke, top 5 rated movies ko sort kar rahe hain
    rated_movies = rated_movies[rated_movies['title'] != M_j].sort_values(by='rating', ascending=False).iloc[:5]
    # Recommended movies list me in movies ko add kar rahe hain
    recommended_movies.extend(list(rated_movies['title'].values))
    
# Unique recommended movies list banate hain
recommended_movies = np.unique(recommended_movies)

# Target movie ke genres ko split kar ke list banate hain
gmovie_genres = df[df['title'] == M_j].iloc[0]['genres'].split('|')

# Score dictionary ko initialize kar rahe hain
scores = {}

# Recommended movies me se har ek movie ke liye
for movie in recommended_movies:
    # Current movie ka data filter kar rahe hain
    movied = df[df['title'] == movie].iloc[0]
    # Current movie ke genres ko split kar ke list banate hain
    movie_genres = movied['genres'].split('|')
    score = 0
    
    # Target movie ke genres ko current movie ke genres se compare kar rahe hain
    for gmovie_genre in gmovie_genres:
        if gmovie_genre in movie_genres:
            # Agar genre match hota hai to score ko increment kar rahe hain
            score += 1
    
    # Current movie ke score ko scores dictionary me add kar rahe hain
    scores[movie] = score
    
# Scores ke basis par recommended movies ko sort kar rahe hain aur descending order me reverse kar rahe hain
recommended_movies = sorted(scores, key=lambda x: scores[x])[::-1]

# Recommended movies ko print kar rahe hain
for movie in recommended_movies:
    print(movie)
