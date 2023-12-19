from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QProgressBar, QCheckBox, QTextEdit, QMainWindow, QRadioButton, QPlainTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import utils.configs as cfg
import utils.utils as utl

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a QLabel
        self.label = QLabel("Configurations")
        layout.addWidget(self.label)

        # Create a QHBoxLayout for the radio buttons
        radio_button_layout = QHBoxLayout()
        # Create two QRadioButtons
        self.rdbt_cust_fldr = QRadioButton("Use a custom folder")
        self.rdbt_fldr_nm   = QRadioButton("Save inside the raw folder")
        radio_button_layout.addWidget(self.rdbt_cust_fldr)
        radio_button_layout.addWidget(self.rdbt_fldr_nm)
        # Add the QHBoxLayout to the QVBoxLayout
        layout.addLayout(radio_button_layout)

        # Create a QPlainTextEdit
        self.txt_folder = QPlainTextEdit()
        layout.addWidget(self.txt_folder)
        
        #xx
        self.chk_overwrt = QCheckBox("Overwrite existing JPGs")
        layout.addWidget(self.chk_overwrt)
        
        self.label2 = QLabel("RAW file types to copy")
        layout.addWidget(self.label2)
        # Create a QPlainTextEdit
        self.txt_raw_types = QPlainTextEdit()
        layout.addWidget(self.txt_raw_types)
        
        self.label3 = QLabel("Regex to filter Raw/JPG file name")
        layout.addWidget(self.label3)
        # Create a QPlainTextEdit
        self.txt_regex = QPlainTextEdit()
        layout.addWidget(self.txt_regex)

        # Create a QPushButton
        bt_save = QPushButton("Save and Close")
        layout.addWidget(bt_save)
        bt_save.clicked.connect(self.save_configs)

        # Create a QWidget and set it as the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.resize(300, 400)
        
        # Load initial values
        self.load_configs()

    def browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_location.setText(folder)
            
    def load_configs(self):
        config = cfg.load_config()
        
        self.rdbt_cust_fldr.setChecked(config.getboolean('Img Location', 'custom_path'))
        self.rdbt_fldr_nm.setChecked(config.getboolean('Img Location', 'folder_name'))
        self.txt_folder.setPlainText(config.get('Img Location', 'folder_value'))
        self.chk_overwrt.setChecked(config.getboolean('Files', 'overwrite_existing'))
        self.txt_raw_types.setPlainText(config.get('Files', 'raw_types'))
        self.txt_regex.setPlainText(config.get('Files', 'regex'))
    
    def save_configs(self):
        dict_configs = {}
        dict_configs['Img Location'] = {
            'custom_path': self.rdbt_cust_fldr.isChecked(),
            'folder_name': self.rdbt_fldr_nm.isChecked(),
            'folder_value': self.txt_folder.toPlainText()
        }
        dict_configs['Files'] = {
            'overwrite_existing': self.chk_overwrt.isChecked(),
            'raw_types': self.txt_raw_types.toPlainText(),
            'regex': self.txt_regex.toPlainText()
        }
        
        cfg.save_config(dict_configs)
        
        # Close the window after saving
        self.close()


class DropArea(QLabel):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa")
        self.folder_path = ''
        self.setText("Drag and drop folder/file here or click to open a folder")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            self.folder_path=utl.get_folder_path(path)
            self.setText(self.text() + "\n\nFolder Added ✅")

    def mousePressEvent(self, event):
        folder_path = QFileDialog.getExistingDirectory()
        self.folder_path=utl.get_folder_path(folder_path)
        self.setText(self.text() + "\n\nFolder Added ✅")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pCopy GUI")

        # Create a central widget for the main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set the layout for the central widget
        self.central_widget.setLayout(QVBoxLayout())
        self.hbox_layout = QHBoxLayout()
        self.central_widget.layout().addLayout(self.hbox_layout)
        
        # Create and name the drop areas
        self.drop1 = DropArea()
        self.drop1.setObjectName('drop1')
        self.hbox_layout.addWidget(self.drop1)
        self.d1_text = "🌇 JPG Folder\n\nDrag and drop folder/file here or click to open a folder"
        self.drop1.setText(self.d1_text)
        
        self.drop2 = DropArea()
        self.drop2.setObjectName('drop2')
        self.hbox_layout.addWidget(self.drop2)
        self.d2_text = "📸 RAW Folder\n\nDrag and drop folder/file here or click to open a folder"
        self.drop2.setText(self.d2_text)
        
        self.progress_bar = QProgressBar()
        self.central_widget.layout().addWidget(self.progress_bar)
        self.progress_bar.setValue(0)
        
        self.button_layout = QHBoxLayout()
        self.central_widget.layout().addLayout(self.button_layout)
        self.config_button = QPushButton("Config")
        self.button_layout.addWidget(self.config_button)
        self.config_button.clicked.connect(self.open_config_window)
        self.reset_button = QPushButton("Reset")
        self.button_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset)
        self.run_button = QPushButton("Run")
        self.button_layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run)
        
    def reset(self):
        self.drop1.setText(self.d1_text)
        self.drop2.setText(self.d2_text)
        self.drop1.folder_path = ''
        self.drop2.folder_path = ''
        self.progress_bar.setValue(0)
    
    def run(self):
        jpg_folder = self.drop1.folder_path
        raw_folder = self.drop2.folder_path
        
        file_types = ['JPG', 'jpg']
        jpg_list   = utl.search_files(file_types, jpg_folder)
        
        config = cfg.load_config()
        # Filter out JPG image names
        regex_pattern = config['Files']['regex']
        cleaned_img_list = utl.clean_img_names(jpg_list, regex_pattern)
        
        # Identify RAW files to be copied
        raw_types = utl.get_raw_types(config['Files']['raw_types'])
        raw_files_list = utl.search_files(raw_types, raw_folder, cleaned_img_list)
        
        # Copy RAW files
        num_files = len(raw_files_list)
        src_fldr  = raw_folder
        if config.getboolean('Img Location', 'custom_path'):
            dest_fldr = config['Img Location']['folder_value']
        else:
            dest_fldr = f"{raw_folder}/{config['Img Location']['folder_value']}"
        src_fldr = utl.convert_to_path(src_fldr)
        dest_fldr= utl.convert_to_path(dest_fldr)
        
        for count, raw_file in enumerate(raw_files_list):
            utl.cp(src_fldr/raw_file, dest_fldr/raw_file)
            progress = 100*((1+count)/num_files)
            self.progress_bar.setValue(progress)
    
    def open_config_window(self):
        self.config_window = ConfigWindow()
        self.config_window.show()
        

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.setWindowIcon(QIcon('./imgs/icon.png'))
    window.resize(400, 300)
    window.show()
    app.exec()
