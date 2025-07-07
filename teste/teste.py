import pandas as pd

acoes = pd.read_csv('./acoes-listadas-b3.csv', sep=",")
fiis = pd.read_csv('./fundosListados.csv', sep=";", encoding='latin-1')



fiis['Código'] = fiis['Fundo']
fiis['Fundo'] = fiis['Razão Social']
fiis['Razão Social'] = fiis.index
fiis = fiis.reset_index()
fiis = fiis.drop(columns=['index'])
print(fiis.iloc[0], "\n")
print(acoes.iloc[0])

'''
# Colunas da tabela fiis #
Razão Social
Fundo
Código

# Colunas da tabela ações #
Ticker
Nome
Negócios
Última (R$)
Variação


# Similaridade #
Razão Social (transformar em Title) == Nome
Código (Adicionar o 11 ao fundo) == Ticker

# Próximo passo #
O que eu preciso para pesquisa
Ticker,
Nome,
Preço,
DY

O que eu preciso para ticker
Cópia do Investidor 10

'''