from forms.BookFilterForm import BookFilterForm
from panels._BasePanel import _BasePanel
from info_widgets.BookPreview import BookPreview
from forms.BookForm import BookForm


class BooksPanel(_BasePanel):
    def __init__(self):
        filter_form = BookFilterForm
        add_item_form = BookForm
        about_widget = BookPreview
        table = 'book'
        headers = ['id', 'Название', 'Автор', 'Жанр', 'Год', 'Состояние']
        base_req = f"""
                        SELECT book.id,
                            book.title,
                            author.name,
                            genre.name,
                            book.year,
                            book.status
                        FROM book
                            LEFT JOIN
                            author ON book.author = author.id
                            LEFT JOIN
                            genre ON book.genre = genre.id;
    
                    """
        params = [lambda x: x,
                  lambda x: x,
                  lambda x: self.con.cursor().execute(f"""select name from author where id = {x}""").fetchone()[0],
                  lambda x: self.con.cursor().execute(f"""select name from genre where id = {x}""").fetchone()[0],
                  lambda x: x,
                  lambda x: x - 1]
        super().__init__(filter_form, add_item_form, about_widget, table, headers, base_req, params)
        self._initUI()
