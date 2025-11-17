import logging
import requests
from django.conf import settings
from requests.exceptions import RequestException, Timeout
from urllib.parse import quote_plus
from functools import lru_cache
import time

logger = logging.getLogger(__name__)

# Simple cache: store results for 1 hour (3600 seconds)
_cache = {}
_cache_expiry = {}


def _build_headers():
    headers = {}
    api_key = getattr(settings, 'POKEMON_TCG_API_KEY', None)
    if api_key:
        headers['X-Api-Key'] = api_key
    return headers


def fetch_card_data(query, timeout=30):
    """Fetch cards that match `query` from the Pokemon TCG API.
    
    Returns the parsed JSON on success, or None on failure.
    Uses a short timeout and logs errors instead of raising so views can
    return a friendly 500/empty result without blocking gunicorn workers.
    Caches results for 1 hour to avoid slow API calls on repeat searches.
    """
    # Check cache first
    cache_key = f"cards_{query}"
    if cache_key in _cache:
        expiry = _cache_expiry.get(cache_key, 0)
        if time.time() < expiry:
            logger.info('Returning cached result for query=%s', query)
            return _cache[cache_key]
        else:
            # Cache expired, remove it
            del _cache[cache_key]
            del _cache_expiry[cache_key]
    
    try:
        encoded = quote_plus(query)
        url = f'https://api.pokemontcg.io/v2/cards?q=name:{encoded}*'
        headers = _build_headers()
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            # Cache the result for 1 hour
            _cache[cache_key] = data
            _cache_expiry[cache_key] = time.time() + 3600
            logger.info('Cached card data for query=%s', query)
            return data
        else:
            logger.warning('Pokemon TCG API returned status %d for query=%s', resp.status_code, query)
            return None
    except Timeout:
        logger.warning('Pokemon TCG API request timed out for query=%s', query)
    except RequestException as e:
        logger.exception('Error fetching card data for query=%s: %s', query, e)
    return None


def get_card_details_from_api(card_id, timeout=30):
    try:
        url = f"https://api.pokemontcg.io/v2/cards/{quote_plus(card_id)}"
        headers = _build_headers()
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            if 'data' in data:
                return data['data']
        else:
            logger.warning('Pokemon TCG API returned status %d for card_id=%s', resp.status_code, card_id)
    except Timeout:
        logger.warning('Pokemon TCG API request timed out for card_id=%s', card_id)
    except RequestException as e:
        logger.exception('Error fetching card details for card_id=%s: %s', card_id, e)
    return None

