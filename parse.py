char_id = {
    1000: 'Mantis',
    1047: 'Jeff',
    1000: 'AdamWarlock',
    1025: 'CloakDagger',
    1050: 'InvisibleWoman',
    1000: 'Loki',
    1031: 'LunaSnow',
    1023: 'RocketRaccoon',
    1000: 'Wolverine',
    1000: 'WinterSoldier',
    1014: 'Punisher',
    1000: 'Storm',
    1000: 'StarLord',
    1000: 'SquirrelGirl',
    1000: 'SpiderMan',
    1000: 'ScarletWitch',
    1000: 'Psylocke',
    1045: 'Namor',
    1030: 'MoonKnight',
    1000: 'MisterFantastic',
    1000: 'Magik',
    1034: 'IronMan',
    1000: 'IronFist',
    1000: 'HumanTorch',
    1000: 'Hela',
    1000: 'Hawkeye',
    1033: 'BlackWidow',
    1000: 'BlackPanther',
    1000: 'Venom',
    1000: 'Thor',
    1051: 'TheThing',
    1000: 'PeniParker',
    1000: 'Magneto',
    1011: 'Hulk',
    1027: 'Groot',
    1053: 'EmmaFrost',
    1018: 'DrStrange',
    1000: 'CaptainAmerica'
}


def parseMatch(data):
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

