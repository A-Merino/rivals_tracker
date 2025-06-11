import requests
import json
import parse as ps
import time

def getMatch(match_id, header):
    # Example
    # url = "https://marvelrivalsapi.com/api/v1/match/5521362_1744593397_1201286_11001_11"

    # Create request and recieve response
    response = requests.get('/'.join(("https://marvelrivalsapi.com/api/v1/match", match_id)), headers=header)

    # If all good
    if response.status_code == 200:
        # Check if its the stupid autochess mode or not
        if response.json()['match_details']['game_mode']['game_mode_id'] == 4:
            return 0

        # PROBABLY CHECK FOR DOOM MATCH TOO

        # If its quick match or comp modes then parse
        return ps.parseMatch(response.json())
    else:
        # if error print
        print(f"Error {response.status_code}")
        
        # if rate limit error
        if response.status_code == 429:
            # wait one minute, then retry
            print("Cooling rate limit")
            time.sleep(60)
            print(f"Retrying match {match_id}")
            return getMatch(match_id, header)
        elif response.status_code == 504:
            print('Server error')
            time.sleep(60)
            print(f"Retrying match {match_id}")
            return getMatch(match_id, header)



def getHistory(player, header, mod=False, season='0', page='1', retTotal=False):

    # Example
    # url = "https://marvelrivalsapi.com/api/v1/player/KingDerp_/match-history"

    # Create url
    url= '/'.join(("https://marvelrivalsapi.com/api/v2/player", player, "match-history"))

    # Certain parameter modifying here
    params = f"?season={season}&page={page}"
    
    if mod:
        url += params
    
    # Create request url and save response
    response = requests.get(url, headers=header)

    # All good, parse it
    if response.status_code == 200:
        if retTotal:
            return ps.parseHistory(response.json()), response.json()['pagination']['total_pages']

        return ps.parseHistory(response.json())
    else:
        # If not print error
        print(f"Error {response.status_code}")
        # If it is a rate limit error
        if response.status_code == 429:
            # wait one minute and try again
            print("Cooling rate limit")
            time.sleep(60)
            print(f"Retrying history of {player}")
            return getHistory(player, header, retTotal)  # Recursion!!!
        elif response.status_code == 504:
            print('Server error')
            time.sleep(60)
            print(f"Retrying history of {player}")
            return getHistory(player, header, retTotal)  # Recursion!!!




def updateAccount(player, header):

    # Example
    # url = "https://marvelrivalsapi.com/api/v1/player/KingDerp_/update"

    # Create the url and get response
    response = requests.get('/'.join(("https://marvelrivalsapi.com/api/v1/player", player, "update")), headers=header)

    # If all good then account is updated and we move on
    if response.status_code == 200:
        print(response.json()['message'])
    # If not good (most likely less than 30 minute update) then print and still move on
    else:
        print(f"Error {response.status_code}: {response.text}")
