import subprocess
import os
import time
import webbrowser
import requests

SPOTIFY_URL = "http://127.0.0.1:5051"
NFC_URL = "http://127.0.0.1:5050"
CACHE_FILE = ".cache"

def start_server(script_name, label):
    print(f"🚀 Starting {label}...")
    return subprocess.Popen(["python3", script_name])

def is_spotify_authorized():
    """Check if Spotify server has a valid cache or is authorized."""
    if not os.path.exists(CACHE_FILE):
        return False
    try:
        r = requests.get(f"{SPOTIFY_URL}/play?tag=check")
        return r.status_code != 401  # authorized if not unauthorized
    except:
        return False

if __name__ == "__main__":
    # Step 1 — Start Spotify server
    spotify_process = start_server("spotify_server.py", "Spotify Server")
    time.sleep(3)

    # Step 2 — Check if authorized
    if not is_spotify_authorized():
        print("Spotify not authorized yet.")
        print("Opening browser for authorization...")
        webbrowser.open(f"{SPOTIFY_URL}/auth")

        # Wait for user to finish auth
        print("\nPlease complete authorization in the browser...")
        print("Waiting for Spotify callback...")
        while not os.path.exists(CACHE_FILE):
            time.sleep(2)

        print("✅ Spotify authorized successfully!\n")
    else:
        print("✅ Spotify already authorized.\n")

    # Step 3 — Start NFC server
    nfc_process = start_server("nfc_server.py", "NFC Server")
    print("\n✅ Both servers running!")
    print(f"   - Spotify: {SPOTIFY_URL}")
    print(f"   - NFC:     {NFC_URL}\n")
    print("Tap your NFC tag to start playback!\n")
    print("Press CTRL+C to stop everything.\n")

    try:
        spotify_process.wait()
        nfc_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        spotify_process.terminate()
        nfc_process.terminate()
# http://127.0.0.1:5051/auth
#http://127.0.0.1:5050/test?tag=fuerza