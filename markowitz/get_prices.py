import requests
import datetime
import pandas as pd

# Função que busca os preços ajustados de um único ativo (adjclose)
def get_adjclose(symbol, start_date, end_date):
    period1 = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    period2 = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={period1}&period2={period2}&interval=1d&includeAdjustedClose=true"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(f"[ERRO] {symbol} → {r.status_code}")
        return None

    try:
        data = r.json()
        timestamps = data['chart']['result'][0]['timestamp']
        adjclose = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        datas = [datetime.datetime.fromtimestamp(ts).date() for ts in timestamps]

        df = pd.DataFrame({symbol: adjclose}, index=datas)
        return df

    except Exception as e:
        print(f"[EXCEÇÃO] {symbol} → {e}")
        return None

# Junta os preços de vários ativos em colunas (um por ativo)
def get_multiple_assets(symbols, start_date, end_date):
    df_final = pd.DataFrame()

    for symbol in symbols:
        df = get_adjclose(symbol, start_date, end_date)
        if df is not None:
            df_final = df_final.join(df, how='outer') if not df_final.empty else df

    df_final.index.name = "data"
    return df_final

def main():
    # Explicação do uso das funções
    
    # Data de início e fim para a busca dos preços
    initial_date = str(datetime.datetime.today()).split()[0]
    last_month = str(datetime.datetime.today() - datetime.timedelta(days=30)).split()[0]
    last_1_year = str(datetime.datetime.today() - datetime.timedelta(days=365)).split()[0]
    last_5_year = str(datetime.datetime.today() - datetime.timedelta(days=1825)).split()[0]
    last_10_years = str(datetime.datetime.today() - datetime.timedelta(days=3650)).split()[0]

    # Exemplo de uso da função get_adjclose
    ativos = ["ITSA4.SA", "PETR4.SA", "VALE3.SA"]

    # Busca os preços ajustados de um único ativo
    df_final_month = get_multiple_assets(ativos, last_month, initial_date)
    
    # Exibe os preços ajustados dos ativos
    itsa4 = df_final_month["ITSA4.SA"]
    print(f"ITSA4.SA: {itsa4.iloc[-1]}")

# Bloco principal
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[EXCEÇÃO] main() → {e}")
