from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# TMDB API Key
API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
BASE_URL = "https://api.themoviedb.org/3"

# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route to fetch live trending movies
@app.route("/get_trending_movies", methods=["GET"])
def get_trending_movies():
    endpoint = f"{BASE_URL}/trending/movie/day"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        movies = []
        for movie in data.get("results", [])[:10]:  # Fetch top 10 trending movies
            movies.append({
                "title": movie.get("title", "Unknown Title"),
                "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None
            })
        return jsonify({"movies": movies})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
