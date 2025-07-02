import sqlite3 as sql
import pandas as pd

conn = sql.connect("../db/global.db")
df = pd.read_sql("SELECT * FROM historico_contas", con=conn)
print(df)

v_rico = 10071.41
v_avenue = 85.82
v_webull = 34.76
data = "2025-07-02 09:50:39"

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO historico_contas (rico, avenue, webull, data) VALUES (?, ?, ?, ?)",
    (v_rico, v_avenue, v_webull, data),
)
conn.commit()
conn.close()
print("Dados inseridos com sucesso.")

print(df)
