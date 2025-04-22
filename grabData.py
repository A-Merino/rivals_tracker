import requests
import json
import parse as ps


def getMatch(match_id, header):

    # url = "https://marvelrivalsapi.com/api/v1/match/5521362_1744593397_1201286_11001_11"


    response = requests.get('/'.join(("https://marvelrivalsapi.com/api/v1/match", match_id)), headers=header)

    if response.status_code == 200:
        return ps.parseMatch(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")


def getHistory(player, header):
    # url = "https://marvelrivalsapi.com/api/v1/player/KingDerp_/match-history"

    response = requests.get('/'.join(("https://marvelrivalsapi.com/api/v1/player", player, "match-history")), headers=header)

    if response.status_code == 200:
        return ps.parseHistory(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")



def updateAccount(player, header):
    # url = "https://marvelrivalsapi.com/api/v1/player/KingDerp_/update"

    response = requests.get('/'.join(("https://marvelrivalsapi.com/api/v1/player", player, "update")), headers=header)

    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(f"Error {response.status_code}: {response.text}")
