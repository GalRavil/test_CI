import pytest

from ..cashback import Cashback


class TestCashback:
    def setup(self):
        self.cb = Cashback()

    @pytest.mark.parametrize('money_spend, cashb_type, expected', [
        (1000, None, 10),
        (2000, 'usual', 20),
    ])
    def test_usual_cashback(self, money_spend, cashb_type, expected):
        self.cb.calculate(money_spend, cashb_type=cashb_type)

        assert expected == self.cb.cashb_info['usual']['current_balance']

    @pytest.mark.parametrize('several_payments, cashb_type, expected', [
        ([1000, 2000, 3000], None, 60),
        ([10000, 20000, 30000], 'usual', 600),
    ])
    def test_usual_cashback_several(self, several_payments, cashb_type, expected):
        for payment in several_payments:
            self.cb.calculate(payment, cashb_type=cashb_type)

        assert expected == self.cb.cashb_info['usual']['current_balance']

    def test_increased_cashback(self):
        expected = 50
        self.cb.calculate(1000, cashb_type='increased')
        assert expected == self.cb.cashb_info['increased']['current_balance']

    def test_special_cashback(self):
        expected = 300
        self.cb.calculate(1000, cashb_type='special')
        assert expected == self.cb.cashb_info['special']['current_balance']

    @pytest.mark.parametrize('money_spend, cashb_type, exp_increased, exp_usual', [
        (500_000, 'increased', 3000, 4400),
        (400_000, 'increased', 3000, 3400),
        (60_000, 'increased', 3000, 0),
    ])
    def test_increased_cashback_limit(self, money_spend, cashb_type, exp_increased, exp_usual):
        self.cb.calculate(money_spend, cashb_type=cashb_type)

        assert exp_increased == self.cb.cashb_info['increased']['current_balance']
        assert exp_usual == self.cb.cashb_info['usual']['current_balance']

    @pytest.mark.parametrize('money_spend, cashb_type, exp_special, exp_usual', [
        (50_000, 'special', 6000, 300),
        (100_000, 'special', 6000, 800),
        (20_000, 'special', 6000, 0),
    ])
    def test_special_cashback_limit(self, money_spend, cashb_type, exp_special, exp_usual):
        self.cb.calculate(money_spend, cashb_type=cashb_type)

        assert exp_special == self.cb.cashb_info['special']['current_balance']
        assert exp_usual == self.cb.cashb_info['usual']['current_balance']

    @pytest.mark.parametrize('money_spend, cashb_type', [
        (-100, None),
        (-100, 'usual'),
        (-100, 'increased'),
        (-100, 'special'),
    ])
    def test_negative_money_spend(self, money_spend, cashb_type):
        with pytest.raises(ValueError):
            self.cb.calculate(money_spend, cashb_type=cashb_type)

    # @pytest.mark.xfail(raises=ValueError)
    # def test_negative(self):
    #     self.cb.calculate(-100, cashb_type='usual')
