import customtkinter as ctk
import sqlite3
from datetime import datetime
import os

# Caminho do banco
DB_PATH = os.path.join("db", "global.db")

# Inicializar o banco
def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rico REAL NOT NULL,
            avenue REAL NOT NULL,
            webull REAL NOT NULL,
            data TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Inserir dados no banco
def inserir_dados(janela):
    try:
        v_rico = float(entry_rico.get())
        v_avenue = float(entry_avenue.get())
        v_webull = float(entry_webull.get())
    except ValueError:
        print("Todos os campos devem ser preenchidos com valores numéricos.")
        return

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO historico_contas (rico, avenue, webull, data) VALUES (?, ?, ?, ?)",
        (v_rico, v_avenue, v_webull, data)
    )
    conn.commit()
    conn.close()
    print("Dados inseridos com sucesso.")

    janela.destroy()


# Centralizar janela na tela
def centralizar(janela):
    janela.update_idletasks()
    width = janela.winfo_width()
    height = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (width // 2)
    y = (janela.winfo_screenheight() // 2) - (height // 2)
    janela.geometry(f"{width}x{height}+{x}+{y}")

# Setup
init_db()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Registro Financeiro")
app.geometry("400x250")
app.resizable(False, False)

# Estilo dos campos
entry_style = {"width": 250, "height": 40, "corner_radius": 20, "fg_color": "#d3d3d3", "text_color": "black"}

entry_rico = ctk.CTkEntry(app, placeholder_text="Rico : R$", **entry_style)
entry_rico.pack(pady=10)

entry_avenue = ctk.CTkEntry(app, placeholder_text="Avenue : R$", **entry_style)
entry_avenue.pack(pady=10)

entry_webull = ctk.CTkEntry(app, placeholder_text="Webull : R$", **entry_style)
entry_webull.pack(pady=10)

botao = ctk.CTkButton(app, text="Enviar", command=lambda: inserir_dados(app), corner_radius=20, width=150, height=40)
botao.pack(pady=20)

# Centralizar depois que tudo estiver empacotado
centralizar(app)
app.mainloop()