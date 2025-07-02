# Manager Contribution 💰📊

> Gerenciador inteligente de aportes mensais para carteiras de investimento.

---

## 📌 Sobre o Projeto

O **Manager Contribution** é uma ferramenta em Python desenvolvida para auxiliar investidores a distribuírem aportes mensais de forma estratégica, respeitando uma alocação de carteira personalizada. Com base no objetivo financeiro, tempo estimado e percentual de alocação por classe de ativo, o sistema calcula quanto investir em cada ativo da carteira, considerando os preços atualizados de mercado.

---

## ⚙️ Funcionalidades

- 📂 Leitura da carteira personalizada em `.json`
- 💵 Atualização automática dos preços dos ativos (Tesouro Direto, Ações e FIIs)
- 📈 Cálculo ideal de aporte por ativo com base no objetivo e tempo
- 🧮 Simulação de evolução da carteira ao longo do tempo
- 📊 Exibição dos aportes por ativo e categoria (com detalhamento)
- 👨‍🏫 Estimativa de quantidade de ativos a alcançar

---

## 🧠 Como Funciona

1. Você informa:

   - O **montante** desejado no final do período
   - O **tempo** (em meses)
   - A alocação percentual para cada tipo de investimento

2. O sistema:
   - Lê sua carteira do arquivo `carteira.json`
   - Busca os preços atualizados dos ativos
   - Calcula os **valores ideais de aporte por ativo**
   - Mostra a **quantidade sugerida para compra** e quanto ainda falta para alcançar o objetivo

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas** – manipulação de dados
- **Requests / APIs financeiras** – captura de preços de mercado
- **JSON** – persistência da carteira

---

## 🚀 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/manager-contribution.git
   cd manager-contribution
   ```

2. Instale as dependencias
   ```bash
   git install pandas urllib3 grequests requests
   ```
