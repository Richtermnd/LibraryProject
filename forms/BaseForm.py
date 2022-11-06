from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QFormLayout, QDateEdit
from PyQt5 import uic


class BaseForm(QWidget):
    def __init__(self, holder):
        super().__init__()
        uic.loadUi(r'..\ui\Form.ui', self)
        self.holder = holder
        self.button_add.clicked.connect(self.get_form_result)
        self._initUI()

    def _initUI(self):
        """ Override this. Only QLineEdit or QComboBox like field"""

    def get_form_result(self):
        """ Return dict from form items"""
        res = {}

        # Read data from QFormLayout
        for row in range(self.formLayout.rowCount()):
            label = self.formLayout.itemAt(row, QFormLayout.LabelRole).widget().objectName()
            field = self.formLayout.itemAt(row, QFormLayout.FieldRole).widget()

            if isinstance(field, QLineEdit):
                field = field.text()
            elif isinstance(field, QComboBox):
                field = field.currentIndex()
            elif isinstance(field, QDateEdit):
                field = field.date().toPyDate().strftime('%Y.%m.%d')
            else:
                # I will make other exceptions next time xd
                raise Exception

            # check for data is not empty
            if field is None:
                # I promise to make exceptions
                raise Exception
            res[label] = field

        self.return_result(res)
        self.close()

    def return_result(self, res):
        """ Override with necessary holder method """

