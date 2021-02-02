import os

DOWNLOAD_FOLDER = 'D:\\youtubeDownloader\\'
ERRORS_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'errors')

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
