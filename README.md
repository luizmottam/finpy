# Carteira de Investimentos 📈💼

Este projeto é uma aplicação em Python para análise de carteiras de investimentos, com visualizações gráficas e atualização automática dos preços dos ativos via integração com APIs externas.

## 📊 Funcionalidades

- Criação e persistência de portfólio em banco de dados SQLite
- Atualização automática de preços dos ativos (ações, FIIs e câmbio)
- Análises por categoria: Renda Fixa, Ações, Fundos Imobiliários e Internacional
- Gráficos de distribuição dos investimentos usando Matplotlib
- Menu interativo no terminal

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- SQLite (via `sqlite3`)
- Pandas
- Matplotlib
- API de preços integrada (ex: Yahoo Finance via `functions/prices.py`)

---

## 📁 Estrutura do Projeto

```

.
├── db/
│   └── global.db             # Banco de dados SQLite
├── functions/
│   └── prices.py             # Módulo responsável por buscar preços atuais dos ativos
├── wallet.py                   # Script principal com menu e funcionalidades

```

---

## ⚙️ Como Executar

1. Clone este repositório:

   ```bash
   git clone https://github.com/luizmottam/finpy.git
   cd finpy
   ```

2. Instale as dependências (recomenda-se usar um ambiente virtual):

   ```bash
   pip install pandas sqlite3 matplotlib requests numpy
   ```

3. Execute o script principal:

   ```bash
   python wallet.py
   ```

---

## 🧠 Organização dos Dados

A carteira é armazenada em uma tabela SQLite chamada `meu_portfolio`, com as seguintes colunas:

- `scheme_name` — Categoria do ativo (Renda Fixa, Ações, FIIs, Internacional)
- `asset_name` — Nome ou código do ativo
- `accumulated_value` — Valor acumulado em R\$
- `amount` — Quantidade de cotas ou ações (quando aplicável)

---

## 📈 Exemplos de Gráficos

- Gráfico de pizza geral da carteira
- Distribuição detalhada de renda fixa: Prefixado, Pós-fixado, IPCA+
- Distribuições por ativo em ações e FIIs

---

## 🚧 Futuras Melhorias

- Interface gráfica com Tkinter ou PyQt
- Exportação para Excel ou PDF
- Suporte para múltiplos usuários
- Integração com corretoras (via API)
- Métricas financeiras (CVaR, retorno histórico, etc.)

---

## 🤝 Contribuição

Sinta-se livre para abrir issues, propor melhorias ou enviar pull requests. Toda ajuda é bem-vinda!

---

## 👨‍💻 Autor

Luiz de Aquino Motta Mendes
Desenvolvedor Python com foco em análise financeira e automações.
[LinkedIn](https://www.linkedin.com/in/luizmottam) | [GitHub](https://github.com/luizmottam)
