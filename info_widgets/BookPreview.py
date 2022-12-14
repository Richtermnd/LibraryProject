import sqlite3

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class BookPreview(QWidget):
    """ Детальная информация о книге """
    def __init__(self, book_id):
        super().__init__()
        uic.loadUi(r'ui\BookPreview.ui', self)

        # just grab a book from db
        con = sqlite3.connect(r'db\Library_db.db')
        self.book = con.cursor().execute(f'select * from book where id = {book_id}').fetchone()
        con.close()
        self._initUI()

    def _initUI(self):
        # set title
        self.setWindowTitle(str(self.book[1]))

        # load title
        self.lineEdit_title.setText(str(self.book[1]))

        # load info
        self.textEdit_info.setText(str(self.book[5]))

        # load cover
        pix = QPixmap()
        if pix.loadFromData(self.book[6]):
            self.label_cover.setPixmap(pix)

