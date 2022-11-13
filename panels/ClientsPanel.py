from forms.ClientFilterForm import ClientFilterForm
from panels._BasePanel import _BasePanel
from info_widgets.ClientInfo import ClientInfo
from forms.ClientForm import ClientForm


class ClientsPanel(_BasePanel):
    def __init__(self):
        filter_form = ClientFilterForm
        add_item_form = ClientForm
        about_widget = ClientInfo
        table = 'client'
        headers = ['id', 'Имя']
        base_req = f'SELECT id, name FROM client;'
        params = [lambda x: x,
                  lambda x: x]
        super().__init__(filter_form, add_item_form, about_widget, table, headers, base_req, params)
        self._initUI()
