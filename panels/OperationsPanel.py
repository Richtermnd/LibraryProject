from PyQt5.QtWidgets import QApplication

from panels.BasePanel import BasePanel
from forms.OperationsFilterForm import OperationsFilterForm


class OperationsPanel(BasePanel):
    def __init__(self):
        filter_form = OperationsFilterForm(self)
        about_widget = None
        table = 'operation'
        headers = ['id', 'Книга', 'Клиент', 'Тип', 'Дата']
        base_req = 'SELECT operation.id, book.title, client.name, operation_type.type, operation.date FROM operation ' \
                   'INNER JOIN book, client, operation_type ON operation.book = book.id ' \
                   'AND operation.client = client.id ' \
                   'AND operation.type = operation_type.id'
        super(OperationsPanel, self).__init__(filter_form, about_widget, table, headers, base_req)
        self._initUI()

    def show_about_widget(self):
        print('ПЕРЕДЕЛАЙ')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = OperationsPanel()
    ex.show()
    sys.exit(app.exec())

