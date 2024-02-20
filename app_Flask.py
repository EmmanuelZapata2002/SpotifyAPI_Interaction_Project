from flask import Flask, request, jsonify
from flask_cors import CORS

from Spotify_DataVisualization import SpotifyAPIScenarios # Import your class


from Spotify_DataVisualization import Main




app = Flask(__name__)
CORS(app)

@app.route('/search_artist', methods=['POST'])
def search_artist():
    data = request.json
    artist_name = data['artistName']
    token = SpotifyAPIScenarios.getAccessToken()
    artist = SpotifyAPIScenarios.search_ForArtist(token, artist_name)
    return jsonify(artist)

@app.route('/top_tracks', methods=['GET'])
def top_tracks():
    artist_name = request.args.get('artistName')
    if not artist_name:
        return jsonify({"error": "Missing artistName parameter"}), 400
    token = SpotifyAPIScenarios.getAccessToken()
    artist_id = SpotifyAPIScenarios.get_ArtistID(token, artist_name)
    tracks = SpotifyAPIScenarios.get_TopTracksByArtist(token, artist_id)
    return jsonify(tracks)



if __name__ == '__main__':
    app.run(debug=True)