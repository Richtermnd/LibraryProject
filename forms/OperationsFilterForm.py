import sqlite3

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QApplication, QDateEdit

from custom_widgets.DigitLineEdit import DigitLineEdit
from forms._BaseForm import _BaseForm


class OperationsFilterForm(_BaseForm):
    def __init__(self, holder):
        super(OperationsFilterForm, self).__init__(holder)

    def _initUI(self):
        label = QLabel('Параметр')
        label.setObjectName('param')
        field = QComboBox()
        field.addItems(['', 'id', 'Книга', 'Клиент', 'Тип', 'Дата'])
        field.currentTextChanged.connect(self.choose_param)
        self.formLayout.addRow(label, field)

    def choose_param(self):
        if self.formLayout.rowCount() == 2:
            self.formLayout.removeRow(1)
        cur = self.con.cursor()

        params = ['', 'id', 'book', 'client', 'type', 'date']
        param = params[self.sender().currentIndex()]
        label = QLabel(self.sender().currentText())
        label.setObjectName(param)
        match param:
            case 'id':
                field = DigitLineEdit()
            case 'book':
                field = QLineEdit()
            case 'client':
                field = QComboBox()
                field.addItems([''] + [str(elem[0]) for elem in cur.execute(f"""select name from client""").fetchall()])
            case 'type':
                field = QComboBox()
                field.addItems([''] + [str(elem[0])
                                       for elem in cur.execute(f"""select type from operation_type""").fetchall()])
            case 'date':
                field = QDateEdit()
                field.setDate(QDate().currentDate())

        field.required = True
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        # add_filter - BasePanel method
        self.holder.add_filter(res)
        self.close()
