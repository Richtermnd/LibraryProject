from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit
from forms._BaseForm import _BaseForm
from custom_widgets.DigitLineEdit import DigitLineEdit


class BookFilterForm(_BaseForm):
    """ Форма для создания фильтра для панели книг """
    def __init__(self, *args, **kwargs):
        super(BookFilterForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        label = QLabel('Параметр')
        label.setObjectName('param')
        cb = QComboBox()
        cb.addItems(['', 'id', 'Название', 'Автор', 'Жанр', 'Год', 'Статус'])
        cb.currentIndexChanged.connect(self.choose_param)
        cb.required = True
        self.formLayout.addRow(label, cb)

    def choose_param(self):
        """ Выбор необходимого параметра """

        # Не допускает наличия лишних строк
        if self.formLayout.rowCount() == 2:
            self.formLayout.removeRow(1)
        cur = self.con.cursor()

        params = ['', 'id', 'title', 'author', 'genre', 'year', 'status']
        param = params[self.sender().currentIndex()]
        label = QLabel(self.sender().currentText())
        label.setObjectName(param)

        match param:
            case 'id':
                field = DigitLineEdit()
            case 'title':
                field = QLineEdit()
            case 'author':
                field = QComboBox()
                field.addItems([''] + [str(elem[0]) for elem in cur.execute(f"""select name from author""").fetchall()])
            case 'year':
                field = DigitLineEdit()
            case 'genre':
                field = QComboBox()
                field.addItems([''] + [str(elem[0]) for elem in cur.execute(f"""select name from genre""").fetchall()])
            case 'status':
                field = QComboBox()
                field.addItems([''] + ['Недоступна', 'Доступна'])
        field.required = True
        self.formLayout.addRow(label, field)

    def return_result(self, res):
        self.close()
        # add_filter - BasePanel method
        self.holder.add_filter(res)

