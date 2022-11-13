from PyQt5.QtWidgets import QLabel, QLineEdit
from forms._BaseForm import _BaseForm


class GenreForm(_BaseForm):
    """ Форма для создания жанра """
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        label = QLabel('Имя')
        label.setObjectName('name')
        field = QLineEdit()
        field.required = True
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        cur = self.con.cursor()
        cur.execute(f"""INSERT into genre(name) VALUES(?)""", (res['name'],))
        self.close()

