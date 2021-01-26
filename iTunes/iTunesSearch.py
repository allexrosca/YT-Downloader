import requests
import unidecode
import re
from iTunes.utils.methods import full_match_artist_song_in_tracks, full_match_artist_album_in_tracks
from general_utils.methods import normalize_string


class iTunesSearch:
    def __init__(self, max_tracks_to_search=50):
        self._max_tracks_to_search = max_tracks_to_search

    @staticmethod
    def _normalize_string_for_search(string):
        string = unidecode.unidecode(string.lower())
        string = str(string.strip()).replace(' ', '+')
        string = re.sub(r'(\(.*\))', '', string)
        return string.strip()

    def _normalize_search_items(self, artist, artist_item, max_tracks_to_search=None):
        if max_tracks_to_search is None:
            max_tracks_to_search = self._max_tracks_to_search

        if not artist or not artist_item:
            return -1

        artist = normalize_string(artist)
        artist_item = normalize_string(artist_item)

        artist_for_search = self._normalize_string_for_search(artist)
        artist_item_for_search = self._normalize_string_for_search(artist_item)

        return artist_for_search, artist_item_for_search, max_tracks_to_search

    @staticmethod
    def _get_tracks(artist_for_search, artist_item_for_search, max_tracks_to_search, is_backup=False):
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={max_tracks_to_search}&term={artist_item_for_search}' if is_backup else \
            f'https://itunes.apple.com/search?explicit=yes&media=music&limit={max_tracks_to_search}&term={artist_for_search}+{artist_item_for_search}'
        return requests.get(link)

    def search_artist(self, artist):
        # TODO: raise exceptions in these cases
        if not artist:
            return -1

        artist = normalize_string(artist)

        artist_for_search = self._normalize_string_for_search(artist)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={artist_for_search}'
        response = requests.get(link)
        artist_found = False
        artist_found_index = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'artistName' in track:
                    if normalize_string(track['artistName']) == artist:
                        artist_found = True
                        artist_found_index = track

        return artist_found, artist_found_index

    def search_song(self, song):
        if not song:
            return -1

        song = normalize_string(song)

        song_for_search = self._normalize_string_for_search(song)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={song_for_search}'
        response = requests.get(link)

        song_found = False
        song_found_index = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'trackName' in track:
                    if normalize_string(track['trackName']) == song:
                        song_found = True
                        song_found_index = track

        return song_found, song_found_index

    def search_album(self, album):
        if not album:
            return -1

        album = normalize_string(album)

        album_for_search = self._normalize_string_for_search(album)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={album_for_search}'
        response = requests.get(link)
        album_found = False
        album_found_index = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'collectionName' in track:
                    if normalize_string(track['collectionName']) == album:
                        album_found = True
                        album_found_index = track
        return album_found, album_found_index

    def search_artist_song(self, artist=None, song=None, max_tracks_to_search=None):
        full_match = False
        full_match_index = False

        artist_for_search, artist_song_for_search, max_tracks_to_search = self._normalize_search_items(artist, song, max_tracks_to_search)

        response = self._get_tracks(artist_for_search, artist_song_for_search, max_tracks_to_search)
        if response.status_code == 200:
            full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, response.json()['results'])

        if not full_match:
            backup_response = self._get_tracks(artist_for_search, artist_song_for_search, max_tracks_to_search, True)

            if backup_response.status_code == 200:
                full_match, full_match_index = full_match_artist_song_in_tracks(artist, song, backup_response.json()['results'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_song(artist, song, max_tracks_to_search=200)

        return full_match, full_match_index

    def search_artist_album(self, artist=None, album=None, max_tracks_to_search=None):
        full_match = False
        full_match_index = False

        artist_for_search, artist_album_for_search, max_tracks_to_search = self._normalize_search_items(artist, album, max_tracks_to_search)

        response = self._get_tracks(artist_for_search, artist_album_for_search, max_tracks_to_search)
        if response.status_code == 200:
            full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, response.json()['results'])

        if not full_match:
            backup_response = self._get_tracks(artist_for_search, artist_album_for_search, max_tracks_to_search, True)

            if backup_response.status_code == 200:
                full_match, full_match_index = full_match_artist_album_in_tracks(artist, album, backup_response.json()['results'])

        if not full_match and max_tracks_to_search < 200:
            full_match, full_match_index = self.search_artist_album(artist, album, max_tracks_to_search=200)

        return full_match, full_match_index
