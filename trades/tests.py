import json
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from trades.models import Currency, Trade


class TradeListViewTestCase(APITestCase):
    url = reverse("trades:list")

    def setUp(self):
        self.currency_gbp = Currency.objects.create(name='GBP')
        self.currency_eur = Currency.objects.create(name='EUR')

    def test_create_trade(self):
        """
        Test to create a new trade
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 201, response.data)
        expected_response = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": u'1000.00',
            "buy_currency": self.currency_eur.id,
            "buy_amount": u"1250.00",
            "rate": u"1.2500"
        }
        self.assertDictContainsSubset(actual=response.data, expected=expected_response)

    def test_create_trade_check_id(self):
        """
        Test to check ID "TR" + 7 alphanumerics
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['id'][0:2], 'TR')
        self.assertEqual(len(response.data['id']), 9)

    def test_create_trade_data_none(self):
        """
        Test to create a new trade, without data
        """
        response = self.client.post(path=self.url, data=None)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_sell_currency_incorrect(self):
        """
        Test to create a new trade, with incorrect sell currency
        """
        trade = {
            "sell_currency": 100,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_sell_currency_none(self):
        """
        Test to create a new trade, with sell currency = None
        """
        trade = {
            "sell_currency": None,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_sell_amount_negative(self):
        """
        Test to create a new trade, with a negative sell amount
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": -1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_buy_currency_incorrect(self):
        """
        Test to create a new trade, with incorrect buy currency
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": 100,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_buy_currency_none(self):
        """
        Test to create a new trade, with buy currency = None
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": 100,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_trade_check_buy_amount(self):
        """
        Test to check buy amount = sell_amount * rate
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(float(response.data['buy_amount']), trade["sell_amount"] * trade["rate"])

    def test_create_trade_rate_negative(self):
        """
        Test to create a new trade, with a negative rate
        """
        trade = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": -1.25
        }
        response = self.client.post(path=self.url, data=trade)
        self.assertEqual(response.status_code, 400, response.data)


class TradeDetailViewTestCase(APITestCase):

    def setUp(self):
        self.currency_gbp = Currency.objects.create(name='GBP')
        self.currency_eur = Currency.objects.create(name='EUR')
        trade_data = {
            "sell_currency": self.currency_gbp.id,
            "sell_amount": 1000,
            "buy_currency": self.currency_eur.id,
            "rate": 1.25
        }
        response = self.client.post(path=reverse("trades:list"), data=trade_data)
        self.assertEqual(response.status_code, 201, response.data)
        self.trade = response.data

    def test_edit_trade(self):
        """
        Test to edit a trade
        """
        url = reverse("trades:detail", kwargs={"pk": self.trade['id']})

        # Edit trade
        update_trade = {
            'id': self.trade['id'],
            'sell_amount': 2000
        }
        response = self.client.put(url, data=update_trade)
        self.assertEqual(response.status_code, 200, response.data)
        expected_response = {
            "id": self.trade['id'],
            "sell_currency": self.currency_gbp.id,
            "sell_amount": u'2000.00',
            "buy_currency": self.currency_eur.id,
            "buy_amount": u"2500.00",
            "rate": u"1.2500"
        }
        self.assertDictContainsSubset(actual=response.data, expected=expected_response)

    def test_delete_trade(self):
        """
        Test to delete a trade
        """
        url = reverse("trades:detail", kwargs={"pk": self.trade['id']})

        # Delete trade
        response = self.client.delete(url, data={'id': self.trade['id']})
        self.assertEqual(response.status_code, 204, response.data)

        # Check
        response = self.client.get(url, data={'id': self.trade['id']})
        self.assertEqual(response.status_code, 404)
