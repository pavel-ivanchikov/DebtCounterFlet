from datetime import datetime
from Transaction import Transaction


class Process:
    all_processes = {}
    path = r"C:/DebtCounter/first/"

    def __init__(self, identifier: tuple[float, float]):
        self.__data = []
        self._me = identifier[0]
        self._parent = identifier[1]
        self._able = {'SET_REMINDER': self.set_reminder, 'INFO': self.info, 'SPLIT': self.split, 'CROSS': self.cross}
        self._reminder_date_time = datetime(9999, 12, 31)
        self._reminder_text = 'No have reminder'
        self.related_processes = []
        Process.all_processes[self.get_process_name()] = self

    def add_transaction(self, transaction: Transaction, init: bool):
        if not init:
            # Тут происходит сериализация
            name = Process.path + str(int(self._me * 10 ** 6)) + '.txt'
            with open(name, 'a', encoding='UTF-8') as file:
                file.write(str(transaction.date) + (' +' if transaction.official else '') + '\n')
                file.write(transaction.text + '\n')
        self.__data.append(transaction)

    def act(self, text, date=None, official=False):
        if date is not None:
            init = True
        else:
            init = False
            date = datetime.now().timestamp()
        if official:
            tag = text.split(' ')[0]
            if tag in self._able:
                return self._able[tag](text, date, init)
            else:
                raise ValueError('Wrong Tag')
        else:
            if text.strip() == '':
                raise ValueError('Value should not be empty')
            self.add_transaction(Transaction(date, text, official), init)

    def info(self, text: str, date: float, init: bool):
        pass

    def split(self, _, date: float, init: bool):
        self.add_transaction(Transaction(date, f'SPLIT {date} from {self._me}', True), init)
        process = Process((date, self._me))
        process.add_transaction(Transaction(date, f'INFO New {date} from {self._me}', True), init)
        self.related_processes.append(process)
        process.related_processes.append(self)
        return process

    def cross(self, text: str, date: float, init: bool):
        if len(text.split(' ')) < 2:
            raise ValueError('You should choose another process to intersect')
        try:
            other_id = float(text.split(' ')[1])
        except ValueError:
            raise ValueError('You should choose the process from the list')
        if other_id == self._me:
            raise ValueError('A process cannot have self-intersections')
        process = Process.get_process(other_id)
        self.add_transaction(Transaction(date, f'CROSS {other_id} and {self._me}', True), init)
        process.add_transaction(Transaction(date, f'INFO CROSS {self._me} and {other_id}', True), init)
        if process not in self.related_processes:
            self.related_processes.append(process)
            process.related_processes.append(self)

    def set_reminder(self, text, date: float, init: bool):
        if text.split(' ')[1] == 'None':
            reminder_datetime = datetime(9999, 12, 31)
            reminder_text = 'No have reminder'
        else:
            if len(text.split(' ')) <= 2:
                raise ValueError('Value should be (date-time + text) or None')
            try:
                reminder_datetime = datetime.strptime(text.split(' ')[1], '%d.%m.%Y-%H:%M:%S')
            except ValueError:
                raise ValueError('Value should be (%d.%m.%Y-%H:%M:%S + text) ')
            reminder_text = ' '.join(text.split(' ')[2:])
        self.add_transaction(Transaction(date, f'SET_REMINDER {reminder_datetime.strftime("%d.%m.%Y-%H:%M:%S")} {reminder_text}', True), init)
        self._reminder_date_time = reminder_datetime
        self._reminder_text = reminder_text

    @staticmethod
    def get_process(identifier: float):
        if str(int(identifier * 10 ** 6)) in Process.all_processes:
            return Process.all_processes[str(int(identifier * 10 ** 6))]
        else:
            raise ValueError('No process with such ID')

    def get_identifier(self):
        return self._me, self._parent

    def get_process_name(self):
        return str(int(self._me * 10 ** 6))

    def get_reminder_date_time(self):
        return self._reminder_date_time

    def get_reminder_text(self):
        return self._reminder_text

    def get_last_date(self):
        return self.__data[-1].date

    def get_last_date_date(self):
        return datetime.fromtimestamp(self.__data[-1].date)

    def get_first_date(self):
        return self.__data[0].date
    def get_first_date_date(self):
        return datetime.fromtimestamp(self.__data[0].date)

    def get_data(self):
        return self.__data[:]

    def get_ables(self):
        return ', '.join(self._able.keys())

    def get_able_list(self):
        return self._able.keys()

    def get_not_official_transaction(self):
        not_official = [i for i in self.__data if not i.official]
        return f'\n' + '\n\n'.join(map(lambda x: str(x), reversed(not_official)))

    def get_all_transaction(self):
        return f'\n' + '\n\n'.join(map(lambda x: str(x), reversed(self.__data)))

    def __repr__(self):
        return self.__class__.__name__ + ' ' + str(self.get_process_name())

    @classmethod
    def create_first_process(cls, date=None):
        init = True
        if date is None:
            date = datetime.now().timestamp()
            init = False
        process = Process((date, 0))
        process.add_transaction(Transaction(date, f'INFO New {date} from {0}', True), init)
        return process
