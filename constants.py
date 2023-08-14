from enum import Enum
TEMPLATE_CHARACTERS_FILE_PATH = "data/template_characters.json"
PLAYERS_DATA_FILE_PATH = "data/players.json"
ID_FILE_PATH = "data/ids.json"
BANNERS_FILE_PATH = "data/banners.json"
EQUIPMENT_FILE_PATH = "data/equipments.json"
SCENES_FILE_PATH = "data/story.json"
BATTLES_FILE_PATH = "data/battles.json"

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