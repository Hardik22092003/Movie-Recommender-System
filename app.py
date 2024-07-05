import streamlit as st
import pickle
import pandas as pd

# Load data using st.cache_resource
@st.cache_resource
def load_data():
    # Load only necessary columns to minimize memory usage
    try:
        with open('movie_dict.pkl', 'rb') as f:
            movies_dict = pickle.load(f)
        movies = pd.DataFrame(movies_dict, columns=['movie_id', 'title'])

        with open('similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)

        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Function to recommend movies
def recommend(movie, movies, similarity):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return []

    # Get top 5 most similar movies
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = [movies.iloc[i[0]].title for i in distances]

    return recommended_movie_names

# Main Streamlit app
def main():
    st.title('Movie Recommender System')

    # Load data
    movies, similarity = load_data()

    if movies is not None and similarity is not None:
        # User input
        selected_movie_name = st.selectbox(
            'Type or select a movie from dropdown',
            movies['title'].values)

        if st.button('Show Recommendation'):
            recommendations = recommend(selected_movie_name, movies, similarity)
            if recommendations:
                st.write("Recommendations:")
                for movie in recommendations:
                    st.write(movie)
            else:
                st.write("No recommendations found.")
    else:
        st.write("Failed to load data. Please try again later.")

if __name__ == "__main__":
    main()
