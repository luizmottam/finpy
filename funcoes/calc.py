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
