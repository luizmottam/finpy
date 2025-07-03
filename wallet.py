# Visão analítica da carteira de investimentos e atualização de preços dos ativos

import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import functions.prices as prices
import os

# Conexão com banco de dados
conn = sql.connect("db/global.db")
cursor = conn.cursor()


def print_wallet():
    # Exibe a carteira atual
    df = pd.read_sql_query("SELECT * FROM meu_portfolio;", conn)
    print(df)


def create_wallet_table():
    # Cria e popula a tabela da carteira
    cursor.execute("DROP TABLE IF EXISTS meu_portfolio;")
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

    webull, avenue = international_assets()
    dolar = prices.get_current_price("USDBRL=X")

    my_wallet = [
        # Renda Fixa
        ["Renda Fixa", "Tesouro Selic", 2009.40, None],
        ["Renda Fixa", "Tesouro Prefixado", 1495.90, None],
        ["Renda Fixa", "Tesouro Prefixado com Juros Semestrais", 329.74, None],
        ["Renda Fixa", "Tesouro IPCA+", 717.94, None],
        ["Renda Fixa", "Tesouro IPCA+ com Juros Semestrais", 460.84, None],
        # Internacional
        ["Internacional", "Webull", round(webull * dolar,2), None],
        ["Internacional", "Avenue", round(avenue * dolar,2), None],
        # Fundos Imobiliários
        ["Fundos Imobiliarios", "MXRF11", 0.00, 105],
        ["Fundos Imobiliarios", "GARE11", 0.00, 60],
        ["Fundos Imobiliarios", "CPTS11", 0.00, 26],
        ["Fundos Imobiliarios", "BRCO11", 0.00, 9],
        ["Fundos Imobiliarios", "RBVA11", 0.00, 40],
        # Ações
        ["Acoes", "ALUP4", 0.00, 7],
        ["Acoes", "BBAS3", 0.00, 28],
        ["Acoes", "BBDC3", 0.00, 18],
        ["Acoes", "CMIG4", 0.00, 9],
        ["Acoes", "ITSA4", 0.00, 60],
        ["Acoes", "ITUB3", 0.00, 9],
        ["Acoes", "TAEE3", 0.00, 5],
    ]

    for asset in my_wallet:
        cursor.execute(
            """
            INSERT INTO meu_portfolio (scheme_name, asset_name, accumulated_value, amount)
            VALUES (?, ?, ?, ?);
            """, asset,
        )

    conn.commit()


def update_accumulated_value(type):
    # Atualiza valores acumulados com base no preço atual
    assets = select_by_group(type)

    for _, row in assets.iterrows():
        asset_name = row["asset_name"]
        amount = row["amount"]
        price = prices.get_current_price(f"{asset_name}.SA")

        if price and amount:
            accumulated_value = round(float(price) * float(amount), 2)
            cursor.execute(
                "UPDATE meu_portfolio SET accumulated_value = ? WHERE asset_name = ?",
                (accumulated_value, asset_name),
            )

    conn.commit()


def international_assets():
    # Busca os valores mais recentes de Webull e Avenue
    wallet = pd.read_sql_query("SELECT * FROM historico_contas;", conn)
    return wallet["webull"].iloc[-1], wallet["avenue"].iloc[-1]


def select_by_group(type):
    # Seleciona ativos por grupo
    wallet = pd.read_sql_query("SELECT * FROM meu_portfolio;", conn)
    return wallet[wallet["scheme_name"] == type]


def sum_by_group(type):
    # Soma o valor total de um grupo
    return select_by_group(type)["accumulated_value"].sum()


def chart_geral_portfolio():
    # Exibe gráfico geral da distribuição da carteira
    tesouro = sum_by_group("Renda Fixa")
    fiis = sum_by_group("Fundos Imobiliarios")
    acoes = sum_by_group("Acoes")
    internacional = sum_by_group("Internacional")

    valores = [tesouro, acoes, fiis, internacional]
    labels = [
        f"Tesouro Direto (R$ {tesouro:,.2f})",
        f"Ações (R$ {acoes:,.2f})",
        f"FIIs (R$ {fiis:,.2f})",
        f"Internacional (R$ {internacional:,.2f})",
    ]

    plt.pie(valores, labels=labels, autopct="%1.1f%%")
    plt.title("Distribuição dos ativos")
    plt.show()


def chart_renda_fixa():
    # Exibe gráfico de detalhamento da Renda Fixa
    assets = select_by_group("Renda Fixa")

    total_posfixado = assets[assets["asset_name"].str.contains("Selic", case=False)][
        "accumulated_value"
    ].sum()
    total_prefixado = assets[
        assets["asset_name"].str.contains("Prefixado", case=False)
    ]["accumulated_value"].sum()
    total_inflacao = assets[assets["asset_name"].str.contains("IPCA", case=False)][
        "accumulated_value"
    ].sum()

    print("Total Pós-fixado (Selic):", total_posfixado)
    print("Total Prefixado:", total_prefixado)
    print("Total Inflação (IPCA):", total_inflacao)

    valores = [total_posfixado, total_prefixado, total_inflacao]
    labels = [
        f"Pós-fixado (Selic): R$ {total_posfixado:.2f}",
        f"Prefixado: R$ {total_prefixado:.2f}",
        f"Inflação (IPCA): R$ {total_inflacao:.2f}",
    ]

    plt.pie(valores, labels=labels, autopct="%1.1f%%")
    plt.title("Distribuição dos ativos em renda fixa")
    plt.show()


def chart_stocks(type, title):
    # Exibe gráfico de ações ou FIIs
    assets = select_by_group(type)

    valores = assets["accumulated_value"].round(2).tolist()
    labels = [
        f"{name} (R$ {val:.2f})" for name, val in zip(assets["asset_name"], valores)
    ]

    plt.pie(valores, labels=labels, autopct="%1.1f%%")
    plt.title(title)
    plt.show()


# ================== MENU ==================


def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== MENU CARTEIRA DE INVESTIMENTOS ===")
        print("1. Criar carteira")
        print("2. Exibir carteira")
        print("3. Atualizar valores acumulados (ações)")
        print("4. Atualizar valores acumulados (FIIs)")
        print("5. Gráfico geral")
        print("6. Gráfico renda fixa")
        print("7. Gráfico ações")
        print("8. Gráfico FIIs")
        print("0. Sair")
        opc = input("Escolha uma opção: ")

        if opc == "1":
            create_wallet_table()
        elif opc == "2":
            print_wallet()
            input("Pressione Enter para continuar...")
        elif opc == "3":
            update_accumulated_value("Acoes")
        elif opc == "4":
            update_accumulated_value("Fundos Imobiliarios")
        elif opc == "5":
            chart_geral_portfolio()
        elif opc == "6":
            chart_renda_fixa()
            chart_stocks("Renda Fixa", "Distribuição dos ativos em renda fixa")
        elif opc == "7":
            chart_stocks("Acoes", "Distribuição dos ativos em ações")
        elif opc == "8":
            chart_stocks(
                "Fundos Imobiliarios", "Distribuição dos ativos em fundos imobiliários"
            )
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")


# Iniciar menu
if __name__ == "__main__":
    menu()
