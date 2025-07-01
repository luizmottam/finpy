import grequests
import pandas as pd

headers = {
    "Accept-Linguage": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}


def get_price_acoes_fiis(loop):
    urls = []

    for i in loop:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{i}?range=1d&interval=1d&indicators=quote&includeTimestamp=true"
        urls.append(url)

    rs = (grequests.request("get", u, headers=headers) for u in urls)
    response = grequests.map(rs)

    prices = []
    for res in response:
        try:
            res = res.json()
            df = pd.json_normalize(
                res["chart"]["result"][0]["indicators"]["adjclose"][0], sep="_"
            )
            price = float(df["adjclose"][0][0])
            prices.append(round(price, 2))
        except:
            print("Erro na requisição")
            print("\n")

    return prices