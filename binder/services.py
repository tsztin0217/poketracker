import requests
from django.conf import settings


def fetch_card_data(query):
    url = f'https://api.pokemontcg.io/v2/cards?q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Return the response as a JSON object
    else:
        return None
    
def get_card_details_from_api(card_id):
    url = f"https://api.pokemontcg.io/v2/cards/{card_id}"
    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        return data['data']  
    return None
