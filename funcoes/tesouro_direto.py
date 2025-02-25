import requests
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_price_td():
    # Acessando a API do Tesouro Direto
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"

    response = requests.get(url, verify=False)
    json = response.json()
    # O método json_normalize transforma o JSON em um DataFrame, facilitando a manipulação dos dados
    df = pd.json_normalize(json["response"]["TrsrBdTradgList"], sep="_")

    # Exibir o DataFrame resultante
    # TrsrBd_nm = Nome do Tesouro Direto
    # TrsrBd_minRedVal = Valor Mínimo de Aporte
    return df[["TrsrBd_nm", "TrsrBd_minRedVal"]]


def get_price_td_wallet(loop, dataframe):
    prices = []
    
    for nomeDoTitulo in loop:
        result = dataframe.loc[dataframe["TrsrBd_nm"] == nomeDoTitulo].values[0][1]
        prices.append(result)
        
    return prices
    