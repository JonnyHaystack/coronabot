import requests

API_ROOT = "https://corona.lmao.ninja"


def get_global_cases():
    response = requests.get(f"{API_ROOT}/all").json()
    return response

def get_country_cases(country_name):
    response = requests.get(f"{API_ROOT}/countries/{country_name}").json()
    return response
