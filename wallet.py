# Nesse programa construimos uma visão analítica da nossa carteira de investimentos, e fazemos a atualização dos preços dos ativos.

# Importar bibliotecas necessárias
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import functions.prices as prices
import os

conn = sql.connect("db/global.db")
cursor = conn.cursor()


def print_wallet():
    df = pd.read_sql_query("SELECT * FROM meu_portfolio;", conn)
    print(df)


def create_wallet_table():
    # Criar tabela de portfólio se não existir
    cursor.execute("DROP TABLE meu_portfolio;")
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS meu_portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name TEXT NOT NULL,
        asset_name TEXT NOT NULL,
        accumulated_value REAL NOT NULL,
        amount INTEGER
    );
    """
    )

    # Inserindo dados de exemplo na tabela meu_portfolio
    my_wallet = [
        ["Renda Fixa", "Tesouro Selic", 2007.11, None],
        ["Renda Fixa", "Tesouro Prefixado", 1483.11, None],
        ["Renda Fixa", "Tesouro Prefixado com Juros Semestrais", 342.54, None],
        ["Renda Fixa", "Tesouro IPCA+", 714.36, None],
        ["Renda Fixa", "Tesouro IPCA+ com Juros Semestrais", 457.68, None],
        ["Fundos Imobiliarios", "MXRF11", 0.00, 105],
        ["Fundos Imobiliarios", "GARE11", 0.00, 60],
        ["Fundos Imobiliarios", "CPTS11", 0.00, 26],
        ["Fundos Imobiliarios", "BRCO11", 0.00, 9],
        ["Fundos Imobiliarios", "RBVA11", 0.00, 40],
        ["Acoes", "ALUP4", 0.00, 5],
        ["Acoes", "BBAS3", 0.00, 28],
        ["Acoes", "BBDC3", 0.00, 18],
        ["Acoes", "CMIG4", 0.00, 9],
        ["Acoes", "ITSA4", 0.00, 60],
        ["Acoes", "ITUB3", 0.00, 9],
        ["Acoes", "TAEE3", 0.00, 5],
    ]

    # Inserir dados na tabela meu_portfolio
    for asset in my_wallet:
        cursor.execute(
            """
        INSERT INTO meu_portfolio (scheme_name, asset_name, accumulated_value, amount)
        VALUES (?, ?, ?, ?);
        """,
            (asset[0], asset[1], asset[2], asset[3]),
        )

    conn.commit()


def update_accumulated_value(type):
    wallet = pd.read_sql_query("SELECT * FROM meu_portfolio;", conn)

    assets = wallet[wallet["scheme_name"] == type]

    for i in range(len(assets)):
        asset_name = assets["asset_name"].iloc[i]
        price = prices.get_current_price(f"{asset_name}.SA")
        amount = assets["amount"].iloc[i]

        accumulated_value = float(price) * float(amount)
        cursor.execute(
            "UPDATE meu_portfolio SET accumulated_value = ? WHERE asset_name = ?",
            (round(float(accumulated_value), 2), asset_name),
        )
    conn.commit()

    print_wallet()

# create_wallet_table()
# update_accumulated_value("Fundos Imobiliarios")
# update_accumulated_value("Acoes")


def sum_by_group(type):
    wallet = pd.read_sql_query("SELECT * FROM meu_portfolio;", conn)

    asset = wallet[wallet["scheme_name"] == type]
    
    total_value = asset['accumulated_value'].sum()
    return total_value
    
    
tesouro = sum_by_group('Renda Fixa')
fiis = sum_by_group('Fundos Imobiliarios')
acoes = sum_by_group('Acoes')

print(tesouro)
print(fiis)
print(acoes)

plt.pie([tesouro, acoes, fiis], labels=['Tesouro Direto', 'Ações', 'FIIs'], autopct='%1.1f%%')
plt.title('Distribuição dos ativos')
plt.show()
