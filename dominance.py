from dataclasses import dataclass, field
import sys
from typing import ClassVar
import urllib.request
import json
from collections import OrderedDict
import piesparrow as ps
import pandas as pd
from datetime import datetime

# https://www.coingecko.com/en/api/documentation
@dataclass
class CoinGeckoMarketCap:
    _URL: ClassVar[str] = field(default='https://api.coingecko.com/api/v3/global', 
                                init=False, compare=False)
    market_cap_percentage: OrderedDict

    def __init__(self):
        response = urllib.request.urlopen(self._URL)

        if response.getcode() != 200:
            print(f'{response.getcode()=} not 200')
            exit()

        data = response.read().decode()
        json_data = json.loads(data)

        self.updated_at = json_data['data']['updated_at']

        market_cap_percentage: dict = json_data['data']['market_cap_percentage']
        self.market_cap_percentage = OrderedDict(sorted(market_cap_percentage.items(),
                                                    key=lambda x: x[1], reverse = True))

        # add percent for rest of crypto
        number_of_active_cryptocurrencies = json_data['data']['active_cryptocurrencies']
        title = f'rest {number_of_active_cryptocurrencies-len(market_cap_percentage)}' \
                f' cryptocurrencies'
        self.market_cap_percentage[title] = 100.00 - sum(market_cap_percentage.values())


def main():
    # argv parsing
    output_file = 'bitcoin_dominance'
    if len(sys.argv) == 2 :
        output_file = sys.argv[1]
        
    coin_gecko_market_cap = CoinGeckoMarketCap()

    data = pd.DataFrame([coin_gecko_market_cap.market_cap_percentage])  # https://stackoverflow.com/a/46577585/2006674
    #print(data)
    crypto_currencies = [i for i in coin_gecko_market_cap.market_cap_percentage.keys()]

    ps.init(filename = output_file, title = 'Bitcoin market cap vs. crypto')

    generated_at = datetime.now()
    time_zone = datetime.now().astimezone().tzname()
    update_at = datetime.fromtimestamp(coin_gecko_market_cap.updated_at)
    title = f'Generated at {generated_at} {time_zone}, with data from {update_at} {time_zone}'
    ps.row(
        ps.colxl(type='box', content=ps.p(title))
    )

    ps.row(
        ps.colxl(type='box', content=ps.h1('Bitcoin market cap vs. crypto'))
    )

    ps.row(
        ps.pie(
            title = 'justID',
            df = data,
            columns = crypto_currencies,
            legendposition = 'right',
        )
    )

    to_remove = ['usdt', 'usdc']
    found: list = []
    without_stable_coins: list = []
    for i in crypto_currencies:
        if i in to_remove:
            found.append(i)
        else:
            without_stable_coins.append(i)

    ps.row(
        ps.colxl(type='box', content=ps.h1(
            f'Bitcoin market cap vs. crypto(but without {found})'))
    )
    ps.row(
        ps.pie(
        
            title = 'anotherID',
            df = data,
            columns = without_stable_coins,
            legendposition = 'right',
        )
    )

    ps.row(
        ps.colmd(type='box', content=ps.link(target='https://www.coingecko.com/en/api/documentation', label='Data from CoinGecko'))
    +   ps.colmd(align='center', type='box', content=ps.link('https://github.com/sasa-buklijas/bitcoin_dominance',
                                                            'Code available on GitHub'))
    )


if __name__ == '__main__':
	main()