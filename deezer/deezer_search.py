import requests
from general_utils.methods import normalize_string
from .utils.methods import full_match_artist_song_in_tracks, full_match_artist_album_in_tracks


class DeezerSearch:
    def __init__(self, max_tracks_to_search=50):
        self._max_tracks_to_search = max_tracks_to_search

    def _normalize_search_items(self, max_tracks_to_search=None, *item_list):
        if max_tracks_to_search is None:
            max_tracks_to_search = self._max_tracks_to_search

        normalized_items = []
        if item_list:
            for item in item_list:
                if not item:
                    return -1
                normalized_items.append(normalize_string(item))
        return (max_tracks_to_search, *normalized_items)

    @staticmethod
    def _get_tracks(filters, max_tracks_to_search):
        link = f'https://api.deezer.com/search?output=json&limit={max_tracks_to_search}&q='
        for key, value in filters.items():
            link = link + f'{key}:"{value}",'
        return requests.get(link[:-1])

    def search_artist(self, artist, max_tracks_to_search=None):
        max_tracks_to_search, artist = self._normalize_search_items(max_tracks_to_search, artist)
        response = self._get_tracks({'artist': artist}, max_tracks_to_search)

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'artist' in track and 'name' in track['artist']:
                    if normalize_string(track['artist']['name']) == normalize_string(artist):
                        return True, track['artist']['name']
        return False, None

    def search_song(self, song, max_tracks_to_search=None):
        max_tracks_to_search, song = self._normalize_search_items(max_tracks_to_search, song)
        response = self._get_tracks({'track': song}, max_tracks_to_search)
        if response.status_code == 200:
            for track in response.json()['data']:
                if 'title' in track:
                    if normalize_string(track['title']) == normalize_string(song):
                        return True, track['title']
        return False, None

    def search_album(self, album, max_tracks_to_search=None):
        max_tracks_to_search, album = self._normalize_search_items(max_tracks_to_search, album)
        response = self._get_tracks({'album': album}, max_tracks_to_search)

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'album' in track and 'title' in track['album']:
                    if normalize_string(track['album']['title']) == normalize_string(album):
                        return True, track['album']['title']
        return False, None

    def search_artist_song(self, artist=None, song=None, max_tracks_to_search=None):
        full_match = False
        full_match_index = None

        max_tracks_to_search, artist, song = self._normalize_search_items(max_tracks_to_search, artist, song)

        response = self._get_tracks({'artist': artist, 'track': song}, max_tracks_to_search)
        if response.status_code == 200 and response.json()['total']:
            full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, response.json()['data'])

        if not full_match:
            backup_response = self._get_tracks({'track': song}, max_tracks_to_search)

            if backup_response.status_code == 200 and backup_response.json()['total']:
                full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, backup_response.json()['data'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_song(artist, song, max_tracks_to_search=200)

        return full_match, full_match_index

    def search_artist_album(self, artist=None, album=None, max_tracks_to_search=None):
        full_match = False
        full_match_index = None

        max_tracks_to_search, artist, album = self._normalize_search_items(max_tracks_to_search, artist, album)

        response = self._get_tracks({'artist': artist, 'album': album}, max_tracks_to_search)
        if response.status_code == 200 and response.json()['total']:
            full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, response.json()['data'])

        if not full_match:
            backup_response = self._get_tracks({'album': album}, max_tracks_to_search)
            if backup_response.status_code == 200 and backup_response.json()['total']:
                full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, backup_response.json()['data'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_album(artist, album, max_tracks_to_search=200)
        return full_match, full_match_index
