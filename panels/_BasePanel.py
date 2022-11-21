import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QApplication
from PyQt5 import uic, QtCore


class _BasePanel(QWidget):
    """ Базовая панель """
    def __init__(self, filter_form, add_item_form, about_widget, table, headers, base_req, filter_params):
        # -- UI --
        super().__init__()
        uic.loadUi(r'ui\Panel.ui', self)

        # -- db --
        self.con = sqlite3.connect(r'db\Library_db.db')

        # -- vars --
        self.filter_list = []
        self.filter_form = filter_form  # Форма для фильтра
        self.add_item_form = add_item_form  # Форма для добавления
        self.about_widget = about_widget  # Форма
        self.table = table  # Имя таблицы (используется в add_item)
        self.headers = headers  # Заголовки для таблицы
        self.base_req = base_req  # Базовый запрос для получения данных из дб
        self.filter_params = filter_params  # Используется в apply_filters

        self._initUI()

    def _initUI(self) -> None:
        """ Привзяка кнопок """
        # -- Connect actions --
        self.input_search.textChanged.connect(self.update_main_table)
        self.button_add_filter.clicked.connect(self.show_filter_form)
        self.button_remove_filter.clicked.connect(self.remove_filter)
        self.button_about.clicked.connect(self.show_about_widget)

        # -- loading and update other widgets --
        self.update_main_table()

    # Методы таблицы и фильтров
    ############################
    def update_main_table(self) -> None:
        """ Обновляет таблицу """
        cur = self.con.cursor()
        res = cur.execute(self.base_req).fetchall()
        # Поиск по строке
        res = self.search(res)
        # Применение фильтров
        res = self.apply_filters(res)

        # Загрузка таблицы
        self.table_main.setRowCount(len(res))
        self.table_main.setColumnCount(len(self.headers))
        self.table_main.setHorizontalHeaderLabels(self.headers)

        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                if elem is None:
                    item = QTableWidgetItem('Неизвестно')
                else:
                    item = QTableWidgetItem(str(elem))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_main.setItem(
                    i, j, item)
        self.table_main.resizeColumnsToContents()

    def update_filter_table(self) -> None:
        """ Обновление таблицы фильтров """
        cur = self.con.cursor()
        self.table_filter.setRowCount(0)
        for i, (key, value) in enumerate(self.filter_list):
            self.table_filter.setRowCount(self.table_filter.rowCount() + 1)
            param = self.headers[key - 1]
            item = QTableWidgetItem(str(param))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_filter.setItem(i, 0, item)
            match param:
                case 'Состояние':
                    value = 'Доступна' if value == 2 else 'Недоступна'
                case 'Автор':
                    value, = cur.execute(f"""SELECT name from author where id = {value}""").fetchone()
                case 'Жанр':
                    value, = cur.execute(f"""SELECT name from genre where id = {value}""").fetchone()
            item = QTableWidgetItem(str(value))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_filter.setItem(i, 1, item)

        self.table_filter.resizeColumnsToContents()

    def apply_filters(self, res):
        """ Применение фильтров """
        for col, value in self.filter_list:
            value = self.filter_params[col - 1](value)
            res = [elem for elem in res if elem[col - 1] == value]
        return res

    def add_filter(self, fltr: dict) -> None:
        """ Добавление фильтра в filter_list и обновление таблиц для его применения """
        self.filter_list.append(tuple(fltr.values()))
        self.update_filter_table()
        self.update_main_table()

    def remove_filter(self) -> None:
        """ Удаляет фильтр """
        try:
            index = self.table_filter.currentItem().row()
        except AttributeError:
            return
        self.filter_list.pop(index)
        self.update_filter_table()
        self.update_main_table()

    def search(self, table):
        """ Поиск по строке ввода """
        text = self.input_search.text().lower()
        if len(text) >= 3:
            return [elem for elem in table if text in elem[1].lower()]
        return table

    def show_about_widget(self):
        """ Показывает виджет с детальной информацией """
        try:
            row = self.table_main.currentItem().row()
            index = self.table_main.item(row, 0).text()
            title = self.table_main.item(row, 1).text()
        except AttributeError:
            return

        # if preview is not attr it closing immediately
        self.preview = self.about_widget(index)
        self.preview.show()
        self.write_to_history(title)

    def show_filter_form(self):
        self.form = self.filter_form(self)
        self.form.show()

    def write_to_history(self, title):
        """ Записывает в историю """
        self.table_history.setRowCount(self.table_history.rowCount() + 1)
        item = QTableWidgetItem(str(title))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.table_history.setItem(self.table_history.rowCount() - 1, 0, item)
    ############################

    # Методы для бд
    ###########################
    def show_add_item_form(self):
        self.form = self.add_item_form(self)
        self.form.show()

    def add_item(self, data: dict):
        """ Записывает в бд """
        req = f"""INSERT INTO {self.table}({', '.join(data.keys())}) """ \
              f"""VALUES({', '.join(['?' for _ in range(len(data))])});"""
        cur = self.con.cursor()
        cur.execute(req, tuple(data.values()))
        self.con.commit()
        self.update_main_table()
    ###########################

    def closeEvent(self, a0) -> None:
        self.con.commit()
        self.con.close()
