
import pickle
import pandas as pd
import io
import streamlit as st
import requests

import subprocess
import sys

import gdown
# URL for the similarity pickle file
url = "https://drive.google.com/uc?id=12SVsmtRTuDsxVKulejno7sXHq6AsYRtG"

# Download the file
output = "similarity.pkl"
gdown.download(url, output, quiet=False)

# Load movie data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to get movie poster from TMDB website using API
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

# Function to recommend 5 similar movies and display posters along with names
def recommend(movie):
    if similarity is None:
        st.error("Similarity data not loaded.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Streamlit app
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
