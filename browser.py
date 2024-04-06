import requests

radio_url = "http://de1.api.radio-browser.info/json"

def search_radio(query: str) -> list:
    params = {"order": "name", "reverse": False, "hidebroken": True, "limit": 20}
    data = requests.get(radio_url+"/stations/byname/"+query, params=params).json()
    return data

def get_radio(uuid: str):
    url = radio_url+"/stations/byuuid/"+uuid
    data = requests.get(url).json()
    return data

def radios_by(method: str, offset: int, limit: int) -> list:
    if method not in ["topvote", "topclick", "lastclick"]:
        return []
    url = radio_url+"/stations/"+method
    params = {"offset": offset, "limit": limit}
    data = requests.get(url, params=params).json()
    return data

if __name__ == "__main__":
    from const import *
    uuid = "ddc49aac-eb85-11e9-a96c-52543be04c81"
    print(get_radio(uuid))
    """
    data = search_radio("FIP")
    print(data)
    print(radios_by("lastclick", 0, 5))
    """
