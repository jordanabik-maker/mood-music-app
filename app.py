from flask import Flask, render_template, request
import requests
import base64
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode()
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# 🎵 Mood → Playlist IDs
mood_playlists = {
    "happy": "37i9dQZF1DX3rxVfibe1L0",   # Mood Booster
    "sad": "37i9dQZF1DX7qK8ma5wgG1",     # Sad Songs (this one is fine)
    "focus": "37i9dQZF1DX4sWSpwq3LiO"    # Focus (this one is fine)
}

mood_queries = {
    "happy": "happy upbeat",
    "sad": "sad emotional",
    "focus": "study instrumental",
    "hype": "hype rap energetic",
    "chill": "lofi chill relax"
}

@app.route("/", methods=["GET", "POST"])
def home():
    songs = []

    if request.method == "POST":
        mood = request.form.get("mood")

        token = get_token()
        playlist_id = mood_playlists.get(mood)

        offset = random.randint(0, 50)

        query = mood_queries.get(mood, mood)

        response = requests.get(
            f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10&offset={offset}",
            headers={"Authorization": f"Bearer {token}"}
        )

        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        if "tracks" in data:
            songs = data["tracks"]["items"]
        else:
            songs = []

    return render_template("index.html", songs=songs)

@app.route("/songs/<mood>")
def get_songs(mood):
    token = get_token()

    import random
    offset = random.randint(0, 50)

    response = requests.get(
        f"https://api.spotify.com/v1/search?q={mood}&type=track&limit=10&offset={offset}",
        headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()

    if "tracks" in data:
        return {"songs": data["tracks"]["items"]}
    else:
        return {"songs": []}

if __name__ == "__main__":
    app.run(debug=True)