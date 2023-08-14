from enum import Enum
import os

platform_environment = os.environ.get('ENVIRONMENT')

if platform_environment == 'pythonanywhere':
    BASE_DIR = 'Novas_expanse/data'
else:
    BASE_DIR = 'data/'


TEMPLATE_CHARACTERS_FILE_PATH = BASE_DIR + "template_characters.json"
PLAYERS_DATA_FILE_PATH =  BASE_DIR + "players.json"
ID_FILE_PATH =  BASE_DIR + "ids.json"
BANNERS_FILE_PATH =  BASE_DIR + "banners.json"
EQUIPMENT_FILE_PATH =  BASE_DIR + "equipments.json"
SCENES_FILE_PATH =  BASE_DIR + "story.json"
BATTLES_FILE_PATH =  BASE_DIR + "battles.json"

class Aspect(Enum):
    TIME = "Time"
    SPACE = "Space"
    ASTRAL = "Astral"
    VOID = "Void"
    MATTER = "Matter"
    LIGHT = "Light"
    MIND = "Mind"
    LIFE = "Life"
    DEATH = "Death"
    ENERGY = "Energy"


class Stat(Enum):
    HEALTH = 0
    ATTACK_PHYSICAL = 1
    ATTACK_ASPECT = 2
    DEFENCE_PHYSICAL = 3
    RESISTANCE_ASPECT = 4
    RECOVERY = 5
    AGILITY = 6
    CRITICAL_CHANCE = 7
    CRITICAL_DAMAGE = 8

class AttackType(Enum):
    PHYSICAL = "Physical"
    ASPECT = "Aspect"

class Rarity(Enum):
    STELLA_I = "Stella I"
    STELLA_II = "Stella II"
    STELLA_III = "Stella III"

class EquipmentType(Enum):
    HAT = "Hat"
    CLOTHING = "Clothing"
    ACCESSORY = "Accessory"
    WEAPON = "Weapon"

class EquipmentSlot(Enum):
    HAT = "Hat"
    CLOTHING = "Clothing"
    ACCESSORY_1 = "Accessory_1"
    ACCESSORY_2 = "Accessory_2"

class SummonableType(Enum):
    FEATURED = 1
    BEST_DROP = 2
    GOOD_DROP = 3
    NORMAL_DROP = 4