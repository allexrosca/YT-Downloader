from general_utils.methods import normalize_string


def full_match_artist_song_in_tracks(artist, song, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'artistName' in track and 'trackName' in track:
            if normalize_string(track['artistName']) == artist and \
                    normalize_string(track['trackName']) == song:
                return True, track
    return False, None


def full_match_artist_album_in_tracks(artist, album, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'collectionName' in track and 'artistName' in track:
            if normalize_string(track['collectionName']) == album and \
                    normalize_string(track['artistName']) == artist:
                return True, track
    return False, None
