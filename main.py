import requests
import model
import utils
import grabData as gd
import parse as ps
import json
import time
import datetime

def main():

    # get our key and set header for api calls
    header = utils.get_key()

    # get uids and handles
    us = utils.get_our_info()

    uids = utils.list_uids(us)

    # Get already saved data
    old_data = utils.load_info()

    # if no files, then init new models
    if old_data is None:
        old_data = utils.init_players(us)
        
    
    # go through each of us and collect data
    for player in us:

        # Start with match history
        matches = gd.getHistory(player['uid'], header)
        saver(matches)
            
        # After we get data then we update the player

        '''
            There is a 30 minute lock after updating the player so
            we call this after grabbing the data so we do not get
            stuck in a 'data loop' we will call this program every 32
            minutes after completion to account for this and give some leeway
        '''
        gd.updateAccount(player['uid'], header)
    loader()


def getAll():
    # get our key and set header for api calls
    header = utils.get_key()

    # get uids and handles
    us = utils.get_our_info()

    uids = utils.list_uids(us)

    # Get already saved data
    old_data = utils.load_info()
    
    seasons = [
        # '0'
        # ,'1.0'
        # ,'1.5'
        # ,'2.0'
        '2.5'
    ]

    # if no files, then init new models
    if old_data is None:
        old_data = utils.init_players(us)
    
    # go through each of us and collect data
    for player in us:

        for season in seasons:

            matches, pages = gd.getHistory(player['uid'], header, True, season, '1', True)
            saver(matches)
            # Start with match history
            for p in range(2, pages+1):
                matches = gd.getHistory(player['uid'], header, True, season, str(p))
                saver(matches)

            
        # After we get data then we update the player

        '''
            There is a 30 minute lock after updating the player so
            we call this after grabbing the data so we do not get
            stuck in a 'data loop' we will call this program every 32
            minutes after completion to account for this and give some leeway
        '''
        gd.updateAccount(player['uid'], header)
    loader()


def saver(matches):
    for match in matches:
        # there is only one key in match variables
        mid = list(match.keys())[0]
        
        # check if the match is already collected
        if utils.isAMatch(mid):
            print('Already Collected')
            continue  # Skip
        
        # if not...

        # get the match from the match history
        match_data = gd.getMatch(mid, utils.get_key())

        # Save the match data to file if its a normal mode
        if match_data != 0:
            utils.save_match(match_data)
            



def test():
    # print(model.Player().heroes['Mantis'])
    # utils.match_compiler()
    utils.save_match(gd.getMatch('6713347_1740250568_681_11001_10', utils.get_key()))

# test()



def loader():
    '''
        Loads all data from already saved matches
    '''


    # get our key and set header for api calls
    header = utils.get_key()

    # get uids and handles
    us = utils.get_our_info()

    uids = utils.list_uids(us)

    # Get already saved data
    old_data = utils.load_info()

    # if no files, then init new models
    if old_data is None:
        old_data = utils.init_players(us)

    # get matches
    matches = utils.get_all_matches()

    # Go through each match
    for match in matches:
        with open(match, 'r') as f:
            data = json.load(f)
            f.close()

        # Get match id
        mid = list(data.keys())[0]

        # for each player in the match
        for stats in data[mid]['players']:
            # Get id from current player
            cur_id = list(stats.keys())[0]
            
            # Check if its one of us
            if cur_id in uids:
                # if so then get the player model
                cur_player = utils.getPlayer(old_data, cur_id)
                # update
                if not cur_player.checkMatch(mid):
                    ps.updatePlayer(cur_player, stats, mid)

    utils.save_data(old_data)
    utils.update_mvps()
    utils.match_compiler()

getAll()
# main()
# loader()