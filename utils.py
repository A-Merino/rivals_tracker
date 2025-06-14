import json
import os
from glob import glob
from model import Player
from model import character_ids as cid


def save_match(data):
    '''
        Function that saves the match data to file

        Parameters
        ----------
        data: dictionary, json, Object
            The match data that is being saved

        Returns
        -------
        None. Adds a file to the './data/matches' directory
    '''
    # Create the path
    outfile = f'./data/matches/{list(data.keys())[0]}.json'

    # If already exists then don't save
    # if os.path.exists(outfile):
    #     return

    # if not then save as json
    with open(outfile, 'w') as f:
        json.dump(data, f)
        f.close()
    print(f"Saved: {outfile}")


# Return my api_key in the header format
def get_key():
    with open('api_key.txt', "r") as file:
        key = file.readline()
        file.close()

    headers = {
        "x-api-key": key
    }

    return headers


# Get a list of uids from a list of dictionaries
def list_uids(data):
    return [p['uid'] for p in data]


def get_our_info():
    # Get Rivals ID for ourselves
    with open('uids.json', 'r') as f:
        data = json.load(f)
        f.close()

    return data


def load_info():
    '''
        Function that loads all player data from
        json files in the 'data/players' directory
    '''

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
    '''
        Function that initializes player models given player data

        Parameters
        ----------
        p_data: list, array-like
            The player data that is wanting to be added to a
            player model

        Returns
        -------
        all_players: list, array-like
            The list of Player objects from model.py with data
            from the parameter set

    '''

    all_players = []
    # Create a player model for each piece of data given
    for player in p_data:
        all_players.append(Player(player['uid'], player['user']))
    return all_players


# Check if we have a match already
def isAMatch(match_id):
    # List comprehension is pretty neat:
    #   - get all files
    #   - get rid of .json part
    matches = [m.split('.')[0] for m in glob('./data/matches/*')]

    # If we already have match we don't need it again
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


def match_compiler():
    '''
        Function that compiles every match in dataset into
        one file

        Parameters
        ----------
        None

        Returns
        -------
        None

        It will create a file called 'all_matches.json' in the
        project root directory

    '''

    # Grab all matches
    matches = get_all_matches()

    # Put all data into an array
    data = load_matches(matches)

    # Create/overwrite file and dump json data
    with open('all_matches.json', 'w') as file:
        json.dump(data, file)
        file.close()


def load_matches(matches):
    '''
        Function that loads matches into a list

        Parameters
        ----------
        matches: list, array-like of Path
            A list of filepaths that contain match
            data

        Returns
        -------
        md: list, array-like
            A list of objects, json, dictionaries that contain
            match data from a single match of rivals 
    '''

    md = []

    # Go through each match
    for match in matches:
        with open(match, 'r') as mat:
            md.append(json.load(mat)) # append json data to list
            mat.close()

    return md


def update_mvps():
    '''
        Function that updates the mvp count for
        each player, and each character as well
        (assuming that they only used one character
        in said round)

    Parameters
    ----------
    None

    Returns
    -------
    None. Updates the 'players.json' file
    '''

    # Get matches and players
    matches = get_all_matches()
    data = load_matches(matches)
    players = load_info()

    # This is so silly
    uids = list_uids(get_our_info())

    for match in data:
        # Why doesn't dict_keys return as list???
        match = match[list(match.keys())[0]]

        # Save 
        mvp = match['mvp']
        svp = match['svp']

        if mvp in uids:
            char = match['mvp_char']
        elif svp in uids:
            char = match['svp_char']
        else:
            continue
        print(char)
# update_mvps()

def rewtir():

    # vv = None

    # with open ('all_matches.json', 'r') as file:
    #     vv = json.load(file)

    # for match in vv:
    #     save_match(match)


    data = load_matches(get_all_matches())
    for m in data:
        print(m)
        
        for b in m[list(m.keys())[0]]['players']:
            uid = list(b.keys())[0]
            b[int(uid)] = b[uid]
            del b[uid]
        # save_match(m)

rewtir()