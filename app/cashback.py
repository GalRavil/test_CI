""" ДЗ №1: кэшбэк по карте

Напишите функцию, которая расчитывает кэшбэк по карте:

В зависимости от категории покупки кэшбэк может быть выше или ниже:
• за обычные покупки банк начислит 1%
• за покупки в категориях повышенного кэшбэка — 5%
• за покупки по спецпредложениям — 30%

Лимиты:
• повышенный - 3000
• специальный - 6000
"""

import json


class Cashback():
    def __init__(self):
        self.cashb_info = {
            'usual': {
                'coefficient': 0.01,
                'limit': 1_000_000_000,
                'current_balance': 0,
            },

            'increased': {
                'coefficient': 0.05,
                'limit': 3000,
                'current_balance': 0,
            },

            'special': {
                'coefficient': 0.3,
                'limit': 6000,
                'current_balance': 0,
            },
        }

        self.default_cashb_type = 'usual'

    def calculate(self, money_spend, cashb_type=None):
        """Рассчитать кэшбек"""

        if cashb_type is None:
            cashb_type = self.default_cashb_type

        if money_spend <= 0:
            raise ValueError('The amount of money spent shold be more than 0.00$')
        cashback = money_spend * self.cashb_info[cashb_type]['coefficient']

        # проверка на лимиты кэшбека
        if self.check_cashback_limit(cashback, cashb_type):
            self.cashb_info[cashb_type]['current_balance'] += cashback
        else:
            limit = self.cashb_info[cashb_type]['limit']
            now = self.cashb_info[cashb_type]['current_balance']
            until_limit = limit - now

            # заполнить current_balance до лимита
            self.cashb_info[cashb_type]['current_balance'] = limit

            # оставшийся кэшбек после заполнения лимита
            rest_cashb = (cashback - until_limit)
            rest_money_spend = rest_cashb / self.cashb_info[cashb_type]['coefficient']
            # оставшийся кэшбек (rest_cashb) рассчитать по дефолтному типу кэшбека
            rest_cashb = rest_money_spend * self.cashb_info[self.default_cashb_type]['coefficient']

            # залить в деффолтный кэшбек
            self.cashb_info[self.default_cashb_type]['current_balance'] += rest_cashb

    def check_cashback_limit(self, cashback, cashb_type):
        """Проверить кэшбек-лимит определенного типа"""

        limit = self.cashb_info[cashb_type]['limit']
        now = self.cashb_info[cashb_type]['current_balance']

        if limit >= now + cashback:
            return True

    def get_info(self):
        """Принтнуть информацию в форматированном виде"""
        print(json.dumps(self.cashb_info, indent=2))

# c = Cashback()

# c.calculate(-100)
# c.calculate(5000)
# # c.get_info()

# c.calculate(5000, cashb_type='special')
# # c.get_info()

# c.calculate(100000, cashb_type='special')
# c.get_info()

# c.calculate(400000, cashb_type='increased')
# c.get_info()