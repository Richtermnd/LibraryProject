from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QWidget


class PathPointer(QWidget):
    """
       Виджет для выбора файла и указания пути к нему
    """

    def __init__(self):
        super(PathPointer, self).__init__()
        self.__path = ''

        self.__btn = QPushButton('Выбрать')
        self.__btn.clicked.connect(self.__set_path)
        self.__field = QLineEdit(self.__path)
        self.__field.setReadOnly(True)

        self.__layout = QHBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__btn)
        self.__layout.addWidget(self.__field)

    def path(self):
        return self.__path

    def __set_path(self):
        self.__path = QFileDialog().getOpenFileName()[0]
        self.__field.setText(self.__path)