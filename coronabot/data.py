import requests

API_ROOT = "https://coronavirus-19-api.herokuapp.com"


def get_global_cases():
    response = requests.get(f"{API_ROOT}/all").json()
    return response

def get_country_cases(country_name):
    response = requests.get(f"{API_ROOT}/countries/{country_name}").json()
    return response
