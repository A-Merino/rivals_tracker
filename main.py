import requests
import model
import utils
import grabData as gd
import parse
import json

def main():

    # get our key and set header for api calls
    header = utils.get_key()

    # get uids and handles
    us = utils.get_our_info()

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
            mid = match.keys()[0]
            
            # check if the match is already collected
            if utils.isAMatch(mid):
                continue
            
            # if not...

            # get the match from the match history
            match_data = gd.getMatch(mid, header)

            # for each player in the match
            for stats in match_data[mid]['players']:
                # Check if its one of us

                # then add to olddata
                pass



def test():    
    # print(gd.getHistory("172351051",utils.get_key()))
    #print(gd.getMatch("5518698_1744684424_1170273_11001_11", utils.get_key()))
#test()
main()