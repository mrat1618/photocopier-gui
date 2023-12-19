import os
from configparser import ConfigParser
from PySide6.QtWidgets import QMessageBox

def create_new_config():
    config = ConfigParser()
    config.add_section('Img Location')
    config.set('Img Location', 'custom_path', 'False')
    config.set('Img Location', 'folder_name', 'True')
    config.set('Img Location', 'folder_value', 'Selected Photos')

    config.add_section('Files')
    config.set('Files', 'overwrite_existing', 'False')
    config.set('Files', 'raw_types', ".NEF .ARW .CR2 .CR3 .DNG .CRW")
    config.set('Files', 'regex', r'\b(IMG_\d{4}|DSC\d{5}|P\d{7}|DSC_\d{4})\b')
    
    return config


def load_config(file='config.ini'):
    config = ConfigParser()
    if not os.path.exists(file):
        config = create_new_config()
        msg_box = QMessageBox()
        msg_box.setText(f"Error: The file {file} does not exist.")
        msg_box.exec()
        return config
    config.read(file)
    if not config.sections():
        config = create_new_config()
        msg_box = QMessageBox()
        msg_box.setText(f"Error: The file {file} is empty.")
        msg_box.exec()
    return config


def save_config(dict_config: dict, file='config.ini'):
    config = ConfigParser()
    
    for section, data in dict_config.items():
        config.add_section(section)
        for key, value in data.items():
            config.set(section, str(key), str(value))
    
    try:
        with open(file, 'w') as config_file:
            config.write(config_file)
        
    except Exception as e:
        msg_box = QMessageBox()
        msg_box.setText(f"An error occurred: {e}")
        msg_box.exec()


#read
'''
config = load_config('config.ini')

chk_img_custom_path = config.getboolean('Img Location', 'custom_path')
chk_img_folder_name = config.getboolean('Img Location', 'folder_name')
img_folder_value    = config['Img Location']['folder_value']

file_overwrite_existing = config.getboolean('Files', 'overwrite_existing')
file_raw_types = config['Files']['raw_types']
file_regex     = config['Files']['regex']

'''
