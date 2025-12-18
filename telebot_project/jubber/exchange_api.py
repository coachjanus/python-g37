import re
import requests
import json

# URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

from jubber.config import PRIVATBANK_API_URL

# def load_exchange():
#     return json.loads(requests.get(URL).text)

# Add error handling for requests.get(), including exception handling for timeouts and invalid responses. Use a try-except block with informative error messages.
# def load_exchange():
#     try:
#         response = requests.get(PRIVATBANK_API_URL, timeout=10)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Error fetching exchange data: {e}")
#         return []
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
def load_exchange():
    try:
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3,
                        status_forcelist=[500, 502, 503, 504])
        session.mount(PRIVATBANK_API_URL, HTTPAdapter(max_retries=retries))
        response = session.get(PRIVATBANK_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching exchange data: {e}")
        return None

# def get_exchange(ccy_key):
#     for exc in load_exchange():
#         if ccy_key == exc['ccy']:
#             return exc
#     return False

# def get_exchanges(ccy_pattern):
#     result = []
#     ccy_pattern = re.escape(ccy_pattern) + '.*'

#     for exc in load_exchange():
#         if re.match(ccy_pattern, exc['ccy'], re.IGNORECASE) is not None:
#             result.append(exc)
#     return result

def get_exchange(ccy_key):
    for exc in load_exchange():
        if ccy_key == exc['ccy']:
            return exc
    return None

def get_exchanges(ccy_pattern):
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'

    for exc in load_exchange():
        if re.match(ccy_pattern, exc['ccy'], re.IGNORECASE):
            result.append(exc)
    return result
