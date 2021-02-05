import os
import unidecode


def check_and_create_folder(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)


def remove_files_from_directory(path):
    if os.path.isdir(path):
        for file_object in os.listdir(path):
            file_object_path = os.path.join(path, file_object)
            if os.path.isfile(file_object_path):
                os.remove(file_object_path)


def normalize_string(string):
    string = unidecode.unidecode(string.lower())
    return string.strip()


def get_short_path(path):
    if len(path) > 50:
        short_path = ''
        for i in path.split('/'):
            if len(short_path + i + '\\') > 40:
                break
            short_path = short_path + i + '\\'

        path = short_path + '...\\' + path.split('/')[-1]
        return path
    else:
        return path.replace('/', '\\')


def generate_error_folder_path(download_path):
    return os.path.join(download_path, 'errors')