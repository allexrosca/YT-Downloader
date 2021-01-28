import requests
from general_utils.methods import normalize_string
from utils.methods import full_match_artist_song_in_tracks, full_match_artist_album_in_tracks


class iTunesSearch:
    def __init__(self, max_tracks_to_search=50):
        self._max_tracks_to_search = max_tracks_to_search

    @staticmethod
    def _normalize_string_for_search(string):
        return str(normalize_string(string).replace(' ', '+'))

    def _normalize_search_items(self, max_tracks_to_search=None, *item_list):
        if max_tracks_to_search is None:
            max_tracks_to_search = self._max_tracks_to_search

        normalized_items = []
        if item_list:
            for item in item_list:
                if not item:
                    return -1
                normalized_items.append(self._normalize_string_for_search(normalize_string(item)))
        return (max_tracks_to_search, *normalized_items)

    @staticmethod
    def _get_tracks(filters, max_tracks_to_search):
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={max_tracks_to_search}&term='
        for value in filters:
            link = link + f'{value}+'
        return requests.get(link[:-1])

    def search_artist(self, artist, max_tracks_to_search=None):
        max_tracks_to_search, artist_search_normalized = self._normalize_search_items(max_tracks_to_search, artist)

        response = self._get_tracks([artist_search_normalized], max_tracks_to_search)
        if response.status_code == 200 and response.json()['resultCount']:
            for track in response.json()['results']:
                if 'artistName' in track:
                    if normalize_string(track['artistName']) == normalize_string(artist):
                        return True, track
        return False, None

    def search_song(self, song, max_tracks_to_search=None):
        max_tracks_to_search, song_search_normalized = self._normalize_search_items(max_tracks_to_search, song)

        response = self._get_tracks([song_search_normalized], max_tracks_to_search)
        if response.status_code == 200 and response.json()['resultCount']:
            for track in response.json()['results']:
                if 'trackName' in track:
                    if normalize_string(track['trackName']) == normalize_string(song):
                        return True, track
        return False, None

    def search_album(self, album, max_tracks_to_search=None):
        max_tracks_to_search, album_search_normalized = self._normalize_search_items(max_tracks_to_search, album)

        response = self._get_tracks([album_search_normalized], max_tracks_to_search)
        if response.status_code == 200 and response.json()['resultCount']:
            for track in response.json()['results']:
                if 'collectionName' in track:
                    if normalize_string(track['collectionName']) == normalize_string(album):
                        return True, track
        return False, None

    def search_artist_song(self, artist, song, max_tracks_to_search=None):
        full_match = False
        full_match_index = None

        max_tracks_to_search, artist_for_search, artist_song_for_search = self._normalize_search_items(max_tracks_to_search, artist, song)

        response = self._get_tracks([artist_for_search, artist_song_for_search], max_tracks_to_search)
        if response.status_code == 200 and response.json()['resultCount']:
            full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, response.json()['results'])

        if not full_match:
            backup_response = self._get_tracks([artist_song_for_search], max_tracks_to_search)

            if backup_response.status_code == 200 and backup_response.json()['resultCount']:
                full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, backup_response.json()['results'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_song(artist, song, max_tracks_to_search=200)

        return full_match, full_match_index

    def search_artist_album(self, artist=None, album=None, max_tracks_to_search=None):
        full_match = False
        full_match_index = None

        max_tracks_to_search, artist_for_search, artist_album_for_search = self._normalize_search_items(max_tracks_to_search, artist, album)

        response = self._get_tracks([artist_for_search, artist_album_for_search], max_tracks_to_search)
        if response.status_code == 200 and response.json()['resultCount']:
            full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, response.json()['results'])

        if not full_match:
            backup_response = self._get_tracks([artist_album_for_search], max_tracks_to_search)

            if backup_response.status_code == 200 and backup_response.json()['resultCount']:
                full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, backup_response.json()['results'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_album(artist, album, max_tracks_to_search=200)

        return full_match, full_match_index
