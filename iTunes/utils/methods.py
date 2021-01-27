from general_utils.methods import normalize_string


def full_match_artist_song_in_tracks(artist, song, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'artistName' in track and 'trackName' in track:
            if normalize_string(track['artistName']) == normalize_string(artist) and \
                    normalize_string(track['trackName']) == normalize_string(song):
                return True, track
    return False, None


def full_match_artist_album_in_tracks(artist, album, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'collectionName' in track and 'artistName' in track:
            if normalize_string(track['collectionName']) == normalize_string(album) and \
                    normalize_string(track['artistName']) == normalize_string(artist):
                return True, track
    return False, None
