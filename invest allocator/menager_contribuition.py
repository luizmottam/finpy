import json
import functions.stockPrice as bv
import functions.tesouroDireto as td
import functions.amountFunctions as calc
import pandas as pd
import time
import os

# Cabeçalhos usados em requisições (simula navegador)
headers = {
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

# Cronômetro para medir o tempo de execução (debug)
inicio = time.time()

# Caminho do arquivo da carteira
file_path = '../db/carteira.json'

# Lê a carteira do arquivo JSON
with open(file_path, 'r') as file:
    wallet = json.load(file)

# Converte a carteira em DataFrames
acoes = pd.DataFrame(wallet["Acoes"])
fiis = pd.DataFrame(wallet["Fundos Imobiliarios"])
tesouro = pd.DataFrame(wallet["Tesouro Direto"])

# Busca o preço atual das ações e FIIs
acoes["preco"] = bv.get_price_acoes_fiis(acoes["nome"])
fiis["preco"] = bv.get_price_acoes_fiis(fiis["nome"])

# Busca o preço atual dos títulos do Tesouro Direto
tesouro["preco"] = td.get_price_td_wallet(tesouro["nome"], td.get_price_td())

# Calcula o valor já aplicado
calc.valor_aplicado(acoes)
calc.valor_aplicado(fiis)


def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("{:=^80}\n".format(" INVESTIMENTO "))

        try:
            # Entradas principais
            montante = float(input("Montante no Final do Período: R$ "))
            tempo = int(input("Tempo (meses): "))

            print("\n{:=^80}\n".format(" DISTRIBUIÇÃO "))
            montante_renda_fixa = calc.montante_do_tipo(montante, "Renda Fixa: % ")
            montante_fiis = calc.montante_do_tipo(montante, "Fundos Imobiliários: % ")
            montante_acoes = calc.montante_do_tipo(montante, "Ações: % ")

            # Exibe os valores finais para cada tipo de investimento
            print("\n{:=^80}\n".format(""))
            print("Montante Final de Renda Fixa: R$ ", round(montante_renda_fixa, 2))
            print("Montante Final de Fundos Imobiliários: R$ ", round(montante_fiis, 2))
            print("Montante Final de Ações: R$ ", round(montante_acoes, 2))
            print("\n{:=^80}\n".format(""))

            # Calcula o aporte ideal para cada ativo
            aporte_tesouro = pd.DataFrame(
                calc.aporte(montante_renda_fixa, tesouro, tempo),
                columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"]
            )
            aporte_acoes = pd.DataFrame(
                calc.aporte(montante_acoes, acoes, tempo),
                columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"]
            )
            aporte_fiis = pd.DataFrame(
                calc.aporte(montante_fiis, fiis, tempo),
                columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"]
            )

            # Exibe o aporte necessário por classe
            print(aporte_tesouro[["Nome", "Aporte Real", "Quantidade"]])
            print(aporte_fiis[["Nome", "Aporte Real", "Quantidade"]])
            print(aporte_acoes[["Nome", "Aporte Real", "Quantidade"]])

            # Soma total dos aportes
            aporte_total = (
                aporte_tesouro["Aporte Real"].sum() +
                aporte_acoes["Aporte Real"].sum() +
                aporte_fiis["Aporte Real"].sum()
            )

            print("\n{:=^80}".format(" INFORMAÇÕES ADICIONAIS "))
            print("Aporte Total: R$ ", round(aporte_total, 2))
            print("Aporte em Tesouro Direto: R$ ", round(aporte_tesouro["Aporte Real"].sum(), 2))
            print("Aporte em Fundos Imobiliários: R$ ", round(aporte_fiis["Aporte Real"].sum(), 2))
            print("Aporte em Ações: R$ ", round(aporte_acoes["Aporte Real"].sum(), 2))

            # Mostra quantidade de ativos necessária para atingir o objetivo
            print("\n{:=^80}".format(" QUANTO FALTA "))
            calc.quantidade_final(montante_acoes, acoes)
            calc.quantidade_final(montante_fiis, fiis)

        except Exception as e:
            print("\nErro:", e)
            input("Pressione Enter para tentar novamente.")
            continue

        print("\n{:=^80}".format(" FIM "))
        op = input("Deseja refazer a simulação? (s/n): ").lower()
        if op != "s":
            break


# Executa o menu se for o script principal
if __name__ == "__main__":
    menu()
