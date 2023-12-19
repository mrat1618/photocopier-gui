#!/usr/bin/env python3 

import os, re
from sys import exit
import pathlib, shutil, tqdm
from PySide6.QtWidgets import QMessageBox

def show_error(msg):
    msg_box = QMessageBox()
    msg_box.setText(f"An error occurred: {msg}")
    msg_box.exec()


def get_folder_path(path):
    path = pathlib.Path(path)
    if not path.exists():
        msg=f"No such file or directory: '{path}'"
        show_error(msg)
    elif path.is_dir():
        return path
    else:
        return path.parent


def search_files(types, location, filenames=None):
    loc = pathlib.Path(location)
    files = list()
    if loc.exists():
        for file_type in types:
            if filenames is None:
                # If filenames is not provided, return all files of the type
                files.extend([str(file.name) for file in loc.glob(f'**/*.{file_type}')])
            else:
                # If filenames is provided, return only those files
                for filename in filenames:
                    file = loc / f'{filename}.{file_type}'
                    if file.is_file():
                        files.append(str(file.name))
    return files


def find_image_names(text, pattern):
    matches = re.findall(pattern, text)
    return matches


def clean_img_names(img_list, pattern):
    cleaned_list = []
    for img in img_list:
        cleaned_name = find_image_names(img, pattern)
        cleaned_list.extend(cleaned_name)
    return cleaned_list


def get_raw_types(text):
    # Replace special characters with a space
    text = re.sub(r'\W', ' ', text)
    text_list = text.split()
    return set(text_list)


def cp(src:str, dest:str)->None:
    """copy files from src (source) to dest (destination)

    Args:
        src (str): path of the source file
        dest (str): path of the destination
    """
    src  = pathlib.Path(src)
    dest = pathlib.Path(dest)
    
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    except:
        msg = f"Can't copy {src.name}"
        show_error(msg)


def convert_to_path(loc):
    return pathlib.Path(loc)


def get_cwd():
    cwd = pathlib.Path.cwd()
    return cwd

