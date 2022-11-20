from PyQt5.QtWidgets import QLineEdit


class DigitLineEdit(QLineEdit):
    """ QLineEdit, в который можно вводить только числа"""
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.__is_digit)

    def __is_digit(self):
        if not super().text():
            return
        if not super().text()[-1].isdigit():
            self.setText(super().text()[:-1])

    def text(self) -> int | str:
        """ Возвращает int, если строка не пустая """
        if super().text() == '':
            return ''
        return int(super(DigitLineEdit, self).text())
