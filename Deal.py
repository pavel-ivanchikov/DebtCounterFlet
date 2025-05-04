from Transaction import Transaction
from Process import Process


class Deal(Process):
    _currency_list = ['usd', 'ru', 'euro', 'riel', 'minutes']

    def __init__(self, identifier: tuple[float, float]):
        super().__init__(identifier)
        self.name = "Deal_" + str(len(Process.all_processes[str(int(self._parent * 10 ** 6))].debts))
        self.currency_list = Deal._currency_list
        self.deal_currency = "usd"
        self.deal_amount = 0
        self.additional_ables = {'CHANGE_CURRENCY': self.change_currency, 'GIVE': self.give, 'TAKE': self.take}
        self._able.update(self.additional_ables)

    def change_currency(self, text, date: float, init: bool):
        currency = text.split(' ')[1]
        if currency not in Deal._currency_list:
            raise ValueError(f'Currency should be from the list: {Deal._currency_list}')
        elif self.deal_amount != 0:
            raise ValueError('Can not change currency when debt is not zero')
        self.add_transaction(Transaction(date, f'CHANGE_CURRENCY {currency} from {self.deal_currency}', True), init)
        self.deal_currency = currency

    def give(self, text, date: float, init: bool):
        amount = text.split(' ')[1]
        try:
            amount = int(amount)
        except Exception:
            raise ValueError('Value should be positive integer number')
        if amount < 0:
            raise ValueError('Value should be positive integer number')
        self.add_transaction(Transaction(
            date, f'GIVE {amount} balance was {self.deal_amount} now balance is {amount + self.deal_amount}', True), init)
        self.deal_amount += amount

    def take(self, text, date: float, init: bool):
        amount = text.split(' ')[1]
        try:
            amount = int(amount)
        except Exception:
            raise ValueError('Value should be positive integer number')
        if amount < 0:
            raise ValueError('Value should be positive integer number')
        self.add_transaction(Transaction(
            date, f'TAKE {amount} balance was {self.deal_amount} now balance is {self.deal_amount - amount}', True), init)
        self.deal_amount -= amount

    def get_able_list(self):
        ans = self._able.copy()
        del ans['INFO']
        del ans['SPLIT']
        return ans.keys()
