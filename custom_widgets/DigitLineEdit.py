from PyQt5.QtWidgets import QLineEdit


class DigitLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.__is_digit)

    def __is_digit(self):
        if not super().text():
            return
        if not super().text()[-1].isdigit():
            self.setText(super().text()[:-1])

    def text(self) -> int | str:
        if super().text() == '':
            return ''
        return int(super(DigitLineEdit, self).text())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = DigitLineEdit()
    ex.show()
    sys.exit(app.exec())
