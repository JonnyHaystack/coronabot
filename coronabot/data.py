import requests

API_ROOT = "https://corona.lmao.ninja"


def get_global_cases():
    response = requests.get(f"{API_ROOT}/all").json()

    updated = response["updated"]

    data = {
        "Confirmed": response["cases"],
        "Current": response["active"],
        "Deaths": response["deaths"],
        "Recovered": response["recovered"],
    }

    return data, updated


def get_country_cases(country_name):
    response = requests.get(f"{API_ROOT}/countries/{country_name}").json()

    updated = response["updated"]

    country_info = {
        "country_name": response["country"],
        "country_code": response["countryInfo"]["iso2"].lower(),
    }

    data = {
        "Confirmed": {
            "total": response["cases"],
            "new": response["todayCases"],
        },
        "Current": response["active"],
        "Deaths": {
            "total": response["deaths"],
            "new": response["todayDeaths"],
        },
        "Recovered": response["recovered"],
        "Cases PMP": response["casesPerOneMillion"],
        "Deaths PMP": response["deathsPerOneMillion"],
    }

    return data, country_info, updated
