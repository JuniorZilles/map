import json

class model:
    def __init__(self, termo_bd:str, termo_busca:str, qtd_retornado:int, avg:float, posicoes:list, precision_list:list, recal_list:list):
        self.termo_bd = termo_bd
        self.termo_busca = termo_busca
        self.qtd_retornado = qtd_retornado
        self.avg = avg
        self.posicoes = posicoes
        self.precision_list = precision_list
        self.recal_list = recal_list
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class info:
    def __init__(self, m_avg:float, m_rec_list:list, m_prec_list:list, base_list:list):
        self.media_avg = m_avg
        self.media_recal = m_rec_list
        self.media_precision = m_prec_list
        self.base = base_list

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)