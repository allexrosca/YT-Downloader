import os
from tinytag import TinyTag
from itunes.itunes_search import iTunesSearch
import json
import unidecode


class getInfoForDB(object):
    def __init__(self, accepted_file_types=None):
        if accepted_file_types is None:
            self._accepted_file_types = ['.mp3', '.mp4']
        self._artists = set()
        self._albums = set()
        self._artists_and_albums = set()

    def getArtits(self):
        return self._artists

    def getAlbums(self):
        return self._albums

    def _normalizeString(self, string):
        string = unidecode.unidecode(string.lower())
        string = string.strip()
        return string

    def _write_in_json_file(self, data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _find_or_create_db_file(self, file_path):
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            default_info = {'artists': [],
                            'albums': []}
            with open(file_path, 'w') as file:
                json.dump(default_info, file, indent=2)
        else:
            with open(file_path) as file:
                file_data = json.load(file)
                if not 'artists' in file_data:
                    file_data.update({'artists': []})
                if not 'albums' in file_data:
                    file_data.update({'albums': []})
            self._write_in_json_file(file_data, file_path)

    def _find_or_create_file(self, file_path):
        if not os.path.isfile(file_path):
            file = open(file_path, 'w')
            file.close()

    def _write_not_found_data(self, data, file_path):
        self._find_or_create_file(file_path)
        file = open(file_path, 'r')
        info_to_write = file.read().split('\n')
        file.close()
        file = open(file_path, 'w')
        for i in data:
            info_to_write.append(i)
        info_to_write = set(filter(None, info_to_write))

        for i in info_to_write:
            file.write(str(unidecode.unidecode(i)) + '\n')
        file.close()

    def getInfoFromFolder(self, folder_path):
        for subdir, dirs, files in os.walk(folder_path):
            for file in files:
                song = os.path.join(subdir, file)
                if os.path.splitext(file)[-1] in self._accepted_file_types:
                    tags = TinyTag.get(song)
                    if tags.artist:
                        self._artists.add(tags.artist)
                    if tags.album:
                        self._albums.add(tags.album)
                    if tags.artist and tags.album:
                        self._artists_and_albums.add((tags.artist, tags.album))
        self._artists = set(filter(None, self._artists))
        self._albums = set(filter(None, self._albums))
        self._artists_and_albums = set(filter(None, self._artists_and_albums))  # nu e bun nush de ce

    def verifyArtists(self):
        artists_found = set()
        artists_not_found = set()
        for artist_name in self._artists:
            search = iTunesSearch(max_tracks_to_search=100)
            search_result = search.search_artist(artist_name)
            if search_result != -1 and search_result[0]:
                artists_found.add(artist_name)
            else:
                artists_not_found.add(artist_name)
        return (artists_found, artists_not_found)

    def verifyAlbums(self):
        albums_found = set()
        albums_not_found = set()
        for albums_name in self._albums:
            search = iTunesSearch(max_tracks_to_search=100)
            search_result = search.search_album(albums_name)
            if search_result != -1 and search_result[0]:
                albums_found.add(albums_name)
            else:
                albums_not_found.add(albums_name)
        return (albums_found, albums_not_found)

    def verifyAlbumOfArtist(self):
        albums_found = set()
        albums_not_found = set()
        for artist_name, albums_name in self._artists_and_albums:
            search = iTunesSearch(max_tracks_to_search=200)
            search_result = search.search_artist_album(artist_name, albums_name)
            if search_result != -1 and search_result[0]:
                albums_found.add(albums_name)
            else:
                albums_not_found.add(albums_name)
        return (albums_found, albums_not_found)

    def updateArtistsInFile(self, file_path, write_not_found=True):
        verified_artists, artists_not_found = self.verifyArtists()
        self._find_or_create_db_file(file_path)
        with open(file_path) as db:
            db_info = json.load(db)
            artists = db_info['artists']
            for artist in verified_artists:
                if artist not in artists:
                    artists.append(unidecode.unidecode(artist))
        self._write_in_json_file(db_info, file_path)

        if write_not_found:
            if len(artists_not_found):
                self._write_not_found_data(artists_not_found, 'artists_not_found.txt')

    def updateAlbumsInFile(self, file_path, write_not_found=True):
        verified_albums, albums_not_found = self.verifyAlbums()
        self._find_or_create_db_file(file_path)
        with open(file_path) as db:
            db_info = json.load(db)
            albums = db_info['albums']
            for album in verified_albums:
                if album not in albums:
                    albums.append(unidecode.unidecode(album))
        self._write_in_json_file(db_info, file_path)

        if write_not_found:
            if len(albums_not_found):
                self._write_not_found_data(albums_not_found, 'albums_not_found.txt')

    def updateAlbumOfArtistInFile(self, file_path, write_not_found=True):
        verified_albums, albums_not_found = self.verifyAlbumOfArtist()
        self._find_or_create_db_file(file_path)
        with open(file_path) as db:
            db_info = json.load(db)
            albums = db_info['albums']
            for album in verified_albums:
                if album not in albums:
                    albums.append(unidecode.unidecode(album))
        self._write_in_json_file(db_info, file_path)

        if write_not_found:
            if len(albums_not_found):
                self._write_not_found_data(albums_not_found, 'albums_not_found.txt')


i = getInfoForDB()
i.getInfoFromFolder(r'D:\Muzica')
i.updateArtistsInFile('db.json', False)
i.updateAlbumOfArtistInFile('db.json', False)
i.updateAlbumsInFile('db.json', False)
