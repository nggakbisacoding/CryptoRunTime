import requests
import json
import datetime
from json import (load as jsonload, dump as jsondump)
import os

class coinmarketcap():
    def __init__(self):
        self.api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.config = {
            "currency" : "idr",
            "coins" : [
                "BTC",
                "ETH",
                "XRP",
                "BCH",
                "PAX",
                "XLM",
                "LINK",
                "OMG",
                "KNC",
                "MKR",
                "ZRX",
                "LTC",
                "USDP"
            ],
            "symbol" : "Rp.",
            "api_key" : "38b7c907-2298-40c1-8323-5ca6d247d3bf",
            "limit": "0",
        }
        
    def get_coinmarketcap_latest(self):
        params = {
            "convert": self.config["currency"].upper(),
            "symbol": ",".join(coin.upper() for coin in self.config["coins"]),
        }
        headers = {"X-CMC_PRO_API_KEY": self.config["api_key"]}
        response = requests.get(self.api_url, params=params, headers=headers, timeout=2)
        try:
            api_json = response.json()
        except ValueError as e:
            print(f"Could not parse API response body as JSON:\n{e}", file=sys.stderr)
            return None

        return api_json
    
    def search_coinmarketcap(self, coins):
        limit_counting = int(self.config["limit"])
        if limit_counting >= 100:
           return "Limit Exceeded"
        params = {
            "convert": self.config["currency"].upper(),
            "symbol": coins.upper()
        }
        headers = {"X-CMC_PRO_API_KEY": self.config["api_key"]}
        response = requests.get(self.api_url, params=params, headers=headers, timeout=2)
        try:
            api_json = response.json()
        except ValueError as e:
            print(f"Could not parse API response body as JSON:\n{e}", file=sys.stderr)
            return None
        limit_counting += 1
        with open('limit.ini', 'w', encoding='utf-8') as limit:
            limit.write(str(limit_counting))
            limit.close()

        return api_json

def main():
   crypto = coinmarketcap()
   json_out = crypto.get_coinmarketcap_latest()
   print(json_out)
   with open("data.json", "w", encoding='utf-8') as f:
       json.dump(json_out, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()