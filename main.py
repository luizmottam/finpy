import json
import funcoes.bolsa_valores as bv
import funcoes.tesouro_direto as td
import funcoes.calc as calc
import pandas as pd
import time
import os

headers = {
    "Accept-Linguage": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

inicio = time.time()
file_path = './db/carteira.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    wallet = json.load(file)

# Transoforma a carteira em tabelas de dataframe
acoes = pd.DataFrame(wallet["Acoes"])
fiis = pd.DataFrame(wallet["Fundos Imobiliarios"])
tesouro = pd.DataFrame(wallet["Tesouro Direto"])

# Função para pegar o preço das Ações e FIIs
acoes["preco"] = bv.get_price_acoes_fiis(acoes["nome"])
fiis["preco"] = bv.get_price_acoes_fiis(fiis["nome"])

# Função para pegar preço do Tesouro Direto:
tesouro["preco"] = td.get_price_td_wallet(tesouro["nome"], td.get_price_td())


calc.valor_aplicado(acoes)
calc.valor_aplicado(fiis)

def menu():
    os.system("cls")
    print("{:=^80}\n".format(" INVESTIMENTO "))
    montante = float(input("Montante no Final do Período: R$ "))
    tempo = int(input("Tempo (meses): "))

    # Porcentagem desejada para cada tipo
    print("\n{:=^80}\n".format(" DISTRIBUIÇÃO "))
    montanteRendaFixa = calc.montante_do_tipo(montante, "Renda Fixa: % ")
    montanteFiis = calc.montante_do_tipo(montante, "Fundos Imobiliários: % ")
    montanteAcoes = calc.montante_do_tipo(montante, "Ações: % ")

    print("\n{:=^80}\n".format(""))
    print("Montante Final de Renda Fixa: R$ ", montanteRendaFixa)
    print("Montante Final de Fundos Imobiliários: R$ ", montanteFiis)
    print("Montante Final de Ações: R$ ", montanteAcoes)
    print("\n{:=^80}\n".format(""))

    aporteTesouro = pd.DataFrame(calc.aporte(montanteRendaFixa, tesouro, tempo), columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"])
    aporteAcoes = pd.DataFrame(calc.aporte(montanteAcoes, acoes, tempo), columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"])
    aporteFiis = pd.DataFrame(calc.aporte(montanteFiis, fiis, tempo), columns=["Nome", "Quantidade", "Aporte Ideal", "Aporte Real"])

    print(aporteTesouro[["Nome", "Aporte Real", "Quantidade"]])
    print(aporteFiis[["Nome", "Aporte Real", "Quantidade"]])
    print(aporteAcoes[["Nome", "Aporte Real", "Quantidade"]])
    
    aporteTotal = aporteTesouro["Aporte Real"].sum() + aporteAcoes["Aporte Real"].sum() + aporteFiis["Aporte Real"].sum()
    
    print("\n{:=^80}".format(" INFROMAÇÕES ADICIONAIS "))
    print("Aporte Total: R$ ", round(aporteTotal, 2))
    print("Aporte em Tesouro Direto: R$ ", round(aporteTesouro["Aporte Real"].sum(), 2))
    print("Aporte em Fundos Imobiliários: R$ ", round(aporteFiis["Aporte Real"].sum(), 2))
    print("Aporte em Ações: R$ ", round(aporteAcoes["Aporte Real"].sum(), 2))
    
    print("\n{:=^80}".format(" QUANTO FALTA "))
    calc.quantidade_final(montanteAcoes, acoes)
    calc.quantidade_final(montanteFiis, fiis)

menu()