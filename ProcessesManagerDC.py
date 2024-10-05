import datetime
from ProcessesManager import ProcessesManager
from MyLife import MyLife
from Person import Person
from Debt import Debt


class ProcessesManagerDC(ProcessesManager):
    def __init__(self, path: str):
        super().__init__(path)
        self.new_process_tags = ('SPLIT', 'NEW_PERSON', 'NEW_DEBT')
        self.info_dict = {}
        self.previous_action_result = 'Wellcome!'
        self.positions = []
        self.all_transaction = None

    def controller(self):
        total_amount = 0
        for process in self.main_dict.values():
            if isinstance(process, MyLife):
                self.info_dict[process.get_process_name()] = [process.name]
            elif isinstance(process, Person):
                self.info_dict[process.get_process_name()] = [process.name]
                amount = sum(map(lambda x: x.debt_amount, process.debts))
                total_amount += amount
                self.info_dict[process.get_process_name()].append(process.name
                                                                  + ' balance: ' + str(amount))
            elif isinstance(process, Debt):
                self.info_dict[process.get_process_name()] = ['Debt of ' + process.related_processes[0].name]
                self.info_dict[process.get_process_name()].append('Debt of '
                                                                  + process.related_processes[0].name + ": "
                                                                  + str(process.debt_amount) + ' '
                                                                  + str(process.debt_currency))
            else:
                self.info_dict[process.get_process_name()] = [process.get_process_name()]
                self.info_dict[process.get_process_name()].append(process.get_process_name()
                                                                  + " from " + process.related_processes[0].get_process_name())
        self.info_dict[self.first_process_name].append(self.first_process.name
                                                       + ' balance: ' + str(total_amount))

    def get_transactionDC(self, name, n=None):
        process = self.main_dict[name]
        ans = []
        if n is None:
            data = process.get_data()
        else:
            data = process.get_data()[-n:]
        for transaction in reversed(data):
            if transaction.official:
                date = datetime.datetime.fromtimestamp(transaction.date)
                date_text = date.strftime("%Y-%m-%d %H:%M:%S")
                tag = transaction.text.split()[0]
                if tag == 'INFO':
                    tag2 = transaction.text.split()[1]
                    if tag2 == 'New':
                        message = f'{date_text}\nThe process was created'
                    elif tag2 == 'CROSS':
                        name_float = float(transaction.text.split()[2])
                        name = str(int(name_float * 10 ** 6))
                        message = f'{date_text}\nThe process was crossed with {self.info_dict[name][0]}'
                    else:
                        message = f'{date_text}\nSome another information'
                elif tag == 'SPLIT':
                        name_float = float(transaction.text.split()[1])
                        name = str(int(name_float * 10 ** 6))
                        message = f'{date_text}\nThe process, {name}, was created'
                elif tag == 'CROSS':
                    name_float = float(transaction.text.split()[1])
                    name = str(int(name_float * 10 ** 6))
                    message = f'{date_text}\nThe process was crossed with {self.info_dict[name][0]}'
                elif tag == 'NEW_PERSON':
                    name_float = float(transaction.text.split()[1])
                    name = str(int(name_float * 10 ** 6))
                    message = f'{date_text}\nNew person, {self.info_dict[name][0]}, was created'
                elif tag == 'NEW_DEBT':
                    message = f'{date_text}\nNew debt was created'
                elif tag == 'CHANGE_NAME':
                    message = f'{date_text}\nThe name was changed from {transaction.text.split()[3]}'
                elif tag == 'CHANGE_BIRTHDAY':
                    message = f'{date_text}\nThe birth day was changed'
                elif tag == 'CHANGE_CURRENCY':
                    message = f'{date_text}\nThe currency was changed'
                elif tag == 'GIVE':
                    amount = transaction.text.split()[1]
                    debt = transaction.text.split()[4]
                    message = f'{date_text}\nI gave {amount}. Debt was {debt}'
                elif tag == 'TAKE':
                    amount = transaction.text.split()[1]
                    debt = transaction.text.split()[4]
                    message = f'{date_text}\nI took {amount}. Debt was {debt}'
                else:
                    message = f'{date_text}\nUnknown tag'
                ans.append(message)
            else:
                ans.append(str(transaction))
        return f'\n' + '\n\n'.join(ans)

    def get_main_process(self):
        return MyLife.create_first_process(int(self.first_process_name) / 10 ** 6)

    def deserialization(self):
        super().deserialization()
        self.controller()

    def add_new_process(self, process):
        super().add_new_process(process)
        self.controller()
