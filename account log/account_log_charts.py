# Importar bibliotecas necessárias
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Conectar ao banco de dados
conn = sqlite3.connect("../db/global.db")

# Ler dados do banco
df = pd.read_sql("SELECT * FROM historico_contas", con=conn)

avenue = df[['avenue', 'data']]
rico = df[['rico', 'data']]
webull = df[['webull', 'data']]

print(avenue)



plt.plot(avenue['data'], avenue['avenue'], label='Avenue')
plt.xlabel('Data')
plt.ylabel('Avenue')
plt.title('Avenue ao longo do tempo')
plt.legend()
plt.show()
plt.close()

plt.plot(rico['data'], rico['rico'], label='Rico')
plt.xlabel('Data')
plt.ylabel('Rico')
plt.title('Rico ao longo do tempo')
plt.legend()
plt.show()
plt.close()

plt.plot(webull['data'], webull['webull'], label='Webull')
plt.xlabel('Data')
plt.ylabel('Webull')
plt.title('Webull ao longo do tempo')
plt.legend()
plt.show()
plt.close()

ativos_nacionais = rico['rico'].iloc[-1]
ativos_internacionais = (float(avenue['avenue'].iloc[-1]) + float(webull['webull'].iloc[-1])) * 5.474

plt.pie([ativos_nacionais, ativos_internacionais], labels=['Ativos Nacionais', 'Ativos Internacionais'], autopct='%1.1f%%')
plt.title('Distribuição dos ativos')
plt.show()



