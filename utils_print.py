from datetime import datetime


def auth_page():
    """Static styled HTML page for Spotify authorization."""
    return """
    <html>
        <head>
            <title>Spotify Authorization</title>
            <style>
                body {
                    font-family: system-ui, sans-serif;
                    text-align: center;
                    background-color: #121212;
                    color: #fff;
                    margin-top: 10%;
                }
                a {
                    color: #1DB954;
                    font-size: 1.5em;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                h1 {
                    color: #1DB954;
                }
            </style>
        </head>
        <body>
            <h1>Spotify Authorization</h1>
            <p><a href='{{auth_url}}'>Click here to authorize Spotify</a></p>
        </body>
    </html>
    """

