import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QDateEdit

from forms._BaseForm import _BaseForm


class OperationForm(_BaseForm):
    def __init__(self, *args, **kwargs):
        super(OperationForm, self).__init__(*args, **kwargs)

    def _initUI(self):
        cur = self.con.cursor()

        label = QLabel('Книга')
        label.setObjectName('book')
        field = QComboBox()
        field.addItems([''] + [str(elem[0]) for elem in cur.execute('SELECT title from book').fetchall()])
        field.required = True
        self.formLayout.addRow(label, field)

        label = QLabel('Клиент')
        label.setObjectName('client')
        field = QComboBox()
        field.addItems([''] + [str(elem[0]) for elem in cur.execute('SELECT name from client').fetchall()])
        field.required = True
        self.formLayout.addRow(label, field)

        label = QLabel('Тип')
        label.setObjectName('type')
        field = QComboBox()
        field.addItems([''] + [str(elem[0]) for elem in cur.execute('SELECT type from operation_type').fetchall()])
        field.required = True
        self.formLayout.addRow(label, field)

        label = QLabel('Дата')
        label.setObjectName('date')
        field = QDateEdit()
        field.setDate(QDate().currentDate())
        self.formLayout.addRow(label, field)

    def is_correct_op(self, op) -> bool:
        cur = self.con.cursor()
        status, = cur.execute(f"""select status from book where id = {op['book']}""").fetchone()
        op_type, = cur.execute(f"""select type from operation_type where id = {op['type']}""").fetchone()

        if op_type == 'Возврат':
            if status:
                self.label_exc.setText('Книга уже в библиотеке')
                return False
            else:
                curr_client, cur_date = op['client'], op['date']
                cur_date = datetime.datetime.strptime(cur_date, '%d.%m.%Y')
                prev_client, prev_date = cur.execute(f"""select client, date from operation 
                                                where book = {op['book']} order by id""").fetchone()[::-1]
                prev_date = datetime.datetime.strptime(prev_date, '%d.%m.%Y')

                if curr_client != prev_client:
                    self.label_exc.setText('Книга не у этого клиента')
                    return False

                if prev_date > cur_date:
                    self.label_exc.setText('Некорректная дата')
                    return False

                cur.execute(f"""update book set status = 1 where id = {op['book']}""")
                return True
        else:
            if status:
                cur.execute(f"""update book set status = 0 where id = {op['book']}""")
                return True
            else:
                self.label_exc.setText('Книга недоступна')
                return False

    def return_result(self, res):
        if self.is_correct_op(res):
            self.close()
            self.holder.add_item(res)
