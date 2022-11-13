import sqlite3
import sys

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QApplication
from PyQt5 import uic, QtCore


class OperationInfo(QWidget):
    def __init__(self, operation_id):
        super().__init__()
        uic.loadUi(r'..\ui\ClientInfo.ui', self)
        self.headers = ['id', 'Книга', 'Тип', 'Дата']
        self.base_req = f"""
                            SELECT operation.id,
                                   book.title,
                                   client.name,
                                   operation_type.type
                              FROM operation
                                   INNER JOIN
                                   book,
                                   client,
                                   operation_type ON operation.id = {operation_id} AND 
                                                     book.id = operation.book AND 
                                                     client.id = operation.client AND 
                                                     operation_type.id = operation.type;
                         """

        self._initUI()
        self.update_main_table()

    def _initUI(self):
        self.comboBox_mode.currentTextChanged.connect(self.update_main_table)
        self.input_search.textChanged.connect(self.update_main_table)

    def con(self):
        return sqlite3.connect(r'..\db\Library_db.db')

    def update_main_table(self) -> None:
        """ Update main table"""
        con = self.con()
        cur = con.cursor()
        res = cur.execute(self.base_req).fetchall()
        res = self.search(res)
        res = self.apply_filters(res)

        self.table_main.setRowCount(len(res))
        self.table_main.setColumnCount(len(self.headers))
        self.table_main.setHorizontalHeaderLabels(self.headers)

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_main.setItem(
                    i, j, item)
        self.table_main.resizeColumnsToContents()
        con.close()

    def search(self, table: list[list[str]]) -> list[list[str]]:
        text = self.input_search.text().lower()
        if len(text) >= 3:
            return list(filter(lambda x: text in x[1].lower(), table))
        return table

    def apply_filters(self, table):
        type = self.comboBox_mode.currentText()
        if type == 'Всё':
            return table
        return list(filter(lambda x: x[2] == type, table))

