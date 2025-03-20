def valor_aplicado(loop):
    for i in range(len(loop)):
        preco = loop.loc[i, "preco"]
        quantidade = loop.loc[i, "quantidade"]

        loop.loc[i, "capital aplicado"] = preco * quantidade


def montante_do_tipo(montante, texto):
    porcentagemDoTipo = float(input(texto))
    montanteDoTipo = montante * (porcentagemDoTipo / 100)
    return montanteDoTipo

def soma_valor_aplicado(loop):
    soma = 0
    for i in loop:
        soma += i["capitalAplicado"]

    return soma


def quantidade_final(montante, loop):
    from math import ceil
    qnt_final = []
    
    for i in range(len(loop)):
        preco = loop.loc[i, "preco"]
        porcentagemIdeal = loop.loc[i, "porcentagem ideal"]
        nome = loop.loc[i, "nome"]
        
        totalAtivo = round(montante * (porcentagemIdeal/100), 3)
        qnt = ceil((totalAtivo) / preco)
    
        print(f"No final dos aportes, você terá {qnt} do ativo {nome[:-3]}, totalizando cerca de R$ {totalAtivo}")
        
    
        
    



def aporte(montanteDoTipo, loop, tempo):
    infoAporte = []

    for i in range(len(loop)):
        capitalAplicado = loop.loc[i, "capital aplicado"]
        porcentagemIdeal = loop.loc[i, "porcentagem ideal"]
        preco = loop.loc[i, "preco"]
        nome = loop.loc[i, "nome"]

        aporteIdeal = ((montanteDoTipo * (porcentagemIdeal/100)) - capitalAplicado)/tempo

        quantidade = int(max(1, aporteIdeal/preco))
        aporteReal = preco * quantidade 
        
        infoAporte.append([nome, quantidade, aporteIdeal, aporteReal])

    return infoAporte
