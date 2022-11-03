from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit
from forms.BaseForm import BaseForm


class BookFilterForm(BaseForm):
    def __init__(self, holder):
        super().__init__(holder)

    def _initUI(self):
        label = QLabel('Параметр')
        label.setObjectName('param')
        cb = QComboBox()
        cb.addItems(['id', 'author', 'year', 'status'])
        self.formLayout.addRow(label, cb)

        label = QLabel('Критерий')
        label.setObjectName('criter')
        self.formLayout.addRow(label, QLineEdit())

    def return_result(self, res):
        # add_filter - BasePanel method
        self.holder.add_filter(res)
