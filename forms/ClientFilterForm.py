from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit

from custom_widgets.DigitLineEdit import DigitLineEdit
from forms._BaseForm import _BaseForm


class ClientFilterForm(_BaseForm):
    def __init__(self, *args, **kwargs):
        super(ClientFilterForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        label = QLabel('Параметр')
        label.setObjectName('param')
        cb = QComboBox()
        cb.addItems(['', 'id', 'name'])
        cb.currentIndexChanged.connect(self.choose_param)
        cb.required = True
        self.formLayout.addRow(label, cb)

    def choose_param(self):
        if self.formLayout.rowCount() == 2:
            self.formLayout.removeRow(1)

        params = ['', 'id', 'name']
        param = params[self.sender().currentIndex()]
        label = QLabel(self.sender().currentText())
        label.setObjectName(param)
        match param:
            case 'id':
                field = DigitLineEdit()
            case 'name':
                field = QLineEdit()
        field.required = True
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        # add_filter - BasePanel method
        self.holder.add_filter(res)
        self.close()
