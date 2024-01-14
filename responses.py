from statics import HELLO, INVALID, HELP, arg_message
from random import choice
from spotify import (
    get_artist_top_tracks,
    search_for_artist,
    search_for_track,
    get_recommendation,
)


# handles the logic for responses
def handle_response(tokens, spotify_token) -> str:
    command = tokens[0]

    if not command:
        return INVALID
    if command in ["hello", "hi"]:
        return choice(HELLO)
    if command in ["search", "s"]:
        if len(tokens) == 1:
            return arg_message("search")
        return handle_search(tokens[1], spotify_token)
    if command == "rec":
        return handle_recommendation(tokens[1], tokens[2], tokens[3], spotify_token)
    if command == "help":
        return HELP

    return INVALID


# handles search requests and reformats artist data
def handle_search(search_query: str, spotify_token: str) -> str:
    search_res = search_for_artist(spotify_token, search_query)
    if not search_res.success:
        return search_res.message

    # we want name, image, and top 5 songs
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
    for i in range(len(genres_list)):
        if i == len(genres_list) - 1:
            genres += genres_list[i]
        else:
            genres += genres_list[i] + ", "

    formatted_response = (
        f"**{name}**\n\n"
        f"**Genres**: {genres}\n\n"
        "**Top Tracks**:\n" + formatted_tracks
    )

    return formatted_response


# handles requests for track recommendations
def handle_recommendation(genre: str, artist: str, track: str, spotify_token: str):
    # get IDs for artist and track
    artist_res = search_for_artist(spotify_token, artist)
    if not artist_res.success:
        return artist_res.message

    artistID = artist_res.payload["id"]

    track_res = search_for_track(spotify_token, track)
    if not track_res.success:
        return track_res.message

    trackID = track_res.payload["id"]

    # get recommendation
    rec_res = get_recommendation(spotify_token, genre, artistID, trackID)
    if not rec_res.success:
        return rec_res.message

    recommendation = rec_res.payload
    recc_name = recommendation["name"]
    artist_list = [x["name"] for x in recommendation["artists"]]
    recc_artists = ""

    for i in range(len(artist_list)):
        if i == len(artist_list) - 1:
            recc_artists += artist_list[i]
        else:
            recc_artists += artist_list[i] + ", "

    spotify_url = recommendation["external_urls"]["spotify"]

    formatted_response = (
        "SpottyBot Recommends...\n\n"
        f"**{recc_name} - {recc_artists}**\n\n"
        f"Take a listen: {spotify_url}"
    )

    return formatted_response
