from flask import Flask, render_template, jsonify, request
import requests
import base64
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

TMDB_API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
NEWS_API_KEY = "cab19e923c8c413585e2ad9d3fb257be"
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


# Spotify Access Token Helper
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


# Trending Music (Spotify - Top 50 Global)
@app.route("/get_trending_music")
def get_trending_music():
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(GLOBAL_TOP_URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    songs = []
    for item in data.get("albums", {}).get("items", [])[:10]:
        songs.append({
            "name": item.get("name"),
            "image": item.get("images", [{}])[0].get("url"),
            "url": item.get("external_urls", {}).get("spotify")
        })
    return jsonify(songs)


# Trending Fashion (Scraped from Vogue)
@app.route("/get_trending_fashion")
def get_trending_fashion():
    try:
        url = "https://www.vogue.com/fashion"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        fashion_items = []
        
        # Extract trending fashion items from Vogue
        articles = soup.select('div.summary-item__content')[:10]
        for article in articles:
            title = article.select_one('h3.summary-item__hed')
            image = article.select_one('img')
            
            if title and image:
                fashion_items.append({
                    "title": title.text.strip(),
                    "poster": image.get('src') or image.get('data-src')
                })
        
        return jsonify({"fashion": fashion_items[:10]})
    except Exception as e:
        return jsonify({"error": str(e)})


# Trending Apps (Top Free Apps from Play Store)
@app.route("/get_trending_apps")
def get_trending_apps():
    try:
        url = "https://play.google.com/store/apps/top?hl=en_US"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        apps = []
        
        # Extract top free apps
        app_cards = soup.select('div.ZmHEEd')[:10]
        for card in app_cards:
            title = card.select_one('div.WsMG1c')
            image = card.select_one('img.T75of')
            
            if title and image:
                apps.append({
                    "title": title.text.strip(),
                    "poster": image.get('src') or image.get('data-src')
                })
        
        return jsonify({"apps": apps[:10]})
    except Exception as e:
        return jsonify({"error": str(e)})


# Trending Games (Top Free Games from Play Store)
@app.route("/get_trending_games")
def get_trending_games():
    try:
        url = "https://play.google.com/store/apps/category/GAME/collection/topselling_free?hl=en_US"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        games = []
        
        # Extract top free games
        game_cards = soup.select('div.ZmHEEd')[:10]
        for card in game_cards:
            title = card.select_one('div.WsMG1c')
            image = card.select_one('img.T75of')
            
            if title and image:
                games.append({
                    "title": title.text.strip(),
                    "poster": image.get('src') or image.get('data-src')
                })
        
        return jsonify({"games": games[:10]})
    except Exception as e:
        return jsonify({"error": str(e)})


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
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        data = requests.get(url).json()
        news = [{
            "title": article["title"],
            "poster": article.get("urlToImage", None)
        } for article in data.get("articles", [])[:10]]
        return jsonify({"news": news})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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