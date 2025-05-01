import requests
from django.conf import settings


def fetch_card_data(query):
    url = f'https://api.pokemontcg.io/v2/cards?q=name:{query}*'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


    
def get_card_details_from_api(card_id):
    url = f"https://api.pokemontcg.io/v2/cards/{card_id}"
    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        return data['data'] 
    return None 

