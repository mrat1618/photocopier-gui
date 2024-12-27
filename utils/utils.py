#!/usr/bin/env python3 

import os, re
from sys import exit
import utils.utils as utl
import utils.configs as cfg
import pathlib, shutil, tqdm
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QThread, Signal

class FileCopyWorker(QThread):
    progress_updated = Signal(int)  # Signal to update progress
    total_files_calculated = Signal(int)  # Signal to set the maximum value for the progress bar
    finished = Signal()  # Signal when the copy is finished

    def __init__(self, jpg_folder, raw_folder):
        super().__init__()
        self.jpg_folder = jpg_folder
        self.raw_folder = raw_folder
        

    def run(self):
        file_types = ['JPG', 'jpg']
        jpg_list   = utl.search_files(file_types, self.jpg_folder)
        
        config = cfg.load_config()
        # Filter out JPG image names
        regex_pattern = config['Files']['regex']
        cleaned_img_list = utl.clean_img_names(jpg_list, regex_pattern)
        
        # Identify RAW files to be copied
        raw_types = utl.get_raw_types(config['Files']['raw_types'])
        raw_files_list = utl.search_files(raw_types, self.raw_folder, cleaned_img_list)
        
        # Copy RAW files
        total_files = len(raw_files_list)
        src_fldr    = self.raw_folder
        
        if config.getboolean('Img Location', 'custom_path'):
            dest_fldr = config['Img Location']['folder_value']
        else:
            dest_fldr = f"{self.raw_folder}/{config['Img Location']['folder_value']}"
        
        src_fldr = utl.convert_to_path(src_fldr)
        dest_fldr= utl.convert_to_path(dest_fldr)
        
        self.total_files_calculated.emit(total_files)
        copied_files = 0
        
        # Copy files and track count
        for count, raw_file in enumerate(raw_files_list):
            utl.cp(src_fldr/raw_file, dest_fldr/raw_file)
            copied_files = count + 1
            # self.progress_bar.setValue(progress)
            self.progress_updated.emit(copied_files)
        
        self.finished.emit()


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

