import requests
import unidecode
import re


class iTunesSearch(object):
    def __init__(self, max_tracks_to_search=10):
        self._max_tracks_to_search = max_tracks_to_search

    def _normalizeString(self, string):
        string = unidecode.unidecode(string.lower())
        string = string.strip()
        return string

    def _normalizeStringForSearch(self, string):
        string = unidecode.unidecode(string.lower())
        string = string.strip()
        string = str(string).replace(' ', '+')
        string = re.sub(r'(\(.*\))', '', string)
        string = string.strip()
        return string

    def searchArtistAndSong(self, artist='', song=''):
        if not artist or not song:
            return -1
        else:
            artist = self._normalizeString(artist)
            song = self._normalizeString(song)

        artistForSearch = self._normalizeStringForSearch(artist)
        songForSearch = self._normalizeStringForSearch(song)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={artistForSearch}+{songForSearch}'
        response = requests.get(link)

        fullMatch = False
        fullMatchIndex = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'artistName' in track and 'trackName' in track:
                    if self._normalizeString(track['artistName'].lower()) == artist and \
                            self._normalizeString(track['trackName'].lower()) == song:
                        fullMatch = True
                        fullMatchIndex = track

        return (fullMatch, fullMatchIndex)

    def searchArtist(self, artist=''):
        if not artist:
            return -1
        else:
            artist = self._normalizeString(artist)

        artistForSearch = self._normalizeStringForSearch(artist)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={artistForSearch}'
        response = requests.get(link)
        artistFound = False
        artistFoundIndex = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'artistName' in track:
                    if self._normalizeString(track['artistName'].lower()) == artist:
                        artistFound = True
                        artistFoundIndex = track

        return (artistFound, artistFoundIndex)

    def searchSong(self, song):
        if not song:
            return -1
        else:
            song = self._normalizeString(song)

        songForSearch = self._normalizeStringForSearch(song)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={songForSearch}'
        response = requests.get(link)

        songFound = False
        songFoundIndex = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'trackName' in track:
                    if self._normalizeString(track['trackName'].lower()) == song:
                        songFound = True
                        songFoundIndex = track

        return (songFound, songFoundIndex)

    def searchAlbum(self, album= ''):
        if not album:
            return -1
        else:
            album = self._normalizeString(album)

        albumForSearch = self._normalizeStringForSearch(album)
        link = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={albumForSearch}'
        response = requests.get(link)
        albumFound = False
        albumFoundIndex = False
        if response.status_code == 200:
            for track in response.json()['results']:
                if 'collectionName' in track:
                    if self._normalizeString(track['collectionName'].lower()) == album:
                        albumFound = True
                        albumFoundIndex = track
        return (albumFound, albumFoundIndex)

    def searchAlbumOfArtist(self, artist= '', album = ''):
        if not album or not artist:
            return -1
        else:
            artist = self._normalizeString(artist)
            album = self._normalizeString(album)

        albumForSearch = self._normalizeStringForSearch(album)
        artistForSearch = self._normalizeStringForSearch(artist)
        link1 = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={albumForSearch}'
        link2 = f'https://itunes.apple.com/search?explicit=yes&media=music&limit={self._max_tracks_to_search}&term={artistForSearch}+{albumForSearch}'
        response1 = requests.get(link1)
        response2 = requests.get(link2)
        albumFound = False
        albumFoundIndex = False
        if response1.status_code == 200:
            for track in response1.json()['results']:
                if 'collectionName' in track and 'artistName' in track:
                    if self._normalizeString(track['collectionName'].lower()) == album and\
                            self._normalizeString(track['artistName'].lower()) == artist:
                        albumFound = True
                        albumFoundIndex = track
        elif response2.status_code == 200:
            for track in response2.json()['results']:
                if 'collectionName' in track and 'artistName' in track:
                    if self._normalizeString(track['collectionName'].lower()) == album and\
                            self._normalizeString(track['artistName'].lower()) == artist:
                        albumFound = True
                        albumFoundIndex = track
        return (albumFound, albumFoundIndex)