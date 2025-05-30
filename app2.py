from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

TMDB_API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
NEWS_API_KEY = "cab19e923c8c413585e2ad9d3fb257be"
RAWG_API_KEY = "your_rawg_api_key"
SPOTIFY_CLIENT_ID = "c2be84ba28fd4b0db8fc32591f003397"
SPOTIFY_CLIENT_SECRET = "003a5b32475b4cc2a53bf80c52a7f38f"

@app.route("/")
def index():
    return render_template("index2.html")


# Trending Movies
@app.route("/get_trending_movies")
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    try:
        data = requests.get(url).json()
        movies = [
            {
                "title": movie["title"],
                "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
            }
            for movie in data.get("results", [])[:10]
        ]
        return jsonify({"movies": movies})
    except Exception as e:
        return jsonify({"error": str(e)})


# Trending Books
@app.route("/get_trending_books")
def get_trending_books():
    url = "https://www.googleapis.com/books/v1/volumes?q=subject:fiction+india&maxResults=10"
    try:
        data = requests.get(url).json()
        books = [
            {
                "title": item["volumeInfo"]["title"],
                "poster": item["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            }
            for item in data.get("items", [])
        ]
        return jsonify({"books": books})
    except Exception as e:
        return jsonify({"error": str(e)})


# 🔥 Spotify Access Token Helper
def get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")


# 🔥 Trending Music (Spotify - Top 50 India)
@app.route("/get_trending_music")
def get_trending_music():
    try:
        access_token = get_spotify_access_token()
        if not access_token:
            return jsonify({"error": "Could not get Spotify access token"})

        playlist_id = "37i9dQZF1DXbVhgADFy3im"  # 🎵 Spotify Playlist: Top 50 - India
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=10"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        if "items" not in data:
            return jsonify({"error": "No tracks found in the playlist"})

        tracks = []
        for item in data["items"]:
            track = item.get("track")
            if not track:
                continue

            title = track.get("name")
            artists = ", ".join(artist["name"] for artist in track.get("artists", []))
            image = track["album"]["images"][0]["url"] if track.get("album", {}).get("images") else None

            tracks.append({
                "title": f"{title} - {artists}",
                "poster": image
            })

        return jsonify({"music": tracks})

    except Exception as e:
        return jsonify({"error": str(e)})


# Trending Apps
@app.route("/get_trending_apps")
def get_trending_apps():
    return jsonify({
        "apps": [
            {"title": "Instagram", "poster": None},
            {"title": "Threads", "poster": None},
            {"title": "ShareChat", "poster": None}
        ]
    })


# Trending Fashion
@app.route("/get_trending_fashion")
def get_trending_fashion():
    return jsonify({
        "fashion": [
            {"title": "Sabyasachi Collection 2025", "poster": None},
            {"title": "Lakmé Fashion Week Highlights", "poster": None}
        ]
    })


# Trending Tech
@app.route("/get_trending_tech")
def get_trending_tech():
    return jsonify({
        "tech": [
            {"title": "Nothing Phone 2a", "poster": None},
            {"title": "Apple Vision Pro", "poster": None}
        ]
    })


# Trending News
@app.route("/get_trending_news")
def get_trending_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        data = requests.get(url).json()
        news = [
            {
                "title": article["title"],
                "poster": article.get("urlToImage")
            }
            for article in data.get("articles", [])[:10]
        ]
        return jsonify({"news": news})
    except Exception as e:
        return jsonify({"error": str(e)})


# Trending Games
@app.route("/get_trending_games")
def get_trending_games():
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&ordering=-rating"
    try:
        data = requests.get(url).json()
        games = [
            {
                "title": game["name"],
                "poster": game.get("background_image")
            }
            for game in data.get("results", [])[:10]
        ]
        return jsonify({"games": games})
    except Exception as e:
        return jsonify({"error": str(e)})


# Movie Reviews from RottenTomatoes
@app.route("/get_movie_info/<movie_name>")
def get_movie_info(movie_name):
    formatted_movie_name = movie_name.replace(" ", "_").lower()
    url = f"https://www.rottentomatoes.com/m/{formatted_movie_name}/reviews?type=user"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Movie reviews not found"})

        soup = BeautifulSoup(response.text, 'html.parser')
        review_elements = soup.find_all('span', class_='sc-16c36l0-1 eNlxlZ')  # Adjust if needed
        reviews = [review.get_text() for review in review_elements]

        if not reviews:
            return jsonify({"error": "No reviews found for this movie"})
        
        return jsonify({"reviews": reviews})
    
    except Exception as e:
        return jsonify({"error": str(e)})


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
