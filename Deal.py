from Transaction import Transaction
from Process import Process


class Deal(Process):
    _currency_list = ['usd', 'ru', 'euro', 'riel']

    def __init__(self, identifier: tuple[float, float]):
        super().__init__(identifier)
        self.name = "Deal_" + str(len(Process.all_processes[str(int(self._parent * 10 ** 6))].debts))
        self.currency_list = ['usd', 'ru', 'euro', 'riel']
        self.debt_currency = "usd"
        self.debt_amount = 0
        self.additional_ables = {'CHANGE_CURRENCY': self.change_currency, 'GIVE': self.give, 'TAKE': self.take}
        self._able.update(self.additional_ables)

    def change_currency(self, text, date: float, init: bool):
        currency = text.split(' ')[1]
        if currency not in Deal._currency_list:
            raise ValueError(f'Currency should be from the list: {Deal._currency_list}')
        elif self.debt_amount != 0:
            raise ValueError('Can not change currency when debt is not zero')
        self.add_transaction(Transaction(date, f'CHANGE_CURRENCY {currency} from {self.debt_currency}', True), init)
        self.debt_currency = currency

    def give(self, text, date: float, init: bool):
        amount = text.split(' ')[1]
        try:
            amount = int(amount)
        except Exception:
            raise ValueError('Value should be positive integer number')
        if amount < 0:
            raise ValueError('Value should be positive integer number')
        self.add_transaction(Transaction(
            date, f'GIVE {amount} debt was {self.debt_amount} now debt is {amount + self.debt_amount}', True), init)
        self.debt_amount += amount

    def take(self, text, date: float, init: bool):
        amount = text.split(' ')[1]
        try:
            amount = int(amount)
        except Exception:
            raise ValueError('Value should be positive integer number')
        if amount < 0:
            raise ValueError('Value should be positive integer number')
        self.add_transaction(Transaction(
            date, f'TAKE {amount} debt was {self.debt_amount} now debt is {self.debt_amount - amount}', True), init)
        self.debt_amount -= amount

    def get_able_list(self):
        ans = self._able.copy()
        del ans['INFO']
        del ans['SPLIT']
        return ans.keys()
