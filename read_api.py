import requests

url = "https://apiv3.apifootball.com/?action=get_events"
API_KEY= "11d7031956ed5e022833ae33ce1ddd3334f8644b7b63e10e20f0785444d91d0c"
PARAMS = {"from": "2022-08-11", "to": "2022-11-11","APIkey":API_KEY}

r = requests.get(url=url, params=PARAMS)

# extracting data in json format
data = r.json()
print(data)
