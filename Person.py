from Transaction import Transaction
from Process import Process
from Debt import Debt


class Person(Process):
    _counter = 0

    def __new__(cls, *args, **kwargs):
        cls._counter += 1
        return object.__new__(cls)

    def __init__(self, identifier: tuple[float, float]):
        super().__init__(identifier)
        self.name = "Person_" + str(self.__class__._counter)
        self.debts = []
        self.additional_ables = {'NEW_DEBT': self.new_debt, 'CHANGE_NAME': self.change_name, 'CHANGE_BIRTHDAY': self.change_birthday}
        self._able.update(self.additional_ables)
        self.birthday = None

    def new_debt(self, _, date: float, init: bool):
        process = Debt((date, self._me))
        self.add_transaction(Transaction(date, f'NEW_DEBT {date} from {self._me}', True), init)
        process.add_transaction(Transaction(date, f'INFO New debt: {date} from {self._me}', True), init)
        self.related_processes.append(process)
        process.related_processes.append(self)
        self.debts.append(process)
        return process

    def change_name(self, text, date: float, init: bool):
        new_name = text.split(' ')[1]
        if not new_name:
            raise ValueError('Value should be not empty')
        self.add_transaction(Transaction(date, f'CHANGE_NAME {new_name} from {self.name}', True), init)
        self.name = new_name

    def change_birthday(self, text, date: float, init: bool):
        new_birthday = text.split(' ')[1]
        if not new_birthday:
            raise ValueError('Value should be not empty')
        self.add_transaction(Transaction(date, f'CHANGE_BIRTHDAY {new_birthday} from {self.birthday}', True), init)
        self.birthday = new_birthday

    def get_able_list(self):
        ans = self._able.copy()
        del ans['INFO']
        del ans['SPLIT']
        return ans.keys()

