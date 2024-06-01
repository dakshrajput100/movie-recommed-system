import numpy as np
import pandas as pd

links_df = pd.read_csv('data/links.csv')
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')
tags_df = pd.read_csv('data/tags.csv')

df = movies_df.merge(ratings_df, on='movieId')

M_j = 'John Wick (2014)'
recommended_movies = []

movie_db = df[df['title'] == M_j].sort_values(by='rating', ascending=False)

for user in movie_db.iloc[:5]['userId'].values:
    rated_movies = df[df['userId'] == user]
    rated_movies = rated_movies[rated_movies['title'] != M_j].sort_values(by='rating', ascending=False).iloc[:5]
    recommended_movies.extend(list(rated_movies['title'].values))
    
recommended_movies = np.unique(recommended_movies)

gmovie_genres = df[df['title'] == M_j].iloc[0]['genres'].split('|')
scores = {}

for movie in recommended_movies:
    movied = df[df['title'] == movie].iloc[0]
    movie_genres = movied['genres'].split('|')
    score = 0
    
    for gmovie_genre in gmovie_genres:
        if gmovie_genre in movie_genres:
            score += 1
    
    scores[movie] = score
    
recommended_movies = sorted(scores, key=lambda x: scores[x])[::-1]

for movie in recommended_movies:
    print(movie)
