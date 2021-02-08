from __future__ import unicode_literals
import os
from PySide2 import QtCore
from pytube import Playlist
from general_utils.methods import check_and_create_folder, generate_error_folder_path
from youtube_dl import YoutubeDL


class PlaylistDownloader(QtCore.QThread, QtCore.QObject):
    playlist_length = QtCore.Signal(int)
    playlist_link_index = QtCore.Signal(int)
    current_link_index = QtCore.Signal(int)
    download_status = QtCore.Signal(bool)

    def __init__(self, download_content, download_folder, ydl_opts=None, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        if ydl_opts is None:
            ydl_opts = {}
        self.download_content = download_content
        self.ydl_opts = ydl_opts
        self._download_folder = download_folder
        self.current_song = ''
        self.terminate_thread = False
        self.songs_number = 0

    def download(self, ydl_opts=None):
        check_and_create_folder(self._download_folder)

        if ydl_opts is None:
            ydl_opts = self.ydl_opts

        current_index = 0
        download_error_flag = False
        not_accessible_links = []

        with YoutubeDL(ydl_opts) as ydl:
            for link in self.download_content:
                if self.terminate_thread:
                    break

                self.current_link_index.emit(current_index)

                for song_link in self._prepare_link(link):
                    if self.terminate_thread:
                        break

                    self.current_song = song_link

                    try:
                        ydl.cache.remove()
                        link_info = ydl.extract_info(song_link, download=True)
                        if link_info:
                            if 'title' in link_info and link_info['title']:
                                pass
                            else:
                                pass
                        else:
                            pass
                    except Exception as e:
                        download_error_flag = True
                        not_accessible_links.append((song_link, e))

                if download_error_flag:
                    self.download_status.emit(False)
                else:
                    self.download_status.emit(True)

                if self.terminate_thread:
                    break

                current_index = current_index + 1
                download_error_flag = False

        return not_accessible_links

    def _prepare_link(self, link):
        if str(link).find('playlist') != -1 or str(link).find('list') != -1:
            self.playlist_link_index.emit(self.download_content.index(link) + 1)
            link = Playlist(link)
            # link._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")  # TODO: if everything works without this line, delete it in the future
            self.playlist_length.emit(len(link))
            return link
        return [link]

    def run(self):
        not_accessible_links = self.download()

        if not_accessible_links and len(not_accessible_links):
            errors_folder_path = generate_error_folder_path(self._download_folder)
            check_and_create_folder(errors_folder_path)

            file = open(os.path.join(errors_folder_path, 'not_accessible_links.txt'), 'w')
            file.write('\n'.join(str(link) + ' -> ' + str(error) + '\n' for link, error in not_accessible_links))
            file.close()
