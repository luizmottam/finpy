import pandas as pd
import sqlite3 as sql

df = pd.read_csv("./acoes-listadas-b3.csv", sep=",")

print(df)

conn = sql.connect("./finweb.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Ticker VARCHAR(6) NOT NULL,
        Nome VARCHAR(50) NOT NULL,
        Preco REAL NOT NULL,
        Variacao VARCHAR(10) NOT NULL
    );        
    """
)

for i in range(len(df)):
    try: 
        ticker = df['Ticker'].iloc[i]
        name = df['Nome'].iloc[i]
        price = df['Última (R$)'].iloc[i]
        change = df['Variação'].iloc[i]
        
        cursor.execute("INSERT INTO stocks (Ticker, Nome, Preco, Variacao) VALUES (?, ?, ?, ?)", (ticker, name, price, change))
    except Exception as e:
        print("Erro => ", e)
    
conn.commit()
cursor.close()