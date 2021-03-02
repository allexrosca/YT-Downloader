from .checker import MetadataChecker


def check_metadata(audio_file, song_title):
    metadata_checker = MetadataChecker(audio_file, song_title)
    metadata_checker.check_file_artist()
    metadata_checker.check_file_song_title()
