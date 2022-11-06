import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic, QtCore


class BasePanel(QWidget):
    def __init__(self, filter_form, about_widget, table, headers, base_req):
        # -- UI --
        super().__init__()
        uic.loadUi(r'..\ui\Panel.ui', self)

        # -- SQLite --
        self.con = sqlite3.connect(r'..\\db\Library_db.db')
        self.cur = self.con.cursor()

        # -- vars --
        self.filter_list = []
        self.filter_form = filter_form
        self.about_widget = about_widget
        self.table = table
        self.headers = headers
        self.base_req = base_req

    def _initUI(self) -> None:
        """ Need to call necessary """
        # -- Connect actions --
        self.input_search.textChanged.connect(self.update_main_table)
        self.button_add_filter.clicked.connect(self.filter_form.show)
        self.button_remove_filter.clicked.connect(self.remove_filter)
        self.button_about.clicked.connect(self.show_about_widget)

        # -- loading and update other widgets --
        self.update_main_table()

    def update_main_table(self) -> None:
        """ Update main table with filters and other """
        res = self.cur.execute(self.base_req)
        res = res.fetchall()
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

    def update_filter_table(self) -> None:
        """ Fill table of filters """
        self.table_filter.setRowCount(0)
        for i, fltr in enumerate(self.filter_list):
            self.table_filter.setRowCount(self.table_filter.rowCount() + 1)
            param = self.headers[fltr[0]]
            item = QTableWidgetItem(str(param))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_filter.setItem(i, 0, item)

            criter = str(fltr[1])
            item = QTableWidgetItem(str(criter))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_filter.setItem(i, 1, item)

        self.table_filter.resizeColumnsToContents()

    def apply_filters(self, res):
        for param, criter in self.filter_list:
            res = [elem for elem in res if eval(str(elem[param]) + criter)]
        return res

    def add_filter(self, fltr: dict) -> None:
        """ Add filter from form to filter list """
        self.filter_list.append((fltr['param'], fltr['criter']))
        self.table_filter.setRowCount(self.table_filter.rowCount() + 1)
        self.update_filter_table()
        self.update_main_table()

    def remove_filter(self) -> None:
        """ Remove filter """
        try:
            index = self.table_filter.currentItem().row()
        except AttributeError as e:
            return
        self.filter_list.pop(index)
        self.update_filter_table()
        self.update_main_table()

    def search(self, table: list[list[str]]) -> list[list[str]]:
        text = self.input_search.text().lower()
        if len(text) >= 3:
            return list(filter(lambda x: text in x[1].lower(), table))
        return table

    def show_about_widget(self):
        """ Show widget with additional info. Override this """
        self.about_widget.show()

    def write_to_history(self, title) -> None:
        self.table_history.setRowCount(self.table_history.rowCount() + 1)
        item = QTableWidgetItem(str(title))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table_history.setItem(self.table_history.rowCount() - 1, 0, item)

    def closeEvent(self, event) -> None:
        self.con.close()
