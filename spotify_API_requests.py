# Emmanuel Zapata BackEnd Development Project

# Goal: Use Python for back-end Connection to Work with the Spotify API
import json
import os
import base64
from dotenv import load_dotenv
from requests import post, get
import sys
import webbrowser
from database import ArtistData, ArtistQuery, get_database_session, ArtistCoverPhotoLinks

# This is used for user input via the command line

# This is for getting any information about your favorite artist.  :)
load_dotenv()
client_id = os.getenv("CLIENT_ID")  # Client ID is in a .env file
client_secret = os.getenv("CLIENT_SECRET")  # Client Secret is in a .env file

db_session = get_database_session()  # Initializing Database session here


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
        result = post(url, headers=headers, data=data)
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
    def search_ForArtistCoverPhoto(token, artistName):
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
        return json_result

    @staticmethod
    def get_AlbumsByArtist(token, artistID):
        url = f"https://api.spotify.com/v1/artists/{artistID}/albums"
        headers = SpotifyAPIScenarios.get_AuthHeader(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result

    @staticmethod
    def get30secondSampleTrack(json_result):
        preview_urls = []
        for track in json_result:
            # Check if the preview URL exists for the track
            if track['preview_url'] is not None:
                # Add the preview URL to the list
                preview_urls.append(track['preview_url'])
        return preview_urls

    @staticmethod
    def format_song_list(song_list):
        formatted_songs = []  # This is a Helper Method for the return of the top tracks!!
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

    @staticmethod
    def format_album_list(album_list):
        formatted_albums = []  # This will hold the formatted album information

        for album in album_list:
            # Extracting relevant album information
            album_info = {
                "Album Name": album['name'],
                "Artists": ", ".join([artist['name'] for artist in album['artists']]),
                "Release Date": album['release_date'],
                "Total Tracks": album['total_tracks'],
                "Spotify URL": album['external_urls']['spotify'],
                "Available Markets": album['available_markets']
            }
            formatted_albums.append(album_info)

        # Printing the formatted album information
        for i, album in enumerate(formatted_albums, 1):
            print(f"{i}. Album Name: {album['Album Name']}")
            print(f"   Artists: {album['Artists']}")
            print(f"   Release Date: {album['Release Date']}")
            print(f"   Total Tracks: {album['Total Tracks']}")
            print(f"   Spotify URL: {album['Spotify URL']}\n")
            print(f"   Available in Markets: {', '.join(album['Available Markets'])}")

    @staticmethod
    def format_30secondPreview(previews):
        for prev in previews:
            return "30 second preview is: " + prev

    @staticmethod
    def save_artist_query(current_db_session, artist_name, query_type):

        query_record = ArtistQuery(artist_name=artist_name, query_type=query_type)
        current_db_session.add(query_record)
        current_db_session.commit()  # Adds to the database here

        print(f"Saved query: {artist_name} - {query_type}")

    @staticmethod
    def save_artist_data(current_db_session, artist_id, artist_name, genres):

        artist_record = ArtistData(
            artist_id=artist_id,
            artist_name=artist_name,
            genres=", ".join(genres) if genres else None
        )

        current_db_session.add(artist_record)
        current_db_session.commit()
        print(f"Saved artist data: {artist_name} (ID: {artist_id})")

    @staticmethod
    def save_artist_cover_photo_link(current_db_session, artist_name, cover_photo_link):

        cover_photo_record = ArtistCoverPhotoLinks(
            artist_name=artist_name,
            cover_photo_link=cover_photo_link
        )

        current_db_session.add(cover_photo_record)
        current_db_session.commit()
        print(f"Saved cover photo link: {artist_name} - {cover_photo_link}")


class Main:
    token = SpotifyAPIScenarios.getAccessToken()
    known_commands = {"top_tracks", "cover_photo", "artist_info", "30-second_sample", "albums", "wikipedia", "profile",
                      "popularity", "genres"}

    if len(sys.argv) > 1 and sys.argv[-1] not in known_commands:  # Non-Specific;Keeps track of Artist Names with Spaces
        artist_userinput = ' '.join(sys.argv[1:])
        search_Result = SpotifyAPIScenarios.search_ForArtist(token, artist_userinput)
        artist_ID = SpotifyAPIScenarios.get_ArtistID(token, artist_userinput)
        SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_ID)
        cover_Photo = SpotifyAPIScenarios.search_ForArtistCoverPhoto(token, artist_userinput)
        print(cover_Photo)

    if len(sys.argv) > 2 and sys.argv[-1] in known_commands:  # User specifies what they want from the command line
        artist_userinput = ' '.join(sys.argv[1:-1])
        command = sys.argv[-1]
        artist_ID = SpotifyAPIScenarios.get_ArtistID(token, artist_userinput)

        SpotifyAPIScenarios.save_artist_query(db_session, artist_userinput, command)

        if command == "top_tracks":
            result = SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_ID)
            SpotifyAPIScenarios.format_song_list(result)
            # DatabaseManager.DatabaseManager.createSQLTableTopTracksQuery(db_connection)
            # Process and print top_tracks here
            print(SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_userinput))

        elif command == "cover_photo":
            cover_photo = SpotifyAPIScenarios.search_ForArtistCoverPhoto(token, artist_userinput)
            SpotifyAPIScenarios.save_artist_cover_photo_link(db_session,artist_userinput, cover_photo)
            print(cover_photo)


        elif command == "artist_info":
            artist_info = SpotifyAPIScenarios.search_ForArtist(token, artist_userinput)
            genres = artist_info["genres"]

            SpotifyAPIScenarios.save_artist_data(db_session, artist_info["id"], artist_userinput, genres)
            print(artist_info)

            # Process and print artist_info here


        elif command == "30-second_sample":
            # Uses the top tracks and only extracts a certain portion of the json_result
            top_tracks = SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_ID)
            samples = SpotifyAPIScenarios.get30secondSampleTrack(top_tracks)
            print(SpotifyAPIScenarios.format_30secondPreview(samples))



        elif command == "albums":
            albums = SpotifyAPIScenarios.get_AlbumsByArtist(token, artist_ID)
            SpotifyAPIScenarios.format_album_list(albums)


        elif command == "wikipedia":
            wikipedia_url = f"https://en.wikipedia.org/wiki/{artist_userinput.replace(' ', '_')}"
            webbrowser.open(wikipedia_url)


        elif command == "profile":
            spotify_link = f"https://open.spotify.com/artist/{artist_ID}"
            webbrowser.open(spotify_link)



        elif command == "genres":
            info = SpotifyAPIScenarios.search_ForArtist(token, artist_userinput)
            genres = info["genres"]
            print("The associated genres for " + artist_userinput + " are : \n")
            for index, genre in enumerate(genres, start=1):


                print(f"{index}. {genre}")
        else:
            print("Unknown command")

    if len(sys.argv) == 1:
        print("No arguments provided. Try Again please !")

    # Check the following tmm:
    # Find Data-Vis Techniques

    # commit to the GitHub Repo
