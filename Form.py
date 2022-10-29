import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QApplication, QLabel, QFormLayout
from PyQt5 import uic


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/Form.ui', self)
        self.button_add.clicked.connect(self.return_form)
        self._initUI()

    def _initUI(self):
        """ Override this """

    def return_form(self) -> dict:
        """ Return dict from form items"""
        res = {}
        for row in range(self.formLayout.rowCount()):
            field = self.formLayout.itemAt(row, QFormLayout.LabelRole).widget().objectName()
            data = self.formLayout.itemAt(row, QFormLayout.FieldRole).widget()

            if isinstance(data, QLineEdit):
                data = data.text()
            elif isinstance(data, QComboBox):
                data = data.currentText()
            else:
                # I will make other exceptions next time xd
                raise Exception
            # check for data is not empty
            if not data:
                # I promise to make exceptions
                raise Exception
            res[field] = data
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())
