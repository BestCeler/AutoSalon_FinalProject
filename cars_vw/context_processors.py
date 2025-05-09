import datetime
import os
import requests
from django.conf import settings
from django.core.cache import cache


API_KEY = os.getenv("EXCHANGERATESAPI_KEY")

def season(request):
    month = datetime.datetime.now().month
    if month in (12, 1, 2):
        season = "winter"
    elif month in (3, 4, 5):
        season = "spring"
    elif month in (6, 7, 8):
        season = "summer"
    else:
        season = "autumn"
    return {'season': season}


def exchange_rate(request):
    rate = cache.get('exchange_rate') # we take the course from the cache
    if rate is not None:
        return {'exchange_rate': rate}

    try:
        url = f"https://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base=EUR&symbols=CZK"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"].get("CZK")

        if rate:
            cache.set('exchange_rate', rate, timeout=3600) # cache for 1 hour (3600 seconds)
        return {"exchange_rate": rate}
    except Exception:
        return {"exchange_rate": None}
