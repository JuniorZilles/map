def media_avg(lista:list):
    soma = 0.0
    qtd = len(lista)
    for b in range(0, qtd):
        soma += float(lista[b].avg)
    return soma/qtd

def media_avg2(lista:list):
    soma = 0.0
    qtd = len(lista)
    for b in range(0, qtd):
        soma += float(lista[b])
    return soma/qtd

def obter_prec(lista:list):
    media = []
    for a in range(0, len(lista[0].precision_list)):
        soma = 0.0
        qtd = len(lista)
        for b in range(0, qtd):
            if len(lista[b].recal_list) > a:
                soma += lista[b].precision_list[a]
        media.append(soma/qtd)
    return media

def obter_recal(lista:list):
    media = []
    for a in range(0, len(lista[0].recal_list)):
        soma = 0.0
        qtd = len(lista)
        for b in range(0, qtd):
            if len(lista[b].recal_list) > a:
                soma += lista[b].recal_list[a]
        media.append(soma/qtd)
    return media