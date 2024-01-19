import streamlit as st
import pandas as pd
import pickle
import requests

# Load the data and model
movies_list = pd.read_pickle('D:\\Internship\\CodeClause\\Movie Recommender\\movies_list.pkl')
similarity_matrix = pickle.load(open('D:\\Internship\\CodeClause\\Movie Recommender\\similarity.pkl', 'rb'))

# Function to get movie recommendations with poster links from TMDb API
def get_movie_recommendations_with_posters(movie_title):
    # Convert the input to lowercase for case-insensitive comparison
    movie_title_lower = movie_title.lower()

    # Find the index of the movie in the dataset
    idx = movies_list.index[movies_list['title'].str.lower() == movie_title_lower].tolist()

    if not idx:
        raise IndexError  # Movie not found in the dataset

    idx = idx[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Exclude the input movie itself
    recommended_movies = movies_list.iloc[[i[0] for i in sim_scores]][['title']]

    # Add image URLs using TMDb API
    recommended_movies['image_url'] = recommended_movies['title'].apply(get_movie_poster_url)

    return recommended_movies

# Function to fetch movie poster URL from TMDb API
def get_movie_poster_url(movie_title):
    # Replace 'YOUR_API_KEY' with your TMDb API key
    api_key = 'dc633e7e1ee6a4dde3df943db230f731'
    base_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}&language=en'

    response = requests.get(base_url)
    data = response.json()

    if data['results']:
        movie_id = data['results'][0]['id']
        poster_path = data['results'][0]['poster_path']
        return f'https://image.tmdb.org/t/p/original{poster_path}'

    return None

# Streamlit App
st.markdown("<h1 style='text-align: center;'>Movie Recommendation App</h1>", unsafe_allow_html=True)

# New Banner image
st.image("https://static.vecteezy.com/system/resources/previews/000/540/677/large_2x/movie-banner-alphabet-sign-marquee-light-bulb-vintage-vector.jpg", use_column_width=True, caption='C I N E M A    I S    A    P O W E R F U L    W E A P O N')

# Movie input
movie_input = st.text_input('Enter a movie title:')
if movie_input:
    try:
        recommended_movies = get_movie_recommendations_with_posters(movie_input)

        # Display recommended movies and their images in groups of three
        st.write('Recommended Movies:')
        
        # Create columns for displaying movies
        cols = st.columns(3)

        for index, row in recommended_movies.iterrows():
            with cols[index % 3]:
                #st.write(f"**{row['title']}**")
                st.image(row['image_url'], caption=row['title'], use_column_width=True)

    except IndexError:
        st.write('Movie not found in the dataset. Please try another one.')
