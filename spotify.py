import base64
import json
from requests import post, get, exceptions

from my_types.response import res


# handles all Spotify related needs - tokens, API calls, etc.


# searches for an artist given a search query
# returns response containing artist object
def search_for_artist(token: str, artist: str) -> res:
    try:
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"q={artist}&type=artist&limit=1"

        query_url = url + "?" + query
        response = get(query_url, headers=headers)
        json_result = json.loads(response.content)["artists"]["items"]

        if len(json_result) == 0:
            return res(False, None, f"**{artist}** could not be found")

        return res(True, json_result[0])
    except exceptions.RequestException as e:
        print(e)
        return res(False, None, "Error... please try again")


# returns artist top songs given and artistID
def get_artist_top_tracks(token: str, artistID: str) -> res:
    try:
        url = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?market=US"
        headers = get_auth_header(token)

        response = get(url, headers=headers)
        json_result = json.loads(response.content)["tracks"]

        return res(True, json_result)

    except exceptions.RequestException as e:
        print(e)
        return res(False, None, e)


# retrieves Spotify authorization token
def get_token(client_id: str, client_secret: str) -> str:
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=form)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


# returns authorization header for API calls
def get_auth_header(token: str):
    return {"Authorization": "Bearer " + token}
