from general_utils.methods import check_and_create_folder
import os
from PySide2 import QtCore
from general_utils.constants import ERRORS_FOLDER, DOWNLOAD_FOLDER


class DownloadLogger(QtCore.QObject):
    message_signal = QtCore.Signal(str)

    def __init__(self, download_folder=None):
        super().__init__()
        if download_folder is None:
            download_folder = ERRORS_FOLDER
        self._warning_found = False
        self._error_found = False
        self._error_folder = os.path.join(download_folder, 'errors')
        if os.path.isdir(self._error_folder):
            for file_object in os.listdir(self._error_folder):
                file_object_path = os.path.join(self._error_folder, file_object)
                if os.path.isfile(file_object_path):
                    os.remove(file_object_path)

    def debug(self, status):
        if status.find('[download] Destination:') != -1:
            message = 'Downloading: ' \
                      + (str(status).replace('[download] Destination:', '').strip().split('\\')[-1]).rsplit('.', 1)[0]
            print(message)
            self.message_signal.emit(message)
        if status.find('[download]') != -1 and status.find('Destination') == -1 and status.find('[download] Downloading') == -1 \
                and float(str(status).replace('[download]', '').strip().split('of')[0].replace('%', '').strip()) < 100.0:
            message = 'Progress: ' \
                      + str(status).replace('[download]', '').strip().split('of')[0].strip()
            print('\t' + message)
            self.message_signal.emit(message)
        if status.find('[download] 100%') != -1:
            message = 'Download finished!'
            print('\t' + message)
            self.message_signal.emit(message)
        if status.find('[ffmpeg] Destination:') != -1:
            message = 'Converting file to mp3...'
            print(message)
            self.message_signal.emit(message)
        if status.find('[ffmpeg] Adding metadata') != -1:
            message = 'Convert finished!\n'
            print('\t' + message)
            self.message_signal.emit(message)

    def warning(self, msg):
        if not os.path.isdir(self._error_folder):
            check_and_create_folder(self._error_folder)
        with open(os.path.join(self._error_folder, 'warnings.txt'), 'a') as file:
            file.write(str(msg) + '\n')

        if not self._warning_found:
            self.message_signal.emit('\nWarnings can be found in \\errors\\warnings.txt file\n')
            self._warning_found = True

    def error(self, msg):
        if not os.path.isdir(self._error_folder):
            check_and_create_folder(self._error_folder)
        with open(os.path.join(self._error_folder, 'unrecognised_errors.txt'), 'a') as file:
            file.write(str(msg) + '\n')

        if not self._error_found:
            self.message_signal.emit('\nErrors can be found in \\errors\\unrecognised_errors.txt file\n')
            self._error_found = True


# noinspection SpellCheckingInspection
CONFIG = {
    'format': 'bestaudio/best',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        },

        {
            'key': 'FFmpegMetadata',
        },
    ],
    'prefer_ffmpeg': True,
    'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',  # TODO: maybe it's better to use alt_title?
}
