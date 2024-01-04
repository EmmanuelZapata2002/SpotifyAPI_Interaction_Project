import json
import os
import base64
from dotenv import load_dotenv
from requests import post,get
import sys
# This is used for user input via the command line


# This is for getting any information about your favorite artist.  :)
load_dotenv()
client_id = os.getenv("CLIENT_ID") # Client ID is in a .env file
client_secret = os.getenv("CLIENT_SECRET") #Client Secret is in a .env file

class SpotifyAPIScenarios:
    @staticmethod
    def getAccessToken():
        auth_String = client_id + ":" + client_secret
        auth_Bytes = auth_String.encode("utf-8")
        auth_Base64 = str(base64.b64encode(auth_Bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
        "Authorization": "Basic " + auth_Base64,
        "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url,headers=headers,data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    @staticmethod
    def get_AuthHeader(token):
        return {"Authorization": "Bearer " + token}

    @staticmethod
    def search_ForArtist(token, artistName):
        url = "https://api.spotify.com/v1/search"
        headers = SpotifyAPIScenarios.get_AuthHeader(token)
        query = f"?q={artistName}&type=artist&limit=1"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            print("No artist with this name exists")
            return None
        artist = json_result[0]
        return artist

    @staticmethod
    def search_ForArtistCoverPhoto(token,artistName):
        url = "https://api.spotify.com/v1/search"
        headers = SpotifyAPIScenarios.get_AuthHeader(token)
        query = f"?q={artistName}&type=artist&limit=1"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            print("No artist with this name exists")
            return None
        photo_link = json_result[0]['images'][0]['url']
        return photo_link

    @staticmethod
    def get_ArtistID(token, artistName):
        search_Result = SpotifyAPIScenarios.search_ForArtist(token, artistName)
        artist_ID = search_Result["id"]
        return artist_ID

    @staticmethod
    def get_TopTracksByArtist(token, artistID):
        url = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?country=US"
        headers = SpotifyAPIScenarios.get_AuthHeader(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return SpotifyAPIScenarios.format_song_list(json_result)


    @staticmethod
    def get30secondSampleTrack(result):
        for track in result["tracks"][:10]:
            print('track    : ' + track['name'])
            print('audio    : ' + track['preview_url'])
            print('cover art: ' + track['album']['images'][0]['url'])
            print()

    @staticmethod
    def format_song_list(song_list):
        formatted_songs = [] # This is a Helper Method
        for song in song_list:
            song_info = {
                "Song Name": song['name'],
                "Artists": ", ".join([artist['name'] for artist in song['artists']]),
                "Album": song['album']['name'],
                "Release Date": song['album']['release_date'],
                "Preview URL": song['preview_url']
            }
            formatted_songs.append(song_info)
        for i in range(len(formatted_songs)):
            print(f"{i + 1}. Song Name: {formatted_songs[i]['Song Name']}")
            print(f"   Artists: {formatted_songs[i]['Artists']}")
            print(f"   Album: {formatted_songs[i]['Album']}")
            print(f"   Release Date: {formatted_songs[i]['Release Date']}")
            print(f"   Preview URL: {formatted_songs[i]['Preview URL']}\n")

class Main:

    token = SpotifyAPIScenarios.getAccessToken()
    if len(sys.argv) == 2: # Non-Specific Information about the artist
        artist_userinput = sys.argv[1]
        search_Result = SpotifyAPIScenarios.search_ForArtist(token, artist_userinput)
        artist_ID = SpotifyAPIScenarios.get_ArtistID(token, artist_userinput)
        SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_ID)
        cover_Photo = SpotifyAPIScenarios.search_ForArtistCoverPhoto(token, artist_userinput)
        print(cover_Photo)
    else:
        print("No arguments provided")

    if len(sys.argv) > 2: # User specifies what they want from the command line
        artist_userinput = ' '.join(sys.argv[1:-1])
        command = sys.argv[-1]
        artist_ID = SpotifyAPIScenarios.get_ArtistID(token, artist_userinput)
        if command == "top_tracks":
            SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_ID)
            # Process and print top_tracks here
        elif command == "cover_photo":
            cover_photo = SpotifyAPIScenarios.search_ForArtistCoverPhoto(token, artist_userinput)
            print(cover_photo)
        elif command == "artist_info":
            artist_info = SpotifyAPIScenarios.search_ForArtist(token, artist_userinput)
            # Process and print artist_info here
            # You can add more elif blocks for other commands
        else:
             print("Unknown command")




