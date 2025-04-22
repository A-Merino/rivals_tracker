import requests
import model
import utils
import grabData
import parse


key = ''

with open('api_key.txt', "r") as file:
    key = file.readline()
    file.close()


# url = "https://marvelrivalsapi.com/api/v1/player/KingDerp_/match-history"

url = "https://marvelrivalsapi.com/api/v1/match/5521362_1744593397_1201286_11001_11"

headers = {
    "x-api-key": key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")