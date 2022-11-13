from collections import namedtuple
import datetime
import sqlite3
import sys

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QApplication
from PyQt5 import uic, QtCore


class ClientInfo(QWidget):
    def __init__(self, client_id):
        super().__init__()
        uic.loadUi(r'..\ui\ClientInfo.ui', self)
        self.con = sqlite3.connect(r'..\db\Library_db.db')
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

        self._initUI()
        self.update_main_table()

    def _initUI(self):
        self.comboBox_mode.currentTextChanged.connect(self.update_main_table)
        self.input_search.textChanged.connect(self.update_main_table)

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

    def search(self, table: list[list[str]]) -> list[list[str]]:
        text = self.input_search.text().lower()
        if len(text) >= 3:
            return list(filter(lambda x: text in x[1].lower(), table))
        return table

    def apply_filters(self, table):
        type = self.comboBox_mode.currentText()
        if type == 'Всё':
            return table
        elif type == 'Долги':
            return self.debts(table)
        return list(filter(lambda x: x[1] == type, table))

    def debts(self, table):
        # reverse table for iter in history order
        operations_stack = table

        op_state = {}
        # will use like value for op_state
        BookState = namedtuple('BookState', ['state', 'date', 'op'])

        # like constants
        type_return = 'Возврат'
        type_giving = 'Выдача'

        cur = self.con.cursor()
        while operations_stack:
            op = operations_stack.pop()
            book_title, op_type, date = op
            # will be used like key for op_state
            book_id = cur.execute(f"select id from book where title = '{book_title}'").fetchone()[0]

            if op_type == type_giving:
                op_state[book_id] = BookState(False, date, op)  # False means debt
            elif op_type == type_return:
                if book_id in op_state:
                    cur_date = datetime.datetime.strptime(date, '%d.%m.%Y')  # date from current op
                    prev_op = op_state[book_id]
                    prev_date = datetime.datetime.strptime(prev_op.date, '%d.%m.%Y')  # date prev op
                    if cur_date < prev_date or prev_date is None:  # this check is useless if writing in db correct
                        continue
                op_state[book_id] = BookState(True, None, op)  # True means that book returned
        return [elem[2] for elem in op_state.values() if not elem.state]

    def closeEvent(self, a0) -> None:
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientInfo(2)
    ex.show()
    sys.exit(app.exec())
