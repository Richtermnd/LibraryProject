import sys
from PyQt5.QtWidgets import QApplication
from forms.BookFilterForm import BookFilterForm
from panels.BasePanel import BasePanel
from info_widgets.BookPreview import BookPreview


class BookPanel(BasePanel):
    def __init__(self):
        filter_form = BookFilterForm(self)
        about_widget = BookPreview
        table = 'book'
        headers = ['id', 'title', 'author', 'year', 'status']
        base_req = f'SELECT book.id, book.title, author.name, book.year, book.status' \
                   f' FROM {table} INNER JOIN author ON author.id = book.author'
        super(BookPanel, self).__init__(filter_form, about_widget, table, headers, base_req)
        self._initUI()

    def show_about_widget(self):
        try:
            row = self.table_main.currentItem().row()
            index = self.table_main.item(row, 0).text()
            title = self.table_main.item(row, 1).text()
        except AttributeError:
            return

        # if preview is not attr it closing immediately
        self.preview = self.about_widget(index)
        self.preview.show()
        self.write_to_history(title)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookPanel()
    ex.show()
    sys.exit(app.exec())
