import sys
from PyQt5.QtWidgets import QApplication
from forms.FilterForm import FilterForm
from BasePanel import BasePanel


class BookPanel(BasePanel):
    def __init__(self):
        self.filter_form = FilterForm(self)
        self.table = 'book'
        self.headers = ['id', 'title', 'author', 'year', 'status']
        super().__init__()

    def get_form_result(self, res):
        self.add_filter(res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookPanel()
    ex.show()
    sys.exit(app.exec())
