import streamlit as st
import pickle
import pandas as pd

# Load data and model only once using @st.cache
@st.cache(allow_output_mutation=True)
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

# Function to recommend movies
def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

# Main Streamlit app
def main():
    st.title('Movie Recommender System')

    # Load data
    movies, similarity = load_data()

    # User input
    selected_movie_name = st.selectbox(
        'Type or select a movie from dropdown',
        movies['title'].values)

    if st.button('Show Recommendation'):
        recommendations = recommend(selected_movie_name, movies, similarity)
        for movie in recommendations:
            st.write(movie)

if __name__ == "__main__":
    main()
