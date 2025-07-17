import time
import os
import json
import numpy as np


character_ids = {
    0: None,
    1011: 'Hulk',
    1014: 'Punisher',
    1015: 'Storm',
    1016: 'Loki',
    1017: 'HumanTorch',
    1018: 'DrStrange',
    1020: 'Mantis',
    1021: 'Hawkeye',
    1022: 'CaptainAmerica',
    1023: 'RocketRaccoon',
    1024: 'Hela',
    1025: 'CloakDagger',
    1026: 'BlackPanther',
    1027: 'Groot',
    1028: 'Ultron',
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
    1054: 'Phoenix'
}


class Player:

    def __init__(self, uid=None, user=None):
        self.uid = uid
        self.handle = user
        self.heroes = { 'Mantis': Hero('Mantis', "Support"),
                        'Jeff': Hero('Jeff', "Support"),
                        'AdamWarlock': Hero('Adam Warlock', "Support"), 
                        'CloakDagger': Hero('Cloak Dagger', "Support"),
                        'InvisibleWoman': Hero('Invisible Woman', "Support"),
                        'Loki': Hero('Loki', "Support"),
                        'LunaSnow': Hero('Luna Snow', "Support"),
                        'RocketRaccoon': Hero('Rocket Raccoon', "Support"),
                        'Ultron': Hero('Ultron', "Support"),
                        'Wolverine': Hero('Wolverine', "Duelist"),
                        'WinterSoldier': Hero('Winter Soldier', "Duelist"),
                        'Punisher': Hero('Punisher', "Duelist"),
                        'Storm': Hero('Storm', "Duelist"),
                        'StarLord': Hero('Star-Lord', "Duelist"),
                        'SquirrelGirl': Hero('Squirrel Girl', "Duelist"),
                        'SpiderMan': Hero('Spider Man', "Duelist"),
                        'ScarletWitch': Hero('Scarlet Witch', "Duelist"),
                        'Psylocke': Hero('Psylocke', "Duelist"),
                        'Namor': Hero('Namor', "Duelist"),
                        'MoonKnight': Hero('Moon Knight', "Duelist"),
                        'MisterFantastic': Hero('Mister Fantastic', "Duelist"),
                        'Magik': Hero('Magik', "Duelist"),
                        'IronMan': Hero('Iron Man', "Duelist"),
                        'IronFist': Hero('Iron Fist', "Duelist"),
                        'HumanTorch': Hero('Human Torch', "Duelist"),
                        'Hela': Hero('Hela', "Duelist"),
                        'Hawkeye': Hero('Hawkeye', "Duelist"),
                        'BlackWidow': Hero('Black Widow', "Duelist"),
                        'BlackPanther': Hero('Black Panther', "Duelist"),
                        'Phoenix': Hero('Pheonix', "Duelist"),
                        'Venom': Hero('Venom', "Vanguard"),
                        'Thor': Hero('Thor', "Vanguard"),
                        'TheThing': Hero('The Thing', "Vanguard"),
                        'PeniParker': Hero('Peni Parker', "Vanguard"),
                        'Magneto': Hero('Magneto', "Vanguard"),
                        'Hulk': Hero('Hulk', "Vanguard"),
                        'Groot': Hero('Groot', "Vanguard"),
                        'EmmaFrost': Hero('Emma Frost', "Vanguard"),
                        'DrStrange': Hero('Dr Strange', "Vanguard"),
                        'CaptainAmerica': Hero('Captain America', "Vanguard")
                        }
        self.matches = []
        self.maps = {}

    def addMatch(self, match):
        self.matches.append(match)

    def checkMatch(self, match_id):
        if match_id in self.matches:
            return True
        return False



    def updateHero(self, hero, data, match_id, damage=None):

        self.heroes[hero].updateData(data, match_id, damage)


    def saveData(self):
        outfile = f'./data/players/{self.handle}.json'
        data = {}
        data['uid'] = self.uid
        data['handle'] = self.handle
        data['matches'] = self.matches

        data['heroes'] = {}

        for char, stats in zip(self.heroes.keys(), self.heroes.values()):
            data['heroes'][char] = stats.dictify()

        with open(outfile, "w") as file:
            json.dump(data, file)
            file.close()


    def loadData(self, data):

        self.uid = data["uid"]
        self.handle = data["handle"]
        self.matches = data['matches']

        for char, stats in zip(self.heroes.keys(), self.heroes.values()):
            # The Player object's Character object is equal to
            # the Character object with loaded data from the datafile object with same character name
            self.heroes[char] = stats.loadData(data['heroes'][char])
            # ^^ I think thats what this is doing

        # Why do I have to return self when I'm updating data
        # I guess its because It has the new data?  
        return self


    def collected(self, match_id):

        if match_id in self.matches:
            return True
        return False


