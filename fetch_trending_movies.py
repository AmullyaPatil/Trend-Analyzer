import requests

# TMDB API Key
API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"

# Base URL for TMDB API
BASE_URL = "https://api.themoviedb.org/3"

# Function to fetch trending movies
def get_trending_movies():
    endpoint = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Extract and display movie details
        print("Trending Movies (Top 10):")
        for movie in data.get("results", [])[:10]:  # Top 10 movies
            title = movie.get("title", "Unknown Title")
            release_date = movie.get("release_date", "Unknown Release Date")
            rating = movie.get("vote_average", "N/A")
            print(f"- {title} (Release: {release_date}, Rating: {rating})")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# Function to fetch movie posters
def get_movie_posters():
    endpoint = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        print("\nTrending Movie Posters:")
        for movie in data.get("results", [])[:10]:
            title = movie.get("title", "Unknown Title")
            poster_path = movie.get("poster_path", "")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # Adjust size if needed
                print(f"- {title}: {poster_url}")
            else:
                print(f"- {title}: No poster available")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# Main function
if __name__ == "__main__":
    get_trending_movies()
    get_movie_posters()
