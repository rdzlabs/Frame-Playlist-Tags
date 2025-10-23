def get_playback_uri(tag: str) -> str:
    """
    Returns a Spotify URI based on the tag or keyword.
    You can map albums, playlists, or artists here.
    """
    tag = tag.lower()

    albums = {
        "fuerza": "spotify:album:3zu0hJJew2qXZNlselIQk8", 
    }

    # Priority: Album → Playlist
    if tag in albums:
        return albums[tag]
    else:
        return None
