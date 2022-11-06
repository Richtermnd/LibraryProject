from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QApplication, QDateEdit
from forms.BaseForm import BaseForm


class OperationsFilterForm(BaseForm):
    def __init__(self, holder):
        super(OperationsFilterForm, self).__init__(holder)

    def _initUI(self):
        label = QLabel('Параметр')
        label.setObjectName('param')

        field = QComboBox()
        field.addItems(['client', 'type', 'date'])
        field.currentTextChanged.connect(self.choose_param)

        self.formLayout.addRow(label, field)

        label = QLabel('Критерий')
        label.setObjectName('criter')

        self.formLayout.addRow(label, QLineEdit())

    def choose_param(self):
        if self.formLayout.rowCount() == 2:
            self.formLayout.removeRow(1)
        label = QLabel('Критерий')
        label.setObjectName('criter')
        param = self.sender().currentText()
        match param:
            case 'client':
                field = QLineEdit()
            case 'type':
                field = QComboBox()
                field.addItems(['Выдача', 'Возврат'])
            case 'date':
                field = QDateEdit()
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        # add_filter - BasePanel method
        self.holder.add_filter()
