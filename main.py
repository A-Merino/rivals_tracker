import requests
import model
import utils
import grabData as gd
import parse as ps
import json
import time

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
        
        for match in matches:
            # there is only one key in match variables
            mid = list(match.keys())[0]
            
            # check if the match is already collected
            if utils.isAMatch(mid):
                print('Already Collected')
                continue  # Skip
            
            # if not...

            # get the match from the match history
            match_data = gd.getMatch(mid, header)

            # Save the match data to file
            utils.save_match(match_data)

            
        # After we get data then we update the player

        '''
            There is a 30 minute lock after updating the player so
            we call this after grabbing the data so we do not get
            stuck in a 'data loop' we will call this program every 32
            minutes after completion to account for this and give some leeway
        '''
        gd.updateAccount(player['uid'], header)




def test():    
    # print(gd.getHistory("172351051",utils.get_key()))
    #print(gd.getMatch("5518698_1744684424_1170273_11001_11", utils.get_key()))
    #gd.updateAccount("1139596293", utils.get_key())
    d = {'get':2}
    print(list(d.keys())[0])
    for i in range(9):
        i = 0
        print(i)


test()
# main()



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

    matches = utils.get_all_matches()

    for match in matches:
        with open(match, 'r') as f:
            data = json.load(f)
            f.close()

        mid = list(data.keys())[0]

        # for each player in the match
        for stats in data[mid]['players']:
            cur_id = list(stats.keys())[0] 
            
            # Check if its one of us
            if cur_id in uids:
                print(f"Matching uid: {cur_id}")
                # if so then get the player model
                cur_player = utils.getPlayer(old_data, cur_id)
                # update
                if not cur_player.checkMatch(mid):
                    ps.updatePlayer(cur_player, stats, mid)

    utils.save_data(old_data)


# loader()