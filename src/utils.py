import requests

def get_binance_price(symbol):
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'
        response = requests.get(url)
        return float(response.json()['price'])
    except Exception as e:
        print(f"바이낸스 가격 조회 실패: {e}")
        return None

def get_upbit_price(symbol):
    try:
        url = f'https://api.upbit.com/v1/ticker?markets=KRW-{symbol}'
        response = requests.get(url)
        return float(response.json()[0]['trade_price'])
    except Exception as e:
        print(f"업비트 가격 조회 실패: {e}")
        return None