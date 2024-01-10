from statics import HELLO, INVALID, HELP, arg_message
from random import choice
from spotify import get_artist_top_tracks, search_for_artist


# handles the logic for responses
def handle_response(tokens, spotify_token) -> str:
    command = tokens[0][1:]

    if not command:
        return INVALID
    if command in ["hello", "hi"]:
        return choice(HELLO)
    if command in ["search", "s"]:
        if len(tokens) == 1:
            return arg_message("search")
        return handle_search(tokens[1], spotify_token)
    if command == "help":
        return HELP

    return INVALID


# handles search requests and reformats artist data
def handle_search(search_query: str, spotify_token: str) -> str:
    search_res = search_for_artist(spotify_token, search_query)
    if not search_res.success:
        return search_res.message
    # we want name, image, and top 5 songs??
    artist = search_res.payload
    name = artist["name"]
    genres_list = artist["genres"]
    artist_ID = artist["id"]

    tracks_res = get_artist_top_tracks(spotify_token, artist_ID)
    if not tracks_res.success:
        return tracks_res.message

    tracks = tracks_res.payload
    top_five_tracks = (
        [x["name"] for x in tracks[:5]]
        if len(tracks) > 5
        else [x["name"] for x in tracks]
    )

    formatted_tracks = ""
    for track in top_five_tracks:
        formatted_tracks += f"- {track}\n"

    genres = ""
    for n, genre in enumerate(genres_list):
        if n == len(genres_list) - 1:
            genres += genre
        else:
            genres += genre + ", "

    formatted_response = (
        f"**{name}**\n\n"
        f"**Genres**: {genres}\n\n"
        "**Top Tracks**:\n" + formatted_tracks
    )

    return formatted_response
