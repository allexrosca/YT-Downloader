import json
import requests
import unidecode

class DeezerSearch(object):
    def __init__(self, max_tracks_to_search=50):
        self._max_tracks_to_search = max_tracks_to_search

    def _normalizeString(self, string):
        string = unidecode.unidecode(string.lower())
        string = string.strip()
        return string

    def searchArtist(self, artist=''):
        if not artist:
            return -1
        else:
            artist = self._normalizeString(artist)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=artist:"{artist}"'
        response = requests.get(link)
        artistFound = False
        artistFoundIndex = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'artist' in track:
                    if 'name' in track['artist']:
                        if self._normalizeString(track['artist']['name']) == artist:
                            artistFound = True
                            artistFoundIndex = track

        return (artistFound, artistFoundIndex)

    def searchSong(self, song=''):
        if not song:
            return -1
        else:
            song = self._normalizeString(song)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=track:"{song}"'
        response = requests.get(link)
        songFound = False
        songFoundIndex = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'title' in track:
                    if self._normalizeString(track['title']) == song:
                        songFound = True
                        songFoundIndex = track

        return (songFound, songFoundIndex)

    def searchAlbum(self, album=''):
        if not album:
            return -1
        else:
            album = self._normalizeString(album)

        link = f'https://api.deezer.com/search?output=json&limit={self._max_tracks_to_search}&q=album:"{album}"'
        response = requests.get(link)
        albumFound = False
        albumFoundIndex = False

        if response.status_code == 200:
            for track in response.json()['data']:
                if 'album' in track:
                    if 'title' in track['album']:
                        if self._normalizeString(track['album']['title']) == album:
                            albumFound = True
                            albumFoundIndex = track

        return (albumFound, albumFoundIndex)


    def searchSongOfArtist(self, artist='', song='', max_tracks_to_search=None):
        if max_tracks_to_search == None:
            max_tracks_to_search = self._max_tracks_to_search

        if not artist or not song:
            return -1
        else:
            artist = self._normalizeString(artist)
            song = self._normalizeString(song)

        link = f'https://api.deezer.com/search?output=json&limit={max_tracks_to_search}&q=track:"{song}"'
        response = requests.get(link)
        songFound = False
        songFoundIndex = False

        if response.status_code == 200:
            for track in response.json()['data']:
                print(track)
                if 'title' in track and 'artist' in track:
                    if 'name' in track['artist']:
                        if self._normalizeString(track['title']) == song and \
                                self._normalizeString(track['artist']['name']) == artist:
                            songFound = True
                            songFoundIndex = track

        if not songFound:
            backup_link = f'https://api.deezer.com/search?output=json&limit={max_tracks_to_search}&q="{artist}{song}"'
            backup_response = requests.get(backup_link)

            if backup_response.status_code == 200:
                for track in backup_response.json()['data']:
                    if 'title' in track and 'artist' in track:
                        if 'name' in track['artist']:
                            if self._normalizeString(track['title']) == song and \
                                    self._normalizeString(track['artist']['name']) == artist:
                                songFound = True
                                songFoundIndex = track

        if not songFound and self._max_tracks_to_search < 200:
            songFound, songFoundIndex = self.searchSongOfArtist(artist,song, max_tracks_to_search= 200)

        return (songFound, songFoundIndex)

# de facut searchalbumofartist