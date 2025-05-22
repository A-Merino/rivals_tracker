import json
import os
from glob import glob
from model import Player

def save_match(data):
    outfile = f'./data/matches/{list(data.keys())[0]}.json'

    if os.path.exists(outfile):
        return

    with open (outfile, 'w') as f:
        json.dump(data, f)
        f.close()
    print(f"Saved: {outfile}")

def get_key():
    with open('api_key.txt', "r") as file:
        key = file.readline()
        file.close()

    headers = {
        "x-api-key": key
    }

    return headers


def list_uids(data):
    return [p['uid'] for p in data]


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


def getPlayer(line, uid):
    for p in line:
        
        if uid == p.uid:
            return p
    raise "Error: ID is not in list, which should not be possible" 


def save_data(players):
    for player in players:
       player.saveData() 


def get_all_matches():
    return glob('./data/matches/*')

