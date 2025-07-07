import dividendYeld as dy
import sqlite3 as sql
import pandas as pd
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

conn = sql.connect("../db/global.db")

portfolio = pd.read_sql_query("select * from meu_portfolio;", conn)

acoes = portfolio[portfolio["scheme_name"] == "Acoes"]
fiis = portfolio[portfolio["scheme_name"] == "Fundos Imobiliarios"]


url_fiis = 'https://investidor10.com.br/fiis/'
url_acoes = 'https://investidor10.com.br/acoes/'

for i in fiis["asset_name"]:
    dividend = dy.get_dy(url_fiis, i)
    print(f"Ações: {i}\t P/VP: {dividend}")
    
for i in acoes["asset_name"]:
    dividend = dy.get_dy(url_acoes, i)
    print(f"Ações: {i}\t P/VP: {dividend}")