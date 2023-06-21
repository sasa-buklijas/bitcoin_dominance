import pprint
import sys
import urllib.request
import json
import piesparrow as ps
from datetime import datetime


class BinancePrice:
    #_URL: str = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
    _URL: str = 'https://api.binance.com/api/v3/ticker/24hr?symbols=["BTCUSDT","BTCEUR"]'
    # https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

    def __init__(self):
        try:
            response = urllib.request.urlopen(BinancePrice._URL)
        except urllib.error.HTTPError:
            BinancePrice._URL: str = 'https://api.binance.us/api/v3/ticker/24hr?symbols=["BTCUSDT"]'
            response = urllib.request.urlopen(BinancePrice._URL)

        data = response.read().decode()
        json_data = json.loads(data)
        self.json_data = pprint.pformat(json_data) # for DEBUG
        #pprint.pprint(self.json_data)

        for asset in json_data:
            if asset['symbol'] == 'BTCUSDT':
                self.current = float(asset['lastPrice'])
                self.last24h = float(asset['weightedAvgPrice'])


def main():
    # argv parsing
    output_file = 'bitcoin_price'
    if len(sys.argv) == 2 :
        output_file = sys.argv[1]
        
    bitcoin_price = BinancePrice()

    ps.init(filename = output_file, title = 'Bitcoin price')

    generated_at = datetime.now()
    time_zone = datetime.now().astimezone().tzname()
    title = f'Generated at {generated_at} {time_zone}'
    ps.row(
        ps.colxl(type='box', content=ps.p(title))
    )

    ps.row(
        ps.colxs(align='left', type='box', content=ps.h2(''))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2('Price for one Bitcoin in USDT'))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2('Satoshis (SATs) for one USDT'))
    +   ps.colxs(align='center', type='card', 
                content=ps.h2('Difference in %'))
    )
    diff = bitcoin_price.current/bitcoin_price.last24h * 100 - 100
    ps.row(
        ps.colxs(align='right', type='card', content=ps.h2('Current:'))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2(f'{bitcoin_price.current:.2f} USDT'))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2(f'{100_000_000/bitcoin_price.current:.2f} SATs'))
    +   ps.colxs(align='center', type='card', 
                content=ps.h2(f'{diff:.2f} %')) # razlika
    )
    ps.row(
        ps.colxs(align='right', type='card', content=ps.h2('last 24h:'))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2(f'{bitcoin_price.last24h:.2f} USDT'))
    +   ps.colxs(align='right', type='card', 
                content=ps.h2(f'{100_000_000/bitcoin_price.last24h:.2f} SATs'))
    +   ps.colxs(align='center', type='card', 
                content=ps.h2('---'))
    )

    ps.row(
        ps.colxl(align='center', type='box', content=ps.link('https://github.com/sasa-buklijas/bitcoin_dominance',
                                                            'Code available on GitHub'))
    )

    ps.row(
        ps.colxl(align='center', type='box', content=ps.p('For DEBUG only'))
    )
    ps.row(
        ps.colxl(align='center', type='box', 
                content=ps.p(f'<pre>{bitcoin_price.json_data}</pre>'))
    )


if __name__ == '__main__':
	main()