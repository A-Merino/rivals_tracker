import json
import os
from glob import glob
from model import Player

def save_match(data):
    outfile = f'./data/matches/{data.keys()[0]}'

    if os.path.exists(outfile):
        return

    with open (outfile, 'w') as f:
        json.dump(data, f)
    

def get_key():
    with open('api_key.txt', "r") as file:
        key = file.readline()
        file.close()

    headers = {
        "x-api-key": key
    }

    return headers


def get_our_info():
    with open('uids.json', 'r') as f:
        data = json.load(f)
        f.close()

    return data


def load_info():
    files = glob('./data/players/*')

    if len(files) == 0:
        return None

    players = []

    for file in files:
        with open(file, 'r') as f:

            data = json.load(f)
            f.close()

        players.append(Player().loadData(data))

    return players


def init_players(p_data):
    things = []

    for player in p_data:
        things.append(Player(player['uid'], player['user']))
    return things


def isAMatch(match_id):
    # List comprehension is pretty neat:
    #   - get all files
    #   - get rid of .json part
    matches = [m.split('.')[0] for m in glob('./data/matches/*')]

    if match_id in matches:
        return True
    return False



