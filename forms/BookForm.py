from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit

from forms._BaseForm import _BaseForm
from custom_widgets.PathPointer import PathPointer


class BookForm(_BaseForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        cur = self.con.cursor()

        label = QLabel('Название')
        label.setObjectName('title')
        field = QLineEdit()
        field.required = True
        self.formLayout.addRow(label, field)

        label = QLabel('Автор')
        label.setObjectName('author')
        field = QComboBox()
        field.required = False
        field.addItems([''] + [elem[0] for elem in cur.execute('SELECT name FROM author').fetchall()])
        self.formLayout.addRow(label, field)

        label = QLabel('Жанр')
        label.setObjectName('genre')
        field = QComboBox()
        field.required = False
        field.addItems([''] + [elem[0] for elem in cur.execute('SELECT name FROM genre').fetchall()])
        self.formLayout.addRow(label, field)

        label = QLabel('Год')
        label.setObjectName('year')
        field = QLineEdit()
        field.required = False
        self.formLayout.addRow(label, field)

        label = QLabel('Информация')
        label.setObjectName('info')
        field = QLineEdit()
        field.required = False
        self.formLayout.addRow(label, field)

        label = QLabel('Обложка')
        label.setObjectName('cover')
        field = PathPointer()
        field.required = False
        self.formLayout.addRow(label, field)

        label = QLabel('Состояние')
        label.setObjectName('status')
        field = QComboBox()
        field.required = True
        field.addItems(['Недоступна', 'Доступна'])
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        self.holder.add_item(res)
        self.close()

