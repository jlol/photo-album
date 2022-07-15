from PyQt5.QtWidgets import QMessageBox


def get_warning_window(message: str) -> QMessageBox:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    #msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Warning")
    #msg.setDetailedText("The details are as follows:")
    return msg