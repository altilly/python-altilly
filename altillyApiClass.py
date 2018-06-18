import time
import json
try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import urljoin
import requests

class AltillyApi(object):
    """ Represents a wrapper for altilly rest API """

    def __init__(self, key, secret):
        self.endpoint = 'https://api.altilly.com/api'
        self.key = key
        self.secret = secret

    def _query_api_public(self, method, parameter=None):
        source = self.endpoint + '/public/' + method
        if parameter:
            source += '/%s' % (parameter)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.get(source, headers=headers)
        return response.json()

    def _query_api_private(self, method, request_type, params={}):
        source = self.endpoint + method
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if request_type == 'get':
            response = requests.get(source, headers=headers, auth=(self.key, self.secret))
        elif request_type == 'post':
            response = requests.post(source, headers=headers, auth=(self.key, self.secret))
        elif request_type == 'delete':
            response = requests.delete(source, headers=headers, auth=(self.key, self.secret))
        elif request_type == 'put':
            response = requests.put(source, headers=headers, auth=(self.key, self.secret))
        return response.json()
    #### PUBLIC API CALLS ####
    def get_all_symbols(self):
        return self._query_api_public(method='symbol')

    def get_symbol(self, symbol):
        return self._query_api_public(method='symbol', parameter=symbol)

    def get_currencies(self):
        return self._query_api_public(method='currency')

    def get_currency(self, currency):
        return self._query_api_public(method='currency', parameter=currency)

    def get_tickers(self):
        return self._query_api_public(method='ticker')

    def get_ticker(self, symbol):
        return self._query_api_public(method='ticker', parameter=symbol)

    def get_simple_trades(self, symbol):
        return self._query_api_public(method='simpletrades', parameter=symbol)

    def get_trades(self, symbol):
        return self._query_api_public(method='trades', parameter=symbol)

    def get_order_book(self, symbol):
        return self._query_api_public(method='orderbook', parameter=symbol)

    def get_simple_order_book(self, symbol):
        return self._query_api_public(method='simpleorders', parameter=symbol)

    def get_candles(self, symbol):
        return self._query_api_public(method='candles', parameter=symbol)
    #### PRIVATE API CALLS ####
    def get_open_orders(self, symbol=None):
        params = {'symbol':symbol}
        return self._query_api_private(method='/order', request_type='get', params=params)

    def create_order(self, symbol, side, quantity, price, timeInForce='GTC', _type='limit', stopPrice=None, tpPrice=None, expireTime=None, strictValidate='false'):
        params = {
        'symbol': symbol, 'side': side,
        'quantity': quantity, 'price':price,
        'timeInForce': timeInForce, 'type': _type,
        'stopPrice': stopPrice, 'tpPrice': tpPrice,
        'expireTime': expireTime, 'strictValidate': strictValidate
        }
        return self._query_api_private(method='/order', request_type='post', params=params)

    def cancel_all_orders(self, symbol):
        params = {'symbol': symbol}
        return self._query_api_private(method='order', request_type='delete', params=params)

    def get_open_order(self, clientOrderId_UUID):
        return self._query_api_private(method='/order/%s' % (clientOrderId_UUID), request_type='get')

    def cancel_order(self, clientOrderId_UUID):
        return self._query_api_private(method='/order/%s' % (clientOrderId_UUID), request_type='delete')

    def get_balances(self):
        return self._query_api_private(method='/trading/balance', request_type='get')

    def get_market_fees(self, symbol):
        return self._query_api_private(method='/trading/fee/%s' % (symbol), request_type='get')

    def get_trade_history(self, symbol=None, sort=None, by=None, _from=None, till=None, limit=None, offset=None):
        params = {
        'symbol': symbol,
        'sort': sort,
        'by': by,
        'from': _from,
        'till': till,
        'limit': limit,
        'offset': offset
        }
        return self._query_api_private(method='/history/trades', request_type='get', params=params)

    def get_order_history(self, symbol, historytype, sort=None, by=None, _from=None, till=None, limit=None, offset=None, clientOrderId=None):
        params = {
        'symbol': symbol,
        'historytype': historytype,
        'sort': sort,
        'by': by,
        'from': _from,
        'till': till,
        'limit': limit,
        'offset': offset,
        'clientOrderId': clientOrderId
        }
        return self._query_api_private(method='/history/order', request_type='get', params=params)

    def get_trade_history_by_id(self, clientOrderId_UUID):
        return self._query_api_private(method='/history/trades/%s' % (clientOrderId_UUID), request_type='get')

    def get_detailed_balances(self):
        return self._query_api_private(method='/account/balance', request_type='get')

    def get_transactions(self, currency, sort=None, by=None, _from=None, till=None, limit=None, offset=None):
        params = {
        'currency': currency,
        'sort': sort,
        'by': by,
        'from': _from,
        'till': till,
        'limit': limit,
        'offset': offset
        }
        return self._query_api_private(method='/account/transactions', request_type='get', params=params)

    def get_transaction_by_id(self, transactionId):
        return self._query_api_private(method='/account/transactions/%s' % (transactionId), request_type='get')

    def initiate_withdrawal(self, currency, amount, address, paymentId=None, includeFee=None, autoCommit=True):
        params = {
        'currency': currency,
        'amount': amount,
        'address': address,
        'paymentId': paymentId,
        'includeFee': includeFee,
        'autoCommit': autoCommit
        }
        return self._query_api_private(method='/account/crypto/withdraw', request_type='post', params=params)

    def commit_withdrawal(self, _id, confirmCode):
        params = {
        'id': _id,
        'confirmCode': confirmCode
        }
        return self._query_api_private(method='/account/crypto/withdraw/%s' % (_id), request_type='put', params=params)

    def cancel_withdrawal(self, _id):
        return self._query_api_private(method='/account/crypto/withdraw/%s' % (_id), request_type='delete')

    def get_deposit_address(self, currency):
        return self._query_api_private(method='/account/crypto/address/%s' % (currency), request_type='get')

    def create_deposit_address(self, currency):
        return self._query_api_private(method='/account/crypto/address/%s' % (currency), request_type='post')
