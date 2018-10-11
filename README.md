# python-altilly
A python implementation of [Altilly](https://www.altilly.com/referral/f446e)'s REST API

## usage
Simply clone the repository and include it in your project, or make a new .py file and copy-paste the RAW text into it.

#### Example usage:

Make an instance of the class like so:

`from altillyApiClass import AltillyApi`


`altilly_api_client = AltillyApi(<APIKEY>, <APISECRET>)`

You can also instantiate it without key, secret as follows:


`altilly_api_client = AltillyApi()`


if you only need public queries.


query account balances:


`balance_info = altilly_api_client.get_balances()`

place a simple order:

`order = altilly_api_client.create_order('ETHBTC', 'sell', '1.0', '0.0505')`


see https://www.altilly.com/page/restapi#/ for full documentation on the REST API.


## found it useful?
BTC : 38y579pT88RZ9AfwEfJnrV6o1bWASuaD3n


DOGE : DBThNeUb9YTGPoRYR2XmDwNQwKciuHWQ7M


MOON : 2SE7fMMSw1XpyQjaboZULg1SxBehQp91ky
