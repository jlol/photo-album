from PyQt5 import QtWidgets, QtCore


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.index = 0
        self.setStyleSheet(
            "background-color: rgb(222, 221, 218); \
            border-color: rgb(0, 0, 0); border: 2px; \
            border-style: solid;"
        )

    def set_index(self, index):
        self.index = index

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        return QtWidgets.QLabel.mousePressEvent(self, event)
