import requests  # requisições http
import json

def get_request_as_json(url):
    response = requests.get(url)
    dados = json.loads(response.text)
    return dados