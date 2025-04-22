char_id = {
    1011: 'Hulk',
    1014: 'Punisher',
    1015: 'Storm',
    1016: 'Loki',
    1017: 'HumanTorch',
    1018: 'DrStrange',
    1020: 'Mantis',
    1021: 'Hawkeye',
    1022: 'CaptainAmerica'
    1023: 'RocketRaccoon',
    1024: 'Hela',
    1025: 'CloakDagger',
    1026: 'BlackPanther',
    1027: 'Groot',
    1029: 'Magik',
    1030: 'MoonKnight',
    1031: 'LunaSnow',
    1032: 'SquirrelGirl',
    1033: 'BlackWidow',
    1034: 'IronMan',
    1035: 'Venom',
    1036: 'SpiderMan',
    1037: 'Magneto',
    1038: 'ScarletWitch',
    1039: 'Thor',
    1040: 'MisterFantastic',
    1041: 'WinterSoldier',
    1042: 'PeniParker',
    1043: 'StarLord',
    1045: 'Namor',
    1046: 'AdamWarlock',
    1047: 'Jeff',
    1048: 'Psylocke',
    1049: 'Wolverine',
    1050: 'InvisibleWoman',
    1051: 'TheThing',
    1052: 'IronFist',
    1053: 'EmmaFrost',
}


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
        'mvp': data['mvp_uid'],
        'mvp_char': char_id[data['mvp_hero_id']],
        'svp': data['svp_uid'],
        'svp_char': char_id[data['svp_hero_id']]
        }
    }
    
    parsed[data['match_uid']'players'] = []

    for player in data['match_players']:
        parsed[data['match_uid']]['uids'].append(player['player_uid'])
        temp = {player['player_uid']: {

            'handle': player['nick_name'],
            'team': player['camp'],
            'last': char_id[player['cur_hero_id']],
            'won': player['is_win'],
            'kos': player['kills'],
            'deaths': player['deaths'],
            'assists': player['assists'],
            'total_damage': player['total_hero_damage'],
            'total_taken': player['total_hero_heal'],
            'total_heal': player['total_damage_taken']
            }
        }

        temp[player['player_uid']]['badges'] = []
        if player['badges'] is not None:
            temp['badges'] = player['badges']

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
                'match_score': {
                    0: match['score_info']['0'],
                    1: match['score_info']['1']
                },
                'team': match['match_player']['camp'],
                'br': {
                    'diff': match['match_player']['score_info']['add_score'],
                    'rating': match['match_player']['score_info']['new_score']
                },
                'disconnected': match['match_player']['disconnected']
            }
            })

    return games

