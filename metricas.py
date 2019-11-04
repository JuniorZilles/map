import matplotlib.pyplot as plt
import numpy as np


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
    precision_at = [1,]

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
            avg_prec +=  count / (retrived.index(ret) + 1)
            
    return avg_prec / count


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
    recall_at = [0,]

    for ret in retrived:
        if ret in relevant:
            count += 1

        recall_at.append(count / len(relevant))

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
    return np.trapz(y, x, axis = -1)


def plot_curve(precision_list: list, recall_list: list):
    """
    Plot das curvas e cálculo de suas áreas.
    """  
    # Definições do plot
    plt.title("Recall x Precision")  
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.ylim(top = 1.05, bottom = 0)
    plt.xlim(left = 0, right = 1.05)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    # Plot da curva Recall x Precision e calculo da 
    # área abaixo da mesma
    prec = np.array(precision_list)
    rec = np.array(recall_list)
    plt.plot(rec, prec, color = "blue", label = "Completa")
    area_rp_1 = calculate_area(prec, rec)

    # Plot da curva interpolada e cálculo da
    # área abaixo da mesma
    precision_interpolated = np.array(interpolate(precision_list))
    recall_interpolated = np.array(recall_list)
    plt.plot(recall_interpolated, precision_interpolated, 
        color = "red", label = "Interpolada")
    area_rp_2 = calculate_area(precision_interpolated, recall_interpolated)

    # Plot da curva interpolada em 11 pontos e
    # cálculo da área abaixo da mesma
    recall_at = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    precision_at = np.array(interpolate_at(list(recall_interpolated), 
        list(precision_interpolated), list(recall_at)))
    plt.plot(recall_at, precision_at, 
        color = "green", label = "Interpolada 11 pts")
    area_rp_3 = calculate_area(precision_at, recall_at)

    print("\n### Área abaixo das curvas")
    print("-> Completa: ", area_rp_1)
    print("-> Interpolada: ", area_rp_2)
    print("-> Interpolada em 11 pontos: ", area_rp_3)

    plt.legend()
    plt.show()