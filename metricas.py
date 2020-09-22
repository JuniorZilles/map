import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd


def precision(retrived: list, relevant: list):
    """
    Retorna a medida de precisão.
    """
    if len(retrived) == 0:
        return 0

    relevant_retrieved = [r for r in retrived if r in relevant]

    return len(relevant_retrieved) / len(retrived)


def precision_at_k(retrived: list, relevant: list):
    """
    Retorna uma lista contendo a precisão para os documentos
    recuperados.
    """
    count = 0.0
    precision_at = [1, ]

    for ret in retrived:
        if ret in relevant:
            count += 1

        precision_at.append(count / (retrived.index(ret) + 1))

    return precision_at


def average_precision(retrived: list, relevant: list):
    """
    Retorna o Average Precision.
    """
    count = 0
    avg_prec = 0

    for ret in retrived:
        if ret in relevant:
            count += 1
            avg_prec += count / (retrived.index(ret) + 1)

    return avg_prec / (count if count != 0 else 1)


def recall(retrived: list, relevant: list):
    """
    Retorna a medida de recall.
    """
    if len(relevant) == 0:
        return 0

    relevant_retrieved = [r for r in retrived if r in relevant]

    return len(relevant_retrieved) / len(relevant)


def recall_at_k(retrived: list, relevant: list):
    """
    Retorna uma lista contendo a medida de recall 
    para cada documento recuperado.
    """
    count = 0.0
    recall_at = [0, ]

    for ret in retrived:
        if ret in relevant:
            count += 1

        recall_at.append(count / (len(relevant) if len(relevant) != 0 else 1))

    return recall_at


def f_measure(retrived: list, relevant: list):
    """
    Retorna a medida F Measure.
    """
    precision_v = precision(retrived, relevant)
    recall_v = recall(retrived, relevant)
    if recall_v == 0 or precision_v == 0:
        return 0

    return (2 * precision_v * recall_v) / (precision_v + recall_v)


def find_next_nearest(array: list, value):
    """
    Retorna o elemento do array com valor mais próximo de value.
    """
    n = [(i - value) for i in array]
    idx = n.index(min([i for i in n if i >= 0])) if max(n) > 0 else None

    if idx is None:
        return None

    return array[idx]


def interpolate_at(recall_list, precision_list, recall_at):
    """
    Retorna uma nova lista de "precision" com mais proximidade
    aos "recall" de cada recall_at.
    """
    precision_interpolated = []

    for r in recall_at:
        nearest = find_next_nearest(recall_list, r)
        if nearest is None:
            precision_interpolated.append(0.0)
        else:
            location = recall_list.index(nearest)
            precision_interpolated.append(precision_list[location])

    return precision_interpolated


def interpolate(precision_list: list):
    """
    Retorna uma nova lista de "precision" com os maiores valores da 
    lista antiga a partir da posição pos.
    """
    precision_interpolated = []

    for pos in range(len(precision_list)):
        max_value = max(precision_list[pos:])
        precision_interpolated.append(max_value)

    return precision_interpolated


def calculate_area(y, x):
    """
    Retorna a área abaixo da curva pelo método trapezoidal.
    """
    return np.trapz(y, x, axis=-1)


def plot_curve(precision_list: list, recall_list: list):
    """
    Plot das curvas e cálculo de suas áreas.
    """
    # Definições do plot
    plt.title("Recall x Precision")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.ylim(top=1.05, bottom=0)
    plt.xlim(left=0, right=1.05)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    # Plot da curva Recall x Precision e calculo da
    # área abaixo da mesma
    prec = np.array(precision_list)
    rec = np.array(recall_list)
    plt.plot(rec, prec, color="blue", label="Completa")
    area_rp_1 = calculate_area(prec, rec)

    # Plot da curva interpolada e cálculo da
    # área abaixo da mesma
    precision_interpolated = np.array(interpolate(precision_list))
    recall_interpolated = np.array(recall_list)
    plt.plot(recall_interpolated, precision_interpolated,
             color="red", label="Interpolada")
    area_rp_2 = calculate_area(precision_interpolated, recall_interpolated)

    # Plot da curva interpolada em 11 pontos e
    # cálculo da área abaixo da mesma
    recall_at = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    precision_at = np.array(interpolate_at(list(recall_interpolated),
                                           list(precision_interpolated), list(recall_at)))
    plt.plot(recall_at, precision_at,
             color="green", label="Interpolada 11 pts")
    area_rp_3 = calculate_area(precision_at, recall_at)

    print("\n### Área abaixo das curvas")
    print("-> Completa: ", area_rp_1)
    print("-> Interpolada: ", area_rp_2)
    print("-> Interpolada em 11 pontos: ", area_rp_3)

    plt.legend()
    plt.show()


def getLabel(value: str):
    if value == 'eq':
        return 'equals'
    elif value == 'lk':
        return 'like'
    elif value == 'ws':
        return 'word_similarity'
    elif value == 's':
        return 'similarity'


def plot_curve_j1(precision_list: list, recall_list: list, method: str):
    """
    Plot das curvas e cálculo de suas áreas.
    """
    mlabel = getLabel(method)
    points = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # Definições do plot
    plt.title("Recall x Precision")
    plt.xlabel("Recall/100")
    plt.ylabel("Precision/100")
    plt.ylim(top=1.05, bottom=0)
    plt.xlim(left=0, right=1.05)
    plt.xticks(points)
    plt.yticks(points)

    # Plot da curva interpolada em 11 pontos e
    # cálculo da área abaixo da mesma
    recall_at = np.array(points)
    precision_interpolated = np.array(interpolate(precision_list))
    recall_interpolated = np.array(recall_list)
    precision_at = np.array(interpolate_at(list(recall_interpolated),
                                           list(precision_interpolated), list(recall_at)))
    plt.plot(recall_at, precision_at,
             color="green", label=mlabel)
    area_rp_3 = calculate_area(precision_at, recall_at)

    print("\n### Área abaixo das curvas")
    print("->", area_rp_3)

    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_'+method+'.png', dpi=1280, orientation='portrait')
    plt.show()


def plot_curve_j2(precision_list_1: list, recall_list_1: list, precision_list_2: list, recall_list_2: list, method_1: str, method_2: str):
    """
    Plot das curvas e cálculo de suas áreas.
    """
    mlabel_1 = getLabel(method_1)
    mlabel_2 = getLabel(method_2)
    points = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # Definições do plot
    plt.title("Recall x Precision")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim(top=1.05, bottom=0)
    plt.xlim(left=0, right=1.05)
    plt.xticks(points)
    plt.yticks(points)

    # Plot da curva interpolada em 11 pontos e
    # cálculo da área abaixo da mesma
    recall_at_1 = np.array(points)
    precision_interpolated_1 = np.array(interpolate(precision_list_1))
    recall_interpolated_1 = np.array(recall_list_1)
    precision_at_1 = np.array(interpolate_at(list(recall_interpolated_1),
                                             list(precision_interpolated_1), list(recall_at_1)))
    plt.plot(recall_at_1, precision_at_1,
             color="green", label=mlabel_1)
    area_rp_1 = calculate_area(precision_at_1, recall_at_1)

    print("\n### Área abaixo da curva(1)")
    print("->", area_rp_1)

    recall_at_2 = np.array(points)
    precision_interpolated_2 = np.array(interpolate(precision_list_2))
    recall_interpolated_2 = np.array(recall_list_2)
    precision_at_2 = np.array(interpolate_at(list(recall_interpolated_2),
                                             list(precision_interpolated_2), list(recall_at_2)))
    area_rp_2 = calculate_area(precision_at_2, recall_at_2)
    plt.plot(recall_at_2, precision_at_2, '--',
             color="red", label=mlabel_2)

    print("\n### Área abaixo da curva(2)")
    print("->", area_rp_2)

    plt.legend()
    plt.grid(True)
    plt.savefig('grafico.png', dpi=1280, orientation='portrait')
    plt.show()


def plot_curve_j3(info_list: list):
    """
    Plot das curvas e cálculo de suas áreas.
    """
    points = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # Definições do plot
    plt.title("Recall x Precision")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim(top=1.05, bottom=0)
    plt.xlim(left=0, right=1.05)
    plt.xticks(points)
    plt.yticks(points)

    # Plot da curva interpolada em 11 pontos e
    # cálculo da área abaixo da mesma
    pos = 0
    colors = ['green', 'red', 'blue', 'orange', 'brown',
              'grey', 'yellow',  'purple', 'black', 'gold', 'silver']
    line = [
        (0, (1, 1)),
        (0, (5, 10)),
        (0, (5, 5)),
        (0, (5, 1)),
        (0, (3, 10, 1, 10)),
        (0, (3, 5, 1, 5)),
        (0, (3, 1, 1, 1)),
        (0, (3, 5, 1, 5, 1, 5)),
        (0, (3, 10, 1, 10, 1, 10)),
        (0, (3, 1, 1, 1, 1, 1)),
        (0, (1, 10))]
    for a in info_list:
        recall_at = np.array(points)
        precision_interpolated = np.array(interpolate(a.media_precision))
        recall_interpolated = np.array(a.media_recal)
        precision_at = np.array(interpolate_at(list(recall_interpolated),
                                               list(precision_interpolated), list(recall_at)))
        plt.plot(recall_at, precision_at, linestyle=line[pos],
                 color=colors[pos], label=a.method)
        area_rp_1 = calculate_area(precision_at, recall_at)

        print("\n### Área abaixo da curva: ", a.method)
        print("->", area_rp_1)
        pos += 1

    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_tse.png', dpi=1280, orientation='portrait')
    plt.show()


def histogram_plot(np_hist: list):
    print(np_hist)
    plt.figure(figsize=[10, 8])
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Score', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('Frequência', fontsize=15)
    plt.title('Histograma frequência por score', fontsize=15)
    plt.hist(np_hist, bins=100, label="Scores",
             color='green', edgecolor='black')
    plt.legend()
    plt.grid(True)
    plt.show()


def histogram_plot_v2(x: list, y: list):
    print(x)
    print(y)
    plt.figure(figsize=[10, 8])
    pos = np.arange(len(x))
    plt.bar(x, y, color='#6A5ACD')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Score', fontsize=15)
    plt.ylabel('Frequência', fontsize=15)
    plt.title('Histograma frequência por score', fontsize=15)
    plt.show()


def histogram_plot_v3(np_hist: list):
    print(np_hist)
    plt.figure(figsize=[10, 10])
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Score', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('Frequência', fontsize=15)
    plt.title('Histograma frequência por score', fontsize=15)
    plt.hist(np_hist, bins=100, label=['Score', "Interações"],
             color=['blue', 'red'], edgecolor='black', stacked=True)
    # plt.hist(np_hist, bins=10, label=['Score', "Interações"],
    #         color=['blue', 'red'], histtype='step', stacked=True)
    # plt.hist(np_hist[1], bins=10, label="Interações",
    #         color='blue', edgecolor='black', log=True)
    # plt.hist(np_hist[0], bins=10, label="Scores",
    #         color='red', edgecolor='black', log=True)
    #plt.axvline(10, color="orange")
    plt.legend()
    plt.grid(True)
    plt.show()


def histogram_plot_v4(np_hist: list):
    print(np_hist)
    df = pd.DataFrame({
        'Scores': np_hist[0],
        'Interações': np_hist[1]
    })
    plt.figure(figsize=[10, 10])
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Score', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylabel('Frequência', fontsize=15)
    plt.title('Histograma frequência por score', fontsize=15)
    df.plot(kind='bar', stacked=True)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_curve_histo(x: list, y: list):
    # Definições do plot
    maxx = round(max(x)) + 10
    maxy = round(max(y)) + 10
    qtdx = maxx/20
    qtdy = maxy/20
    xpoints = [x*qtdx for x in range(0, 20)]
    ypoints = [y*qtdy for y in range(0, 20)]
    plt.style.use('fivethirtyeight')
    plt.title("Curva frequência por score")
    plt.xlabel("Score")
    plt.ylabel("Frequência")
    #plt.ylim(top=1.05, bottom=0)
    #plt.xlim(left=0, right=1.05)
    # plt.xticks(xpoints)
    # plt.yticks(ypoints)
    print(x)
    print(y)
    plt.plot(x, y,
             color="green", label='Curva de frequencias')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.savefig('grafico_'+method+'.png', dpi=1280, orientation='portrait')
    plt.show()
