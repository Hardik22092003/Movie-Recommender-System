import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names

movies_dict =pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'Type or select a movie from dropdown',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
