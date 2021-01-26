from __future__ import unicode_literals
import youtube_dl
import ytdl_config
from general_utils.methods import check_and_create_folder
import os
from PySide2 import QtCore
from pytube import Playlist
import re


class DownloadPlaylist(QtCore.QThread, QtCore.QObject):
    playlist_length = QtCore.Signal(int)
    playlist_link_index = QtCore.Signal(int)
    current_link_index = QtCore.Signal(int)
    download_status = QtCore.Signal(bool)

    def __init__(self, download_content, ydl_opts=None, other_options=None, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        if other_options is None:
            other_options = {}
        if ydl_opts is None:
            ydl_opts = {}
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
                link._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
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
