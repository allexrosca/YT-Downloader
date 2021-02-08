from deezer.deezer_search import DeezerSearch
from itunes.itunes_search import iTunesSearch


class MetadataChecker:
    def __init__(self, audio_file, song_title):
        self._audio_file = audio_file
        self._song_title = song_title

    @staticmethod
    def check_artist_exists(artist_name):
        status, itunes_artist_name = iTunesSearch().search_artist(artist_name)
        if status:
            return status, itunes_artist_name

        status, deezer_artist_name = DeezerSearch().search_artist(artist_name)
        if status:
            return status, deezer_artist_name
        return False, None

    @staticmethod
    def check_song_title_exists(song_title):
        status, itunes_song_title = iTunesSearch().search_song(song_title)
        if status:
            return status, itunes_song_title

        status, deezer_song_title = DeezerSearch().search_song(song_title)
        if status:
            return status, deezer_song_title
        return False, None

    @staticmethod
    def check_artist_song_title_exists(artist, song_title):
        status, itunes_song_title = iTunesSearch().search_artist_song(artist, song_title)
        if status:
            return status, itunes_song_title

        status, deezer_song_title = DeezerSearch().search_artist_song(artist, song_title)
        if status:
            return status, deezer_song_title
        return False, None

    def _save_artist_tag_or_false(self, artist_name, audio_file):
        check_status, artist_name_tested = self.check_artist_exists(artist_name)
        if check_status:
            audio_file.tag.artist = artist_name_tested
            audio_file.tag.save()
            return True
        return False

    def _save_song_title_tag_or_false(self, song_title, audio_file):
        check_status, song_title_tested = self.check_song_title_exists(song_title)
        if check_status:
            audio_file.tag.title = song_title_tested
            audio_file.tag.save()
            return True
        return False

    def _save_artist_song_title_tag_or_false(self, artist, song_title, audio_file):
        check_status, song_title_tested = self.check_artist_song_title_exists(artist, song_title)
        if check_status:
            audio_file.tag.title = song_title_tested
            audio_file.tag.save()
            return True
        return False

    def check_artist(self, song_title=None, audio_file=None):
        if audio_file is None:
            audio_file = self._audio_file
        if song_title is None:
            song_title = self._song_title

        status = self._save_artist_tag_or_false(audio_file.tag.artist, audio_file)
        if status:
            return True
        else:
            if song_title.find('-') != -1:
                song_title_split = song_title.split('-')
                status = self._save_artist_tag_or_false(song_title_split[0], audio_file)
                if status:
                    return True
                else:
                    return self._save_artist_tag_or_false(song_title_split[1], audio_file)
        return False

    def check_song_title(self, song_title=None, audio_file=None):
        if audio_file is None:
            audio_file = self._audio_file
        if song_title is None:
            song_title = self._song_title

        status = self._save_song_title_tag_or_false(audio_file.tag.title, audio_file)
        if status:
            return True
        else:
            if song_title.find('-') != -1:
                song_title_split = song_title.split('-')
                status = self._save_song_title_tag_or_false(song_title_split[1], audio_file)
                if status:
                    return True
                else:
                    return self._save_song_title_tag_or_false(song_title_split[0], audio_file)
        return False

    def check_artist_song_title(self, song_title=None, audio_file=None):
        if audio_file is None:
            audio_file = self._audio_file
        if song_title is None:
            song_title = self._song_title

        status = self._save_artist_song_title_tag_or_false(audio_file.tag.artist, audio_file.tag.title, audio_file)
        if status:
            return True
        else:
            if song_title.find('-') != -1:
                song_title_split = song_title.split('-')
                status = self._save_artist_song_title_tag_or_false(audio_file.tag.artist, song_title_split[1], audio_file)
                if status:
                    return True
                else:
                    return self._save_artist_song_title_tag_or_false(audio_file.tag.artist, song_title_split[0], audio_file)
        return self.check_song_title(song_title, audio_file)
