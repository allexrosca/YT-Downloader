from __future__ import unicode_literals
import youtube_dl
import ytdl_config
from useful_methods import check_and_create_folder
import os
from func_timeout import *
from PySide2 import QtCore
from pytube import Playlist


class DownloadPlaylist(QtCore.QThread, QtCore.QObject):
    playlist_length = QtCore.Signal(int)
    playlist_link_index = QtCore.Signal(int)
    current_link_index = QtCore.Signal(int)
    download_status = QtCore.Signal(bool)

    def __init__(self, download_content, ydl_opts={}, other_options={}, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.download_content = download_content
        self.ydl_opts = ydl_opts
        self._other_options = other_options
        self.current_song = ''
        self.terminate_thread = False
        self.songs_number = 0

    def run(self):
        not_accessible_links = []
        download_error_flag = False
        if self._other_options['downloadFolder']:
            check_and_create_folder(self._other_options['downloadFolder'])
        else:
            check_and_create_folder(ytdl_config.DOWNLOAD_FOLDER)
        download_error = 0

        current_index = 0
        for link in self.download_content:
            if self.terminate_thread:
                break

            self.current_link_index.emit(current_index)

            if str(link).find('playlist') != -1 or str(link).find('list') != -1:
                self.playlist_link_index.emit(self.download_content.index(link) + 1)
                link = Playlist(link)
                self.playlist_length.emit(len(link))
            else:
                link = [link]

            for song_link in link:
                if self.terminate_thread:
                    break
                self.current_song = song_link
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    try:
                        ydl.cache.remove()
                        ydl.download([song_link])
                    except Exception as e:
                        download_error_flag = True
                        download_error = str(e)

                if download_error:
                    not_accessible_links.append((song_link, download_error))

            if download_error_flag:
                self.download_status.emit(False)
            else:
                self.download_status.emit(True)

            if self.terminate_thread:
                break
            current_index = current_index + 1
            download_error_flag = False

        if len(not_accessible_links):

            if self._other_options['downloadFolder']:
                errors_folder = os.path.join(self._other_options['downloadFolder'], 'errors')
                check_and_create_folder(errors_folder)
            else:
                errors_folder = check_and_create_folder(ytdl_config.ERRORS_FOLDER)

            if not_accessible_links:
                file = open(os.path.join(errors_folder, 'not_accessible_links.txt'), 'w')
                file.write('\n'.join(str(link) + ' -> ' + str(error) + '\n' for link, error in not_accessible_links))
                file.close()

def question():
    question = input('\n\nDo you want to manually write the link?\n\tYes - you can manually paste the links\n\tSpace + Enter (or wait 3 seconds) - skip this step\n\n').lower().strip()
    return question


def main():
    links = []
    try:
        manual_input = func_timeout(3, question)
    except FunctionTimedOut:
        manual_input = ''

    if manual_input == 'yes':
        print('Paste link(s) here:')
        while True:
            link = input()
            if link == '':
                print('Closing...')
                break
            links.append(link)

    elif manual_input == '':
        print('Using saved links...\n')
        if ytdl_config.single_song_url_defined():
            links = ytdl_config.SINGLE_SONG_URL
        else:
            links = ytdl_config.PLAYLIST_URL

    else:
        print('Yes or Enter only!')
        return

    if isinstance(links, list):
        DownloadPlaylist(links, ytdl_config.CONFIG).run()
    else:
        DownloadPlaylist([links], ytdl_config.CONFIG).run()


if __name__ == "__main__":
    main()