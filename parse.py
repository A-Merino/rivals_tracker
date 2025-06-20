from model import character_ids as char_id

def parseHistory(data):
    '''
        Given a match history query (Ex: test_history.json), parse all
        the matches in the list and return as a list of matches
    '''
    data = data['match_history']
    games = []
    for match in data:
        games.append(
            {match['match_uid']: {

                'map': match['match_map_id'],
                'length': match['match_play_duration'],
                'season': match['match_season'],
                'winner': match['match_winner_side'],
                'mvp': match['mvp_uid'],
                'svp': match['svp_uid'],
                'match_score': match['score_info'],
                'team': match['match_player']['camp'],
                'br': {
                    'diff': match['match_player']['score_info']['add_score'],
                    'rating': match['match_player']['score_info']['new_score']
                },
                'disconnected': match['match_player']['disconnected']
            }
            })

    return games


def parseMatch(data):
    '''
        Given a dictionary/json format, parse out all the data in
        a specific way and return the parsed dictionary
    '''
    data = data['match_details']
    parsed = {
        data['match_uid']:{

        'uids': [],
        'game_mode': data['game_mode']['game_mode_name'],
        'replay': data['replay_id'],
        'mvp': str(data['mvp_uid']),
        'mvp_char': char_id[data['mvp_hero_id']],
        'svp': str(data['svp_uid']),
        'svp_char': char_id[data['svp_hero_id']]
        }
    }
    
    # create list for the players of the given match
    parsed[data['match_uid']]['players'] = []

    for player in data['match_players']:
        parsed[data['match_uid']]['uids'].append(player['player_uid'])
        temp = {str(player['player_uid']): {

            'handle': player['nick_name'],
            'team': player['camp'],
            'last': char_id[player['cur_hero_id']],
            'won': player['is_win'],
            'kos': player['kills'],
            'deaths': player['deaths'],
            'assists': player['assists'],
            'total_damage': player['total_hero_damage'],
            'total_taken': player['total_damage_taken'],
            'total_heal': player['total_hero_heal']
            }
        }

        temp[player['player_uid']]['badges'] = []
        if player['badges'] is not None:
            temp[player['player_uid']]['badges'] = player['badges']

        temp[player['player_uid']]['heroes'] = []
        for hero in player['player_heroes']:
            temp[player['player_uid']]['heroes'].append({
                'hero': char_id[hero['hero_id']],
                'time': hero['play_time'],
                'kos': hero['kills'],
                'deaths': hero['deaths'],
                'assists': hero['assists'],
                'acc': hero['session_hit_rate']
            })

        parsed[data['match_uid']]['players'].append(temp)

    return parsed


def updatePlayer(player, stats, match_id):
    player.addMatch(match_id)
    stats = stats[list(stats.keys())[0]]
    if len(stats['heroes']) == 1:
        player.updateHero(stats['heroes'][0]['hero'], stats['heroes'][0], match_id,{'damage':stats['total_damage'],'taken':stats['total_taken'],'heals':stats['total_heal']})
    else:
        for hero in stats['heroes']:
            player.updateHero(hero['hero'], hero, match_id)

    # return player
