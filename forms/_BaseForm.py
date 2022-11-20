import sqlite3

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QFormLayout, QDateEdit
from PyQt5 import uic

from custom_widgets.PathPointer import PathPointer
from LibraryError import LibraryError


class _BaseForm(QWidget):
    """ Базовая форма для заполнения какой-либо информации """
    def __init__(self, holder):
        super().__init__()
        uic.loadUi(r'ui\Form.ui', self)
        self.con = sqlite3.connect(r'db\Library_db.db')
        # holder - объект, которому будет возвращаться результат формы
        self.holder = holder
        self.button_add.clicked.connect(self.get_form_result)
        self.button_cancel.clicked.connect(self.close)
        self._initUI()

    def _initUI(self):
        """ Инициализация ui, обязателен к перегрузке  """

    def get_form_result(self):
        """ Считывает информацию с формы и отсылает её """
        res = {}

        # Read data from QFormLayout
        for row in range(self.formLayout.rowCount()):
            label = self.formLayout.itemAt(row, QFormLayout.LabelRole).widget().objectName()
            field = self.formLayout.itemAt(row, QFormLayout.FieldRole).widget()

            try:
                if isinstance(field, PathPointer):
                    if field.path() == '':
                        continue
                    try:
                        with open(field.path(), mode='rb') as f:
                            data = f.read()
                    except FileNotFoundError:
                        raise LibraryError.FormError(label)
                elif isinstance(field, QLineEdit):
                    data = field.text()
                    if data == '':
                        if field.required:
                            raise LibraryError.FormError(label)
                        else:
                            continue
                elif isinstance(field, QComboBox):
                    data = field.currentIndex()
                    if data == 0 and label not in 'status':
                        if field.required:
                            raise LibraryError.FormError(label)
                        else:
                            continue
                elif isinstance(field, QDateEdit):
                    data = field.date().toPyDate().strftime('%d.%m.%Y')  # some value always present
                else:
                    raise LibraryError.FormError(label)
            except LibraryError as e:
                self.label_exc.setText(f'Ошибка в поле: {e}')
            except Exception:
                self.label_exc.setText(f'Непредвиденная ошибка')

            res[label] = data
        self.return_result(res)

    def return_result(self, res):
        """
            Метод, который возвращает результат holder'у.
            Обязателен к перегрузке с необходимыми проверками и методом holder'а
        """

    def closeEvent(self, a0) -> None:
        self.con.commit()
        self.con.close()

