

from info_widgets.BookPreview import BookPreview
from info_widgets.ClientInfo import ClientInfo
from panels._BasePanel import _BasePanel
from forms.OperationsFilterForm import OperationsFilterForm
from forms.OperationForm import OperationForm


class OperationsPanel(_BasePanel):
    def __init__(self):
        filter_form = OperationsFilterForm
        add_item_form = OperationForm
        about_widget = None
        table = 'operation'
        headers = ['id', 'Книга', 'Клиент', 'Тип', 'Дата']
        base_req = f"""
                        SELECT operation.id,
                             book.title,
                             client.name,
                             operation_type.type,
                             operation.date
                        FROM operation
                             INNER JOIN
                             book,
                             client,
                             operation_type ON operation.book = book.id AND 
                                               operation.client = client.id AND 
                                               operation.type = operation_type.id ORDER BY operation.id desc;
                  """
        params = [lambda x: x,
                  lambda x: x,
                  lambda x: self.con.cursor().execute(f"""select name from client where id = {x}""").fetchone()[0],
                  lambda x: self.con.cursor().execute(f"""select type from operation_type 
                                                              where id = {x}""").fetchone()[0],
                  lambda x: x]
        super().__init__(filter_form, add_item_form, about_widget, table, headers, base_req, params)

    def show_about_widget(self):
        try:
            row = self.table_main.currentItem().row()
            col = self.table_main.currentItem().column()
            title = self.table_main.item(row, col).text()
        except AttributeError:
            return
        if col == 1:
            cur = self.con.cursor()
            index, = cur.execute(f"""select id from book where title = ?""", (title, )).fetchone()
            self.preview = BookPreview(index)
        elif col == 2:
            cur = self.con.cursor()
            index, = cur.execute(f"""select id from client where name = ?""", (title, )).fetchone()
            self.preview = ClientInfo(index)
        else:
            return
        # if preview is not attr it closing immediately
        self.preview.show()
        self.write_to_history(title)
