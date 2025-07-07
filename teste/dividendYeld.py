from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def dados_gerais(soup):
    """
    Extrai dados da estrutura tipo _card (ex: "P/VP": "0,79")
    """
    dados = {}
    for card in soup.select("div._card"):
        titulo_tag = card.select_one("._card-header span[title]")
        valor_tag = card.select_one("._card-body span")
        if titulo_tag and valor_tag:
            chave = titulo_tag.get("title").strip()
            valor = valor_tag.text.strip()
            dados[chave] = valor
    return dados


def dados_empresa(soup):
    """
    Extrai dados da estrutura tipo cell (ex: "CNPJ": "15.576.907/0001-70")
    """
    dados = {}
    for cell in soup.select("div.cell"):
        titulo_tag = cell.select_one(".name")
        valor_tag = cell.select_one(".value span")
        if titulo_tag and valor_tag:
            chave = titulo_tag.get_text(strip=True)
            valor = valor_tag.get_text(strip=True)
            dados[chave] = valor
    return dados


def dados_yeld(soup):
    """
    Extrai dados da estrutura tipo content--info--item (ex: "YIELD 1 MÊS": "1,07%")
    """
    dados = {}
    for item in soup.select(".content--info--item"):
        titulo_tag = item.select_one(".content--info--item--title")
        valor_tag = item.select_one(".content--info--item--value")
        if titulo_tag and valor_tag:
            chave = titulo_tag.get_text(strip=True)
            valor = valor_tag.get_text(strip=True)
            dados[chave] = valor
    return dados


def get_dy(url, ticker):
    url = url + ticker
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar {url} - Código: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    dados = dados_gerais(soup)
    dividendYeld = dados.get('P/VP')  # Você pode trocar a chave dependendo da informação desejada
    return dividendYeld