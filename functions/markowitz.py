from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import sqlite3 as sql
import markowitz.stockPriceFunctions as gp
from scipy.optimize import minimize
import matplotlib.ticker as mticker


# Função que busca os ativos no banco
def my_assets():
    conn = sql.connect("./db/global.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets")
    result = cursor.fetchall()
    conn.close()
    return [asset for _, asset in result]


# Baixa os preços históricos dos ativos
initial_date = str(datetime.today()).split()[0]
last_10_years = str(datetime.today() - timedelta(days=3650)).split()[0]

# Busca ativos e preços
assets = my_assets()
precos = gp.get_multiple_assets(assets, last_10_years, initial_date)

# Calcula retornos logarítmicos
retornos = np.log(precos / precos.shift(1)).dropna()
media_retornos = retornos.mean()
matriz_cov = retornos.cov()

# Simulação de portfólios
numero_carteiras = 10000
tabela_retornos_esperados = np.zeros(numero_carteiras)
tabela_volatilidade_esperadas = np.zeros(numero_carteiras)
tabela_sharpe = np.zeros(numero_carteiras)
tabela_pesos = np.zeros((numero_carteiras, len(assets)))

for k in range(numero_carteiras):
    pesos = np.random.random(len(assets))
    pesos /= np.sum(pesos)
    tabela_pesos[k, :] = pesos

    tabela_retornos_esperados[k] = np.sum(media_retornos * pesos * 252)
    tabela_volatilidade_esperadas[k] = np.sqrt(
        np.dot(pesos.T, np.dot(matriz_cov * 252, pesos))
    )
    tabela_sharpe[k] = tabela_retornos_esperados[k] / tabela_volatilidade_esperadas[k]

# Seleciona carteira ótima (maior Sharpe)
indice_do_sharpe_maximo = tabela_sharpe.argmax()
melhores_pesos = tabela_pesos[indice_do_sharpe_maximo]


tabela_retornos_esperados_aritmeticos = np.exp(tabela_retornos_esperados) - 1

eixo_y_fronteira_eficiente = np.linspace(
    tabela_retornos_esperados_aritmeticos.min(),
    tabela_retornos_esperados_aritmeticos.max(),
    50,
)


def pegando_retorno(peso_teste):
    peso_teste = np.array(peso_teste)
    retorno = np.sum((media_retornos * peso_teste) * 252)
    retorno = np.exp(retorno) - 1
    return retorno


def checando_soma_pesos(peso_teste):
    return np.sum(peso_teste) - 1


def pegando_vol(peso_teste):
    peso_teste = np.array(peso_teste)
    vol = np.sqrt(np.dot(peso_teste.T, np.dot(matriz_cov * 252, peso_teste)))

    return vol


peso_inicial = [1 / len(assets)] * len(assets)
limites = tuple([(0, 1) for asset in assets])

eixo_x_fronteira_eficiente = []

for retorno_possivel in eixo_y_fronteira_eficiente:
    restricoes = (
        {"type": "eq", "fun": checando_soma_pesos},
        {"type": "eq", "fun": lambda w: pegando_retorno(w) - retorno_possivel},
    )

    resultado = minimize(pegando_vol, peso_inicial)

    eixo_x_fronteira_eficiente.append(resultado["fun"])


fig, ax = plt.subplots()

ax.scatter(
    tabela_volatilidade_esperadas,
    tabela_retornos_esperados_aritmeticos,
    c=tabela_sharpe,
)
plt.xlabel("Volatilidade Esperada")
plt.ylabel("Retorno Esperado")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.scatter(
    tabela_volatilidade_esperadas[indice_do_sharpe_maximo],
    tabela_retornos_esperados_aritmeticos[indice_do_sharpe_maximo],
    c="red"
)
ax.plot(eixo_x_fronteira_eficiente, eixo_y_fronteira_eficiente)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

plt.show()

# Exibe resultado
print("Ativos:", assets)
print("Pesos ótimos:", melhores_pesos)
print(
    f"Retorno esperado: {tabela_retornos_esperados[indice_do_sharpe_maximo] * 100:.2f}%"
)
print(
    f"Volatilidade esperada: {tabela_volatilidade_esperadas[indice_do_sharpe_maximo] * 100:.2f}%"
)
print(f"Índice de Sharpe: {tabela_sharpe[indice_do_sharpe_maximo]:.4f}")
