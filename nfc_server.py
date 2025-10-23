from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/test")
def test():
    tag = request.args.get("tag", "unknown")
    print(f"Tag tapped → {tag}")

    try:
        # Forward tag to Spotify server
        r = requests.get(f"http://127.0.0.1:5051/play?tag={tag}")
        print("Spotify server:", r.text)
    except Exception as e:
        print("Could not reach Spotify server:", e)

    return f"Tag {tag} received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
