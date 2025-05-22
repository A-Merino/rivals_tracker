import json
import os
from glob import glob
from model import Player

def save_match(data):
    # Create the path 
    outfile = f'./data/matches/{list(data.keys())[0]}.json'

    # If already exists then don't save
    if os.path.exists(outfile):
        return

    # if not then save as json
    with open (outfile, 'w') as f:
        json.dump(data, f)
        f.close()
    print(f"Saved: {outfile}")

# Return my api_key
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
    # Get Rivals ID for ourselves 
    with open('uids.json', 'r') as f:
        data = json.load(f)
        f.close()

    return data


def load_info():
    # Get saved player data
    files = glob('./data/players/*')

    # If none then return nothing
    if len(files) == 0:
        return None

    players = []

    # Go through files and load into player model
    for file in files:
        with open(file, 'r') as f:

            data = json.load(f)
            f.close()

        players.append(Player().loadData(data))

    return players


def init_players(p_data):
    things = []
    # Create a player model for each piece of data given
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

# Check if the uid is in a match
def getPlayer(line, uid):
    for p in line:        
        if uid == p.uid:
            return p
    raise "Error: ID is not in list, which should not be possible" 

# Save data for all players given
def save_data(players):
    for player in players:
       player.saveData() 

# Gets all matches from data folder
def get_all_matches():
    return glob('./data/matches/*')

