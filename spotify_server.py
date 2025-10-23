from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from playback_logic import get_playback_uri
import time



# --- Load environment variables ---
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-modify-playback-state,user-read-playback-state"

app = Flask(__name__)

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=os.path.join(os.path.dirname(__file__), ".cache"),
    open_browser=True
)

@app.route("/auth")
def auth():
    """Step 1: authorize Spotify once."""
    url = sp_oauth.get_authorize_url()
    return f"<a href='{url}'>Click to authorize Spotify</a>"

@app.route("/callback")
def callback():
    """Step 2: Spotify redirect after login."""
    code = request.args.get("code")
    sp_oauth.get_access_token(code)
    return "✅ Spotify authorized. You can close this tab."

@app.route("/play")
def play():
    tag = request.args.get("tag", "default")
    playback_uri = get_playback_uri(tag)

    if not playback_uri:
        return f"❌ No match found for tag '{tag}'.", 400

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return "❌ Not authorized yet — visit /auth first.", 401

    sp = spotipy.Spotify(auth=token_info["access_token"])
    devices = sp.devices().get("devices", [])

    if not devices:
        return "⚠️ No active Spotify device found. Open Spotify, play a song once, then try again.", 400

    # pick an active device if available
    active_device = next((d for d in devices if d.get("is_active")), devices[0])
    device_id = active_device["id"]

    # transfer playback to ensure Spotify targets this device
    sp.transfer_playback(device_id=device_id, force_play=True)

    # enable shuffle safely
    try:
        sp.shuffle(True, device_id=device_id)
        print("🎲 Shuffle enabled")
    except Exception as e:
        print("Shuffle could not be enabled:", e)

    time.sleep(0.5)

    # start playback
    try:
        sp.start_playback(device_id=device_id, context_uri=playback_uri)
        print(f"🎶 Playing {tag} ({playback_uri}) on {active_device['name']}")
        return f"🎶 Now playing {tag} (shuffle on)"
    except Exception as e:
        print("❌ Playback error:", e)
        return f"Playback failed: {e}", 500


if __name__ == "__main__":
    print(get_playback_uri("fuerza"))
    app.run(host="0.0.0.0", port=5051)