class Hero:

    def __init__(self, nnn, ttt):
        self.name = nnn
        self.type = ttt
        self.damage = 0
        self.heals = 0
        self.taken = 0
        self.final_hits = 0
        self.deaths = 0
        self.kos = 0
        self.time = 0
        self.assists = 0
        self.mvps = 0
        self.svps = 0
        self.matches = []

    def __str__(self):
        return str(self.name)

    def updateData(self, data, match_id, damage):
        if damage is not None:
            self.damage += damage['damage']
            self.heals += damage['heals']
            self.taken += damage['taken']
        self.time += data['time']
        self.deaths += data['deaths']
        self.kos += data['kos']
        self.assists += data['assists']
        self.matches.append(match_id)
        #self.final_hits += data['final_hits']
        #self.mvps += data['mvps']
        #self.svps += data['svps']


    def loadData(self, data):
        self.name = data['name']
        self.type = data['type']
        self.damage = data['damage']
        self.heals = data['heals']
        self.taken = data['taken']
        self.time = data['time']
        self.deaths = data['deaths']
        self.kos = data['kos']
        self.assists = data['assists']
        self.matches = data['matches']
        self.mvps = data['mvps']
        self.svps = data['svps']
        #self.final_hits = data['final_hits']

        return self

    def dictify(self):
        data = {}
        data['name'] = self.name
        data['type'] = self.type
        data['damage'] = self.damage
        data['heals'] = self.heals
        data['taken'] = self.taken
        data['time'] = self.time
        data['deaths'] = self.deaths
        data['kos'] = self.kos
        data['assists'] = self.assists
        data['matches'] = self.matches
        data['mvps'] = self.mvps
        data['svps'] = self.svps
        #data['final_hits'] = self.final_hits
        return data




class Mantis(Hero):

    def _init__(self, f, s):
        self.name = "Mantis"
        self.type = "Support"
        super().__init__(self, self.name, self.type)


class Jeff(Hero):

    def _init__(self):
        self.name = "Jeff"
        self.type = "Support"
        super().__init__(self, self.name, self.type)


class AdamWarlock(Hero):

    def _init__(self):
        self.name = "Adam Warlock"
        self.type = "Support"
        super().__init__(self, self.name, self.type)


class CloakDagger(Hero):

    def _init__(self):
        self.name = "Cloak & Dagger"
        self.type = "Support"
        super().__init__(self, self.name, self.type)


class InvisibleWoman(Hero):

    def _init__(self):
        self.name = "Invisible Woman"
        self.type = "Support"
        super().__init__(self, self.name, self.type)

class Loki(Hero):

    def _init__(self):
        self.name = "Loki"
        self.type = "Support"
        super().__init__(self, self.name, self.type)

class Ultron(Hero):

    def _init__(self):
        self.name = "Ultron"
        self.type = "Support"
        super().__init__(self, self.name, self.type)

class LunaSnow(Hero):

    def _init__(self):
        self.name = "Luna Snow"
        self.type = "Support"
        super().__init__(self, self.name, self.type)

class RocketRaccoon(Hero):

    def _init__(self):
        self.name = "Rocket Raccoon"
        self.type = "Support"
        super().__init__(self, self.name, self.type)

class Wolverine(Hero):

    def _init__(self):
        self.name = "Wolverine"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class WinterSoldier(Hero):

    def _init__(self):
        self.name = "Winter Soldier"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Punisher(Hero):

    def _init__(self):
        self.name = "Punisher"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Storm(Hero):

    def _init__(self):
        self.name = "Storm"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class StarLord(Hero):

    def _init__(self):
        self.name = "Star-Lord"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class SquirrelGirl(Hero):

    def _init__(self):
        self.name = "Squirrel Girl"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class SpiderMan(Hero):

    def _init__(self):
        self.name = "Spider-Man"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class ScarletWitch(Hero):

    def _init__(self):
        self.name = "Scarlet Witch"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Psylocke(Hero):

    def _init__(self):
        self.name = "Psylocke"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Namor(Hero):

    def _init__(self):
        self.name = "Namor"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class MoonKnight(Hero):

    def _init__(self):
        self.name = "Moon Knight"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class MisterFantastic(Hero):

    def _init__(self):
        self.name = "Mister Fantastic"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Magik(Hero):

    def _init__(self):
        self.name = "Magik"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class IronMan(Hero):

    def _init__(self):
        self.name = "Iron Man"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class IronFist(Hero):

    def _init__(self):
        self.name = "Iron Fist"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class HumanTorch(Hero):

    def _init__(self):
        self.name = "Human Torch"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Hela(Hero):

    def _init__(self):
        self.name = "Hela"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Hawkeye(Hero):

    def _init__(self):
        self.name = "Hawkeye"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class BlackWidow(Hero):

    def _init__(self):
        self.name = "Black Widow"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class BlackPanther(Hero):

    def _init__(self):
        self.name = "Black Panther"
        self.type = "Duelist"
        super().__init__(self, self.name, self.type)

class Jeff(Hero):

    def _init__(self):
        self.name = "Jeff"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class CaptainAmerica(Hero):

    def _init__(self):
        self.name = "Captain America"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class DrStrange(Hero):

    def _init__(self):
        self.name = "Doctor Strange"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class EmmaFrost(Hero):

    def _init__(self):
        self.name = "Emma Frost"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class Groot(Hero):

    def _init__(self):
        self.name = "Groot"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class Hulk(Hero):

    def _init__(self):
        self.name = "Hulk"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class Magneto(Hero):

    def _init__(self):
        self.name = "Magneto"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class PeniParker(Hero):

    def _init__(self):
        self.name = "Peni Parker"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class TheThing(Hero):

    def _init__(self):
        self.name = "The Thing"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class Thor(Hero):

    def _init__(self):
        self.name = "Thor"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)

class Venom(Hero):

    def _init__(self):
        self.name = "Venom"
        self.type = "Vanguard"
        super().__init__(self, self.name, self.type)
