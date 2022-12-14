import csv
from collections import namedtuple
import sqlite3

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from PyQt5 import uic, QtCore


class ClientInfo(QWidget):
    """ Детальная информация о клиенте """
    def __init__(self, client_id):
        super().__init__()
        uic.loadUi(r'ui\ClientInfo.ui', self)
        self.con = sqlite3.connect(r'db\Library_db.db')
        self.headers = ['Книга', 'Тип', 'Дата']
        self.base_req = f"""
                            SELECT book.title,
                                   operation_type.type,
                                   operation.date
                            FROM operation
                                   JOIN
                                   book,
                                   operation_type ON operation.client = {client_id} AND 
                                   book.id = operation.book AND
                                   operation_type.id = operation.type order by operation.id desc;
                         """
        self.client_name, = self.con.cursor().execute(f'SELECT name FROM client WHERE id = {client_id}').fetchone()
        self._initUI()
        self.update_main_table()

    def _initUI(self):
        self.comboBox_mode.currentTextChanged.connect(self.update_main_table)
        self.input_search.textChanged.connect(self.update_main_table)
        self.export_button.clicked.connect(self.export)

    def update_main_table(self) -> None:
        """ Update main table"""
        cur = self.con.cursor()
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

    def export(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Экспортировать как',
                                                  rf'C:/Users/{self.comboBox_mode.currentText()}_{self.client_name}',
                                                  'CSV files (*.csv)')
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [self.table_main.horizontalHeaderItem(i).text()
                 for i in range(self.table_main.columnCount())])

            for i in range(self.table_main.rowCount()):
                row = []
                for j in range(self.table_main.columnCount()):
                    row.append(self.table_main.item(i, j).text())
                writer.writerow(row)

    def search(self, table: list[list[str]]) -> list[list[str]]:
        text = self.input_search.text().lower()
        if len(text) >= 3:
            return list(filter(lambda x: text in x[0].lower(), table))
        return table

    def apply_filters(self, table):
        type = self.comboBox_mode.currentText()
        if type == 'Всё':
            return table
        elif type == 'Долги':
            return self.debts(table)
        return list(filter(lambda x: x[1] == type, table))

    def debts(self, table):
        """ Долги клиента """
        operations_stack = table[:]

        op_state = {}
        # Будет использовавться как значение для op_state
        BookState = namedtuple('BookState', ['state', 'op'])

        cur = self.con.cursor()
        # Методом стэка
        while operations_stack:
            op = operations_stack.pop()
            book_title, op_type, _ = op
            # Будет использовавться как ключ для op_state
            book_id, = cur.execute(f"select id from book where title = '{book_title}'").fetchone()

            if op_type == 'Выдача':
                op_state[book_id] = BookState(True, op)  # True означае, что должен
            elif op_type == 'Возврат':
                op_state[book_id] = BookState(False, op)  # False означает, что книгу уже вернули
        # Возвращаем список долгов
        return [elem.op for elem in op_state.values() if elem.state]

    def closeEvent(self, a0) -> None:
        self.con.close()
