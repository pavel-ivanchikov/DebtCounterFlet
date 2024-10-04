import datetime
from Transaction import Transaction
from Process import Process
from Person import Person


class MyLife(Process):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, identifier: tuple[float, float]):
        super().__init__(identifier)
        self.persons = []
        self.additional_ables = {'NEW_PERSON': self.new_person, 'CHANGE_NAME': self.change_name, 'CHANGE_BIRTHDAY': self.change_birthday}
        self._able.update(self.additional_ables)
        self.name = 'Main Process'
        self.birthday = None

    def new_person(self, _, date: float, init: bool):
        self.add_transaction(Transaction(date, f'NEW_PERSON {date} from {self._me}', True), init)
        process = Person((date, self._me))
        process.add_transaction(Transaction(date, f'INFO New person: {date} from {self._me}', True), init)
        self.related_processes.append(process)
        process.related_processes.append(self)
        self.persons.append(process)
        return process

    def change_name(self, text, date: float, init: bool):
        new_name = text.split(' ')[1]
        self.add_transaction(Transaction(date, f'CHANGE_NAME {new_name} from {self.name}', True), init)
        self.name = new_name

    def change_birthday(self, text, date: float, init: bool):
        new_birthday = text.split(' ')[1]
        self.add_transaction(Transaction(date, f'CHANGE_BIRTHDAY {new_birthday} from {self.birthday}', True), init)
        self.birthday = new_birthday

    @classmethod
    def create_first_process(cls, date=None):
        init = True
        if date is None:
            date = datetime.datetime.now(datetime.timezone.utc).timestamp()
            init = False
        process = MyLife((date, 0))
        process.add_transaction(Transaction(date, f'INFO New {date} from {0}', True), init)
        return process
