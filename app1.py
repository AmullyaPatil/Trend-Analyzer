from flask import Flask, render_template
import requests

app = Flask(__name__)

TMDB_API_KEY = "4bf2a03e075776d08f4cd2f418a23e35"
YOUTUBE_API_KEY = "AIzaSyAmXQWASL_pa3CdjZjgkR8tNKKU4k6AkFE"

# 🔹 Get top N trending movies
def get_trending_movies(limit=5):
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url, timeout=10).json()
        return [movie["title"] for movie in response.get("results", [])[:limit]]
    except Exception as e:
        print("Error fetching trending movies:", e)
        return []

# 🔹 Get YouTube review video
def get_youtube_video(movie_title):
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie_title}+review"
        f"&type=video&key={YOUTUBE_API_KEY}&maxResults=1"
    )
    try:
        response = requests.get(search_url, timeout=10).json()
        items = response.get("items", [])
        return items[0]["id"]["videoId"] if items else None
    except Exception as e:
        print(f"Error getting YouTube video for {movie_title}:", e)
        return None

# 🔹 Get comments for a video
def get_youtube_comments(video_id, limit=30):
    comments = []
    url = (
        f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet"
        f"&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults=100"
    )
    try:
        response = requests.get(url, timeout=10).json()
        for item in response.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)
            if len(comments) >= limit:
                break
    except Exception as e:
        print(f"Error getting comments for video {video_id}:", e)
    return comments

# 🔸 Route
@app.route("/")
def index():
    movies = get_trending_movies()
    movie_data = []

    for title in movies:
        video_id = get_youtube_video(title)
        if video_id:
            comments = get_youtube_comments(video_id, limit=30)
            movie_data.append({
                "title": title,
                "video_id": video_id,
                "comments": comments
            })

    return render_template("index1.html", movies=movie_data)

if __name__ == "__main__":
    app.run(debug=True)