from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from panels import BooksPanel
from panels import OperationsPanel
from panels import ClientsPanel
from forms import AuthorForm, GenreForm


class MainWindow(QMainWindow):
    """ Главное окно """
    def __init__(self):
        super().__init__()
        uic.loadUi(r'ui\MainWindow.ui', self)
        self._initUI()

    # Соединение событий с необходимыми функциями
    def _initUI(self):

        self.open_books_panel.triggered.connect(lambda: self.setCentralWidget(BooksPanel.BooksPanel()))
        self.open_operations_panel.triggered.connect(lambda: self.setCentralWidget(OperationsPanel.OperationsPanel()))
        self.open_client_panel.triggered.connect(lambda: self.setCentralWidget(ClientsPanel.ClientsPanel()))

        self.action_add_item.triggered.connect(lambda: self.centralWidget().show_add_item_form())
        self.action_add_filter.triggered.connect(lambda: self.centralWidget().button_add_filter.click())

        self.action_add_author.triggered.connect(self.show_other_form)
        self.action_add_genre.triggered.connect(self.show_other_form)
        self.setCentralWidget(BooksPanel.BooksPanel())

    # В зависимости от отправителя открывает нужную форму
    def show_other_form(self):
        match self.sender():
            case self.action_add_author:
                self.form = AuthorForm.AuthorForm(self)
            case self.action_add_genre:
                self.form = GenreForm.GenreForm(self)
        self.form.show()
