import time
import os
import json
import numpy as np



class Player:

    def __init__(self, uid=None, user=None):
        self.uid = uid
        self.handle = user
        self.heroes = { 'Mantis': Mantis(),
                        'Jeff': Jeff(),
                        'AdamWarlock': AdamWarlock(), 
                        'CloakDagger': CloakDagger(),
                        'InvisibleWoman': InvisibleWoman(),
                        'Loki': Loki(),
                        'LunaSnow': LunaSnow(),
                        'RocketRaccoon': RocketRaccoon(),
                        'Wolverine': Wolverine(),
                        'WinterSoldier': WinterSoldier(),
                        'Punisher': Punisher(),
                        'Storm': Storm(),
                        'StarLord': StarLord(),
                        'SquirrelGirl': SquirrelGirl(),
                        'SpiderMan': SpiderMan(),
                        'ScarletWitch': ScarletWitch(),
                        'Psylocke': Psylocke(),
                        'Namor': Namor(),
                        'MoonKnight': MoonKnight(),
                        'MisterFantastic': MisterFantastic(),
                        'Magik': Magik(),
                        'IronMan': IronMan(),
                        'IronFist': IronFist(),
                        'HumanTorch': HumanTorch(),
                        'Hela': Hela(),
                        'Hawkeye': Hawkeye(),
                        'BlackWidow': BlackWidow(),
                        'BlackPanther': BlackPanther(),
                        'Venom': Venom(),
                        'Thor': Thor(),
                        'TheThing': TheThing(),
                        'PeniParker': PeniParker(),
                        'Magneto': Magneto(),
                        'Hulk': Hulk(),
                        'Groot': Groot(),
                        'EmmaFrost': EmmaFrost(),
                        'DrStrange': DrStrange(),
                        'CaptainAmerica': CaptainAmerica()
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

    def __init__(self, name=None):
        self.name = name
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

    def _init__(self):
        super().__init__("Mantis")
        self.type = "Support"


class Jeff(Hero):

    def _init__(self):
        super().__init__("Jeff")
        self.type = "Support"


class AdamWarlock(Hero):

    def _init__(self):
        super().__init__("Adam Warlock")
        self.type = "Support"


class CloakDagger(Hero):

    def _init__(self):
        super().__init__("Cloak & Dagger")
        self.type = "Support"


class InvisibleWoman(Hero):

    def _init__(self):
        super().__init__("Invisible Woman")
        self.type = "Support"

class Loki(Hero):

    def _init__(self):
        super().__init__("Loki")
        self.type = "Support"

class LunaSnow(Hero):

    def _init__(self):
        super().__init__("Luna Snow")
        self.type = "Support"

class RocketRaccoon(Hero):

    def _init__(self):
        super().__init__("Rocket Raccoon")
        self.type = "Support"

class Wolverine(Hero):

    def _init__(self):
        super().__init__("Wolverine")
        self.type = "Duelist"

class WinterSoldier(Hero):

    def _init__(self):
        super().__init__("Winter Soldier")
        self.type = "Duelist"

class Punisher(Hero):

    def _init__(self):
        super().__init__("Punisher")
        self.type = "Duelist"

class Storm(Hero):

    def _init__(self):
        super().__init__("Storm")
        self.type = "Duelist"

class StarLord(Hero):

    def _init__(self):
        super().__init__("Star-Lord")
        self.type = "Duelist"

class SquirrelGirl(Hero):

    def _init__(self):
        super().__init__("Squirrel Girl")
        self.type = "Duelist"

class SpiderMan(Hero):

    def _init__(self):
        super().__init__("Spider-Man")
        self.type = "Duelist"

class ScarletWitch(Hero):

    def _init__(self):
        super().__init__("Scarlet Witch")
        self.type = "Duelist"

class Psylocke(Hero):

    def _init__(self):
        super().__init__("Psylocke")
        self.type = "Duelist"

class Namor(Hero):

    def _init__(self):
        super().__init__("Namor")
        self.type = "Duelist"

class MoonKnight(Hero):

    def _init__(self):
        super().__init__("Moon Knight")
        self.type = "Duelist"

class MisterFantastic(Hero):

    def _init__(self):
        super().__init__("Mister Fantastic")
        self.type = "Duelist"

class Magik(Hero):

    def _init__(self):
        super().__init__("Magik")
        self.type = "Duelist"

class IronMan(Hero):

    def _init__(self):
        super().__init__("Iron Man")
        self.type = "Duelist"

class IronFist(Hero):

    def _init__(self):
        super().__init__("Iron Fist")
        self.type = "Duelist"

class HumanTorch(Hero):

    def _init__(self):
        super().__init__("Human Torch")
        self.type = "Duelist"

class Hela(Hero):

    def _init__(self):
        super().__init__("Hela")
        self.type = "Duelist"

class Hawkeye(Hero):

    def _init__(self):
        super().__init__("Hawkeye")
        self.type = "Duelist"

class BlackWidow(Hero):

    def _init__(self):
        super().__init__("Black Widow")
        self.type = "Duelist"

class BlackPanther(Hero):

    def _init__(self):
        super().__init__("Black Panther")
        self.type = "Duelist"

class Jeff(Hero):

    def _init__(self):
        super().__init__("Jeff")
        self.type = "Vanguard"

class CaptainAmerica(Hero):

    def _init__(self):
        super().__init__("Captain America")
        self.type = "Vanguard"

class DrStrange(Hero):

    def _init__(self):
        super().__init__("Doctor Strange")
        self.type = "Vanguard"

class EmmaFrost(Hero):

    def _init__(self):
        super().__init__("Emma Frost")
        self.type = "Vanguard"

class Groot(Hero):

    def _init__(self):
        super().__init__("Groot")
        self.type = "Vanguard"

class Hulk(Hero):

    def _init__(self):
        super().__init__("Hulk")
        self.type = "Vanguard"

class Magneto(Hero):

    def _init__(self):
        super().__init__("Magneto")
        self.type = "Vanguard"

class PeniParker(Hero):

    def _init__(self):
        super().__init__("Peni Parker")
        self.type = "Vanguard"

class TheThing(Hero):

    def _init__(self):
        super().__init__("The Thing")
        self.type = "Vanguard"

class Thor(Hero):

    def _init__(self):
        super().__init__("Thor")
        self.type = "Vanguard"

class Venom(Hero):

    def _init__(self):
        super().__init__("Venom")
        self.type = "Vanguard"
