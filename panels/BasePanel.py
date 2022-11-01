import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QApplication, QLabel, QTableWidgetItem
from PyQt5 import uic
from forms.FilterForm import FilterForm


class BasePanel(QWidget):
    def __init__(self):
        # -- UI --
        super().__init__()
        uic.loadUi('ui/Panel.ui', self)

        # -- SQLite --
        self.con = sqlite3.connect('db/Library_db.db')
        self.cur = self.con.cursor()

        # -- vars --
        self.filter_list = []
        self.filter_form: FilterForm  # attempt at abstraction
        self.table: str
        self.headers: list[str]

        # -- Connect actions --
        self.input_search.textChanged.connect(self.update_main_table)
        self.button_add_filter.clicked.connect(self.filter_form.show)
        self.button_remove_filter.clicked.connect(self.remove_filter)

        # -- init --
        self.update_main_table()

    def update_main_table(self):
        """ Update main table with filters and other """
        res = self.cur.execute(self.create_request()).fetchall()
        res = self.search(res)

        self.table_main.setRowCount(len(res))
        self.table_main.setColumnCount(len(self.headers))
        self.table_main.setHorizontalHeaderLabels(self.headers)

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.table_main.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.table_main.resizeColumnsToContents()

    def create_request(self) -> str:
        """ Create request for update_main_table() func with filters and other"""
        req = f'SELECT {", ".join(self.headers)} FROM {self.table}'
        if self.filter_list:
            req += ' WHERE '
            req += ' AND '.join([f'{param} {criter}' for param, criter in self.filter_list])
        return req

    def add_filter(self, fltr: dict):
        """ Add filter from form to filter list """
        self.filter_list.append((fltr['param'], fltr['criter']))
        self.table_filter.setRowCount(self.table_filter.rowCount() + 1)
        self.update_filter_table()
        self.update_main_table()

    def update_filter_table(self):
        """ Fill table of filters """
        self.table_filter.setRowCount(0)
        for i, fltr in enumerate(self.filter_list):
            self.table_filter.setRowCount(self.table_filter.rowCount() + 1)
            for j, elem in enumerate(fltr):
                self.table_filter.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.table_filter.resizeColumnsToContents()

    def remove_filter(self):
        """ Remove filter """
        try:
            index = self.table_filter.currentItem().row()
        except:
            return
        self.filter_list.pop(index)
        self.update_main_table()
        self.update_filter_table()

    def search(self, table):
        text = self.input_search.text()
        if len(text) >= 3:
            return list(filter(lambda x: text in x, table))
        return table

    def write_to_history(self):
        pass

    def closeEvent(self, event):
        self.con.close()

    def get_form_result(self, res):
        """ Get result from form, override this"""
