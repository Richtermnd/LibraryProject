import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QDateEdit

from forms._BaseForm import _BaseForm


class OperationForm(_BaseForm):
    """ Форма для совершения операции """
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
        """ Проврека на корректность операции """
        cur = self.con.cursor()
        # Состояние книги из базы данных
        status, = cur.execute(f"""select status from book where id = {op['book']}""").fetchone()
        # Тип совершаемой операции
        op_type, = cur.execute(f"""select type from operation_type where id = {op['type']}""").fetchone()

        if op_type == 'Возврат':
            if status:
                self.label_exc.setText('Книга уже в библиотеке')
                return False
            else:
                # Текущий и совершивший последнюю операции с книгой клиенты
                curr_client, cur_date = op['client'], op['date']
                prev_client, prev_date = cur.execute(f"""select client, date from operation 
                                                where book = {op['book']} order by id desc""").fetchone()
                if curr_client != prev_client:
                    self.label_exc.setText('Книга не у этого клиента')
                    return False
                # Преобразование даты из формы и из базы данных datetime объект для сравнения
                cur_date = datetime.datetime.strptime(cur_date, '%d.%m.%Y')
                prev_date = datetime.datetime.strptime(prev_date, '%d.%m.%Y')
                if prev_date > cur_date:
                    self.label_exc.setText('Некорректная дата')
                    return False

                # Совершаем операции, если всё нормально
                cur.execute(f"""update book set status = 1 where id = {op['book']}""")
                return True
        else:
            if status:
                # Совершаем операции, если всё нормально
                cur.execute(f"""update book set status = 0 where id = {op['book']}""")
                return True
            else:
                self.label_exc.setText('Книга недоступна')
                return False

    def return_result(self, res):
        # проверка на корректную операцию
        if self.is_correct_op(res):
            self.close()
            self.holder.add_item(res)
