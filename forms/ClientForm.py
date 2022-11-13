from PyQt5.QtWidgets import QLabel, QLineEdit
from forms._BaseForm import _BaseForm


class ClientForm(_BaseForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        label = QLabel('Имя')
        label.setObjectName('name')
        field = QLineEdit()
        field.required = True
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        self.holder.add_item(res)
        self.close()

