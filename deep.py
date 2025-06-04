from flask import Flask, render_template, jsonify
import requests
import base64
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

app = Flask(__name__)

# API Keys
TMDB_API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
NEWS_API_KEY = "cab19e923c8c413585e2ad9d3fb257be"
SPOTIFY_CLIENT_ID = "c2be84ba28fd4b0db8fc32591f003397"
SPOTIFY_CLIENT_SECRET = "003a5b32475b4cc2a53bf80c52a7f38f"
STEAM_API_KEY = "YOUR_STEAM_API_KEY"  # Register at https://steamcommunity.com/dev

# User Agent for scraping
ua = UserAgent()

@app.route("/")
def index():
    return render_template("indexdeep.html")

# Helper Functions
def get_spotify_token():
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token")

def fetch_with_retry(url, headers=None, retries=3):
    headers = headers or {"User-Agent": ua.random}
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            time.sleep(1)
        except Exception:
            time.sleep(1)
            continue
    return None

# API Endpoints
@app.route("/get_trending_movies")
def get_trending_movies():
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
        data = requests.get(url).json()
        movies = [{
            "title": movie["title"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
        } for movie in data.get("results", [])[:10]]
        return jsonify({"movies": movies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_trending_music")
def get_trending_music():
    try:
        token = get_spotify_token()
        if not token:
            return jsonify({"error": "Spotify authentication failed"}), 500
            
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks?limit=10",
            headers=headers
        )
        data = response.json()
        
        tracks = [{
            "title": f"{item['track']['name']} - {', '.join(a['name'] for a in item['track']['artists'])}",
            "poster": item["track"]["album"]["images"][0]["url"] if item["track"]["album"]["images"] else None
        } for item in data.get("items", []) if item.get("track")]
        
        return jsonify({"music": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_trending_apps")
def get_trending_apps():
    try:
        # Scrape Google Play Store Top Free Apps
        url = "https://play.google.com/store/apps/top?hl=en_US"
        response = fetch_with_retry(url)
        if not response:
            return jsonify({"error": "Failed to fetch apps data"}), 500
            
        soup = BeautifulSoup(response.text, 'html.parser')
        apps = []
        
        for item in soup.select('div.VfPpkd-EScbFb-JIbuQc.UVEnyf', limit=10):
            title = item.select_one('div.Epkrse').text if item.select_one('div.Epkrse') else None
            image = item.select_one('img.T75of').get('src') if item.select_one('img.T75of') else None
            
            if title:
                apps.append({
                    "title": title,
                    "poster": image
                })
        
        return jsonify({"apps": apps[:10]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_trending_games")
def get_trending_games():
    try:
        # Scrape Steam Top Sellers
        url = "https://store.steampowered.com/search/?filter=topsellers"
        response = fetch_with_retry(url)
        if not response:
            return jsonify({"error": "Failed to fetch games data"}), 500
            
        soup = BeautifulSoup(response.text, 'html.parser')
        games = []
        
        for item in soup.select('a.search_result_row', limit=10):
            title = item.select_one('span.title').text if item.select_one('span.title') else None
            image = item.select_one('img').get('src') if item.select_one('img') else None
            
            if title:
                games.append({
                    "title": title,
                    "poster": image
                })
        
        return jsonify({"games": games[:10]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_trending_fashion")
def get_trending_fashion():
    try:
        # Scrape Vogue Fashion Trends
        url = "https://www.vogue.com/fashion/trends"
        response = fetch_with_retry(url)
        if not response:
            return jsonify({"error": "Failed to fetch fashion data"}), 500
            
        soup = BeautifulSoup(response.text, 'html.parser')
        fashion = []
        
        for item in soup.select('div.summary-item__content', limit=10):
            title = item.select_one('h3.summary-item__hed').text.strip() if item.select_one('h3.summary-item__hed') else None
            image = item.select_one('img').get('src') if item.select_one('img') else None
            
            if title:
                fashion.append({
                    "title": title,
                    "poster": image
                })
        
        return jsonify({"fashion": fashion[:10]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == "__main__":
    app.run(debug=True)