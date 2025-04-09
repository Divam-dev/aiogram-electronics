import requests

def currency_convert():
    """Get USD exchange rate from PrivatBank API"""
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5') 
    data = response.json()
    usd_price = next(item["sale"] for item in data if item["ccy"] == "USD")
    return usd_price