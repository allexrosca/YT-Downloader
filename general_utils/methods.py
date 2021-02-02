import os
import unidecode


def check_and_create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def normalize_string(string):
    string = unidecode.unidecode(string.lower())
    return string.strip()


def cast_to_list(item):
    if isinstance(item, list):
        return item
    else:
        return [item]


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
