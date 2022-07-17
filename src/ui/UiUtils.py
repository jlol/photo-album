from PyQt5.QtWidgets import QMessageBox, QFileDialog


INPUT_IMAGE_FILE_FILTER = 'Image files (*.jpg *.jpeg *.png)'
OUTPUT_IMAGE_FILE_FILTER = 'Image files (*.jpg *.jpeg *.png)'
PROJECT_FILE_FILTER = ''


def get_warning_window(message: str) -> QMessageBox:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Warning")
    return msg


def show_modal_window(parent, message: str) -> bool:
    result = QMessageBox.question(parent, '', message, QMessageBox.Yes | QMessageBox.No)
    return result == QMessageBox.Yes

