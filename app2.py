from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

TMDB_API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
NEWS_API_KEY = "cab19e923c8c413585e2ad9d3fb257be"
RAWG_API_KEY = "your_rawg_api_key"

@app.route("/")
def index():
    return render_template("index2.html")


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


@app.route("/get_trending_music")
def get_trending_music():
    return jsonify({
        "music": [
            {"title": "Animal - Arjan Vailly", "poster": None},
            {"title": "Kesariya - Brahmastra", "poster": None},
            {"title": "Naatu Naatu - RRR", "poster": None}
        ]
    })


@app.route("/get_trending_apps")
def get_trending_apps():
    return jsonify({
        "apps": [
            {"title": "Instagram", "poster": None},
            {"title": "Threads", "poster": None},
            {"title": "ShareChat", "poster": None}
        ]
    })


@app.route("/get_trending_fashion")
def get_trending_fashion():
    return jsonify({
        "fashion": [
            {"title": "Sabyasachi Collection 2025", "poster": None},
            {"title": "Lakmé Fashion Week Highlights", "poster": None}
        ]
    })


@app.route("/get_trending_tech")
def get_trending_tech():
    return jsonify({
        "tech": [
            {"title": "Nothing Phone 2a", "poster": None},
            {"title": "Apple Vision Pro", "poster": None}
        ]
    })


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


if __name__ == "__main__":
    app.run(debug=True)
