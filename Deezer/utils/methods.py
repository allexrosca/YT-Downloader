from general_utils.methods import normalize_string


def full_match_artist_song_in_tracks(artist, song, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'artist' in track and 'name' in track['artist'] and 'title' in track:
            if normalize_string(track['artist']['name']) == normalize_string(artist) and \
                    normalize_string(track['title']) == normalize_string(song):
                return True, track
    return False, None


def full_match_artist_album_in_tracks(artist, album, track_list):
    # TODO: decide what to do with multiple full matches (currently, taking just the first full match)
    for track in track_list:
        if 'artist' in track and 'name' in track['artist'] and \
                'album' in track and 'title' in track['album']:
            if normalize_string(track['artist']['name']) == normalize_string(artist) and \
                    normalize_string(track['album']['title']) == normalize_string(album):
                return True, track
    return False, None
