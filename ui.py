import ctypes
import os
import youtube_dl
import json
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QFileDialog, QCheckBox, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from downloader_logger import DownloadLogger
from downloader import PlaylistDownloader
from general_utils.methods import get_short_path
from general_utils.constants import CONFIG


class YTDownloaderUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._save_download_location = None

        if os.path.exists('config_data.json'):
            with open('config_data.json', 'r+') as config_file:
                data = json.load(config_file)
                self._download_folder = data['download_location']
                self._download_folder_to_show = data['download_location_short']
                self._location_saved = True
        else:
            self._download_folder = str(os.path.abspath(os.path.curdir))
            self._download_folder_to_show = str(os.path.abspath(os.path.curdir))
            self._location_saved = False

        self.buttons = {}
        self._init_ui()
        self._download_interrupted = False
        self._download_warning_found = False
        self._download_error_found = False

    def _create_button(self, name_list, button_size=(), font_size=16):
        if button_size:
            width = int(button_size[0])
            height = int(button_size[1])
            font_size = int((width + height) / font_size)
        else:
            width = int(self.width() / 4)
            height = int(self.height() / 9)
            font_size = int((width + height) / font_size)

        for name in name_list:
            buttons_design = 'QPushButton{color:#bfc1c1; ' \
                             'background-color:#07695A; ' \
                             f'font: {font_size}px; ' \
                             'border-radius: 10px;}' \
                             'QPushButton:hover {color:#524d4d; background-color: #0eb59c;}' \
                             'QPushButton:disabled {color:#087060; background-color: #075448;}'

            self.buttons[name] = QPushButton(name)
            self.buttons[name].setFixedSize(width, height)
            self.buttons[name].setStyleSheet(buttons_design)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self._userInputArea:
            if event.key() == QtCore.Qt.Key_Return and self._userInputArea.hasFocus():
                self._userInputArea.append('')
        return super().eventFilter(obj, event)

    def _set_initial_settings(self):
        self.setWindowTitle('Youtube Downloader')
        self.setFont(QtGui.QFont("Calibri", 10))
        ui_theme = QtGui.QPalette()
        ui_theme.setColor(QtGui.QPalette.Window, QtGui.QColor(35, 62, 58))
        ui_theme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(222, 222, 222))
        ui_theme.setColor(QtGui.QPalette.Text, QtGui.QColor(194, 234, 216))
        self.setPalette(ui_theme)

    def _create_title(self):
        self._title = QLabel('From Youtube to Mp3 (v0.0.1)')
        self._title.setFont(QtGui.QFont("Calibri", int((self.width() + self.height()) / 46)))

        self._title_layout = QHBoxLayout()
        self._title_layout.addWidget(self._title)
        self._title_layout.setContentsMargins(0, 20, 0, 40)

    def _create_buttons(self):
        self._create_button(['Download', 'Stop', 'Skip', 'Reset', 'Exit'])
        self._set_button_status(['Stop', 'Skip'], False)

        self._button_layout = QVBoxLayout()
        for button in self.buttons.values():
            self._button_layout.addWidget(button)
        self._button_layout.setContentsMargins(25, 0, 50, 10)

        self._create_button(['Change Folder'], (self.width() / 5, self.height() / 13), 13)
        self._create_button(['Open Download Folder'], (self.width() / 4, self.height() / 13))

    def _create_user_input_text_area(self):
        self._userInputArea = QTextEdit(self)
        self._userInputArea.setPlaceholderText("Paste your links here.\n")
        # noinspection SpellCheckingInspection
        self._userInputArea.setStyleSheet('color:#0eeae4; background-color:#43565c; border-radius: 7px')
        self._userInputArea.installEventFilter(self)

        self._text_area_layout = QVBoxLayout()
        self._text_area_layout.addWidget(self._userInputArea)
        self._text_area_layout.setContentsMargins(25, 10, 50, 20)

    def _create_download_folder_info(self):
        self._download_folder_label = QLabel('Download folder:')
        self._download_folder_label.setFont(QtGui.QFont("Calibri", int((self.width() + self.height()) / 100), QtGui.QFont.Bold))
        self._download_folder_label.setStyleSheet("QLabel {color: #a4d1de;}")
        self._download_folder_label.setContentsMargins(10, 0, 0, 0)

        self._download_folder_location = QLabel(self._download_folder_to_show)
        self._download_folder_location.setFont(QtGui.QFont("Calibri", int((self.width() + self.height()) / 100)))
        self._download_folder_location.setStyleSheet("QLabel {color: #02998f;}")

    def _create_save_download_location_checkbox(self):
        self._save_download_location = QCheckBox('save download location path')
        self._save_download_location.setFont(QtGui.QFont("Calibri", int((self.width() + self.height()) / 120)))
        self._save_download_location.setStyleSheet("QCheckBox {color: #02998f;}")

    def _create_download_folder_layout(self):
        self._download_folder_layout = QGridLayout()
        self._download_folder_layout.addWidget(self.buttons['Open Download Folder'], 1, 1)
        self._download_folder_layout.addWidget(self.buttons['Change Folder'], 1, 2)
        self._download_folder_layout.addWidget(self._download_folder_label, 1, 3)
        self._download_folder_layout.addWidget(self._download_folder_location, 1, 4)
        if not self._location_saved:
            self._download_folder_layout.addWidget(self._save_download_location, 2, 2, 1, -1)
        self._download_folder_layout.setContentsMargins(25, 0, 0, 0)

    def _create_main_layout(self):
        self._main_layout = QGridLayout()
        self._main_layout.addLayout(self._title_layout, 1, 1, 1, -1, alignment=QtCore.Qt.AlignCenter)
        self._main_layout.addLayout(self._text_area_layout, 2, 1)
        self._main_layout.addLayout(self._button_layout, 2, 2)
        self._main_layout.addLayout(self._download_folder_layout, 3, 1, alignment=QtCore.Qt.AlignLeft)
        self._main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self._main_layout)

    def _init_ui(self):
        self._set_initial_settings()
        self._create_title()
        self._create_buttons()
        self._create_user_input_text_area()
        self._create_download_folder_info()

        if not self._location_saved:
            self._create_save_download_location_checkbox()

        self._create_download_folder_layout()
        self._create_main_layout()

        self.buttons['Download'].clicked.connect(self._download)
        self.buttons['Reset'].clicked.connect(self._reset_text_area)
        self.buttons['Change Folder'].clicked.connect(self._select_download_folder)
        self.buttons['Open Download Folder'].clicked.connect(self._open_folder_location)

    def _open_folder_location(self):
        os.startfile(self._download_folder)

    def _select_download_folder(self):
        path = str(QFileDialog.getExistingDirectory(self))
        if path != '':
            path_short = get_short_path(str(path))
            if (self._save_download_location and self._save_download_location.isChecked()) or self._location_saved:
                if not os.path.exists('config_data.json'):
                    with open('config_data.json', 'w') as config_file:
                        data = {'download_location': str(path),
                                'download_location_short': path_short}
                        json.dump(data, config_file, indent=4)
                else:
                    with open('config_data.json', 'r+') as config_file:
                        data = json.load(config_file)
                        data['download_location'] = str(path)
                        data['download_location_short'] = path_short

                self._location_saved = True

            self._download_folder = path
            self._download_folder_to_show = path_short
            self._download_folder_location.setText(path_short)

    def _reset_text_area(self):
        self._download_error_found = False
        self._download_warning_found = False
        self._userInputArea.clear()
        self._userInputArea.setTextColor(QtGui.QColor(14, 234, 228, 250))
        self._set_button_status(['Download', 'Reset', 'Change Folder', 'Exit'], True)
        self._userInputArea.setReadOnly(False)

        if self._text_area_layout.itemAt(1):
            self._downloader_output.clear()
            downloader_output_area = self._text_area_layout.takeAt(1)
            downloader_output_area.widget().deleteLater()

    def _set_button_status(self, buttons_list, flag):
        for button in buttons_list:
            self.buttons[button].setEnabled(flag)

    def _download(self):
        self._user_input = list(filter(None, self._userInputArea.toPlainText().split('\n')))
        self._user_input = sorted(set(self._user_input), key=self._user_input.index)
        if len(self._user_input) > 0:
            self._userInputArea.setReadOnly(True)
            self._userInputArea.setText('\n\n'.join([i for i in self._user_input]))

            if self._save_download_location and self._save_download_location.isChecked():
                if not self._location_saved and not os.path.exists('config_data.json'):
                    with open('config_data.json', 'w') as config_file:
                        data = {'download_location': str(self._download_folder),
                                'download_location_short': str(self._download_folder_to_show)}
                        json.dump(data, config_file, indent=4)
                        self._location_saved = True

                if self._download_folder_layout.itemAt(4):
                    self._save_download_location = None
                    checkbox = self._download_folder_layout.takeAt(4)
                    checkbox.widget().deleteLater()

            if not self._text_area_layout.itemAt(1):
                self._downloader_output = QTextEdit(self)
                self._downloader_output.setMaximumSize(int(ctypes.windll.user32.GetSystemMetrics(0)), int(self.height() - self.height() / 1.45))
                self._downloader_output.setReadOnly(True)
                # noinspection SpellCheckingInspection
                self._downloader_output.setStyleSheet('color:#0eeae4; background-color:#43565c; border-radius: 7px')
                self._downloader_output.setAlignment(QtGui.Qt.AlignCenter)
                self._text_area_layout.addWidget(self._downloader_output)

            else:
                self._downloader_output.clear()
                self._downloader_output.setAlignment(QtGui.Qt.AlignCenter)

            logger = DownloadLogger(download_folder=self._download_folder)
            logger.message_signal.connect(self._show_progress)
            # noinspection SpellCheckingInspection
            self._ytdl_opts = CONFIG
            self._ytdl_opts['logger'] = logger
            # noinspection SpellCheckingInspection
            self._ytdl_opts['outtmpl'] = f'{self._download_folder}/%(title)s.%(ext)s'

            self.thread = PlaylistDownloader(self._user_input, self._ytdl_opts, other_options={'downloadFolder': self._download_folder})
            self._set_button_status(['Download', 'Reset', 'Change Folder', 'Exit'], False)
            self.thread.finished.connect(self._when_download_finished)

            self._link_index = 0
            self.thread.playlist_link_index.connect(self._get_link_index)
            self.thread.playlist_length.connect(self._show_playlist_length)
            self._user_input_colored = self._user_input
            self.thread.current_link_index.connect(self._color_when_download_started)
            self.thread.download_status.connect(self._color_download_status)

            self.thread.start()
            self._set_button_status(['Stop', 'Skip'], True)
            if self.thread.isRunning():
                self.buttons['Stop'].clicked.connect(self._terminate_thread)

    def _color_download_status(self, flag):
        if flag:
            current_link_status = '<span style=\"color:#00b515;\">' + self._current_link + '</span>'
            self._user_input_colored[self._current_index] = current_link_status
            self._userInputArea.setHtml('<br><br>'.join([i for i in self._user_input_colored]))
        else:
            current_link_status = '<span style=\"color:#ff0000;\">' + self._current_link + '</span>'
            self._user_input_colored[self._current_index] = current_link_status
            self._userInputArea.setHtml('<br><br>'.join([i for i in self._user_input_colored]))

    def _color_when_download_started(self, index):
        self._current_index = index
        self._current_link = self._user_input[index]
        current_link_status = '<span style=\"color:#fffb00;\">' + self._current_link + '</span>'
        self._user_input_colored[index] = current_link_status
        self._userInputArea.setHtml('<br><br>'.join([i for i in self._user_input_colored]))

    def _get_link_index(self, text):
        self._link_index = int(text)

    def _show_playlist_length(self, text):
        order = {1: '1st', 2: '2nd', 3: '3rd'}
        if self._link_index > 3:
            link_index = f'{self._link_index}th'
        else:
            link_index = order[self._link_index]

        self._downloader_output.append(f'Downloading playlist with {str(text)} songs (found at {link_index} link)\n')

    def _show_progress(self, text):
        if text.find('Warnings can be found') != -1:
            self._download_warning_found = text
        elif text.find('Errors can be found') != -1:
            self._download_error_found = text
        elif not self._download_interrupted:
            self._downloader_output.append(text)

    def _terminate_thread(self):
        self.thread.terminate_thread = True
        self._downloader_output.append('\n=== Download interrupted ===')
        self._set_button_status(['Stop', 'Skip'], False)
        self._download_interrupted = True
        self._file_to_delete = self.thread.current_song
        self._downloader_output.append('\n=== Closing the process, wait ===')

    def _when_download_finished(self):
        self._user_input_colored = None
        if self._download_interrupted and self.thread.isFinished():
            self._downloader_output.append('\n=== Removing temp files ===')
            with youtube_dl.YoutubeDL(self._ytdl_opts) as ydl:
                current_file = ydl.extract_info(self._file_to_delete, download=False)
                for file_object in os.listdir(self._download_folder):
                    if file_object.find(current_file['title']) != -1:
                        file_object_path = os.path.join(self._download_folder, file_object)
                        if os.path.isfile(file_object_path):
                            os.unlink(file_object_path)
            self._downloader_output.append('\n=== Temp files removed===')
            self._download_interrupted = False

        self._set_button_status(['Stop', 'Skip'], False)
        self._set_button_status(['Reset', 'Exit'], True)

        if self._download_warning_found:
            self._downloader_output.append(self._download_warning_found)
        if self._download_error_found:
            self._downloader_output.append(self._download_error_found)

        self._downloader_output.append('\n=== DONE ===')
