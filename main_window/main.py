from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from panels.BookPanel import BookPanel
from panels.OperationsPanel import OperationsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'ui\MainWindow.ui', self)
        self._initUI()

    def _initUI(self):
        self.open_books_panel.triggered.connect(lambda: self.setCentralWidget(BookPanel()))
        self.open_operations_panel.triggered.connect(lambda: self.setCentralWidget(OperationsPanel()))
        self.setCentralWidget(BookPanel())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
