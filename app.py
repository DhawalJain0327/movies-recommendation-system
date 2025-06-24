import streamlit as st
import pickle
import pandas as pd
import requests


OMDB_API_KEY = 'd7f38479'  # <- Your OMDb API key

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True':
        return data['Poster']
    else:
        return "https://via.placeholder.com/200x300?text=No+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    for i in similar_movies:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movies_poster.append(fetch_poster(title))
    return recommended_movies, recommended_movies_poster

# Load pickled data

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # First row (5 movies)
    cols1 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])  # 5 content cols, 4 spacer cols
    for i in range(5):
        with cols1[i * 2]:  # indexes: 0, 2, 4, 6, 8
            #st.image(posters[i], use_container_width=True)
            st.markdown(f"""
            <div style='text-align:center;'>
                <img src="{posters[i]}" 
                     style="width:200px; height:300px; object-fit:contain; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.2);" />
                <div style='margin-top:8px; font-weight:bold;'>{names[i]}</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # Second row (next 5 movies)
    cols2 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
    for i in range(5, 10):
        with cols2[(i - 5) * 2]:
            #st.image(posters[i], use_container_width=True)
            st.markdown(f"""
            <div style='text-align:center;'>
                <img src="{posters[i]}" 
                     style="width:200px; height:300px; object-fit:contain; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.2);" />
                <div style='margin-top:8px; font-weight:bold;'>{names[i]}</div>""", unsafe_allow_html=True)


