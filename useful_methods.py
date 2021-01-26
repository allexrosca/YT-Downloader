import os

def check_and_create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
