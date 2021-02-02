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
