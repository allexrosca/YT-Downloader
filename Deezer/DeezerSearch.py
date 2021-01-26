import requests
from general_utils.methods import normalize_string


class DeezerSearch:
    def __init__(self, max_tracks_to_search=50):
        self._max_tracks_to_search = max_tracks_to_search

    def search_artist(self, artist=''):
        if not artist:
            return -1
        else:
            artist = normalize_string(artist)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=artist:"{artist}"'
        response = requests.get(link)
        artist_found = False
        artist_found_index = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'artist' in track:
                    if 'name' in track['artist']:
                        if normalize_string(track['artist']['name']) == artist:
                            artist_found = True
                            artist_found_index = track

        return artist_found, artist_found_index

    def search_song(self, song=''):
        if not song:
            return -1
        else:
            song = normalize_string(song)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=track:"{song}"'
        response = requests.get(link)
        song_found = False
        song_found_index = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'title' in track:
                    if normalize_string(track['title']) == song:
                        song_found = True
                        song_found_index = track

        return song_found, song_found_index

    def search_album(self, album=''):
        if not album:
            return -1
        else:
            album = normalize_string(album)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=album:"{album}"'
        response = requests.get(link)
        album_found = False
        album_found_index = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'album' in track:
                    if 'title' in track['album']:
                        if normalize_string(track['album']['title']) == album:
                            album_found = True
                            album_found_index = track

        return album_found, album_found_index

    def search_artist_song(self, artist=None, song=None, max_tracks_to_search=None):
        if max_tracks_to_search is None:
            max_tracks_to_search = self._max_tracks_to_search

        if not artist or not song:
            return -1

        artist = normalize_string(artist)
        song = normalize_string(song)

        link = f'https://api.deezer.com/search?output=json&limit={max_tracks_to_search}&q=track:"{artist}{song}"'
        response = requests.get(link)
        song_found = False
        song_found_index = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'title' in track and 'artist' in track:
                    if 'name' in track['artist']:
                        if normalize_string(track['title']) == song and \
                                normalize_string(track['artist']['name']) == artist:
                            song_found = True
                            song_found_index = track

        if not song_found:
            backup_link = f'https://api.deezer.com/search?output=json&limit={max_tracks_to_search}&q="{song}"'
            backup_response = requests.get(backup_link)

            if backup_response.status_code == 200:
                for track in backup_response.json()['data']:
                    if 'title' in track and 'artist' in track:
                        if 'name' in track['artist']:
                            if normalize_string(track['title']) == song and \
                                    normalize_string(track['artist']['name']) == artist:
                                song_found = True
                                song_found_index = track

        if not song_found and max_tracks_to_search < 200:
            song_found, song_found_index = self.search_artist_song(artist, song, max_tracks_to_search=200)

        return song_found, song_found_index

# TODO: search_artist_album
