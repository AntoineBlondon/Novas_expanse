import os
import json
import uuid
from constants import ID_FILE_PATH, SummonableType

def load_data(file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if not os.path.isfile(file):
        with open(file, 'w') as f:
            json.dump({}, f)
            return {}
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def get_unique_id():
    existing_ids = []
    try:
        with open(ID_FILE_PATH, 'r') as file:
            existing_ids = file.read().splitlines()
    except FileNotFoundError:
        pass

    new_id = uuid.uuid4().hex

    while new_id in existing_ids:
        new_id = uuid.uuid4().hex

    existing_ids.append(new_id)

    with open(ID_FILE_PATH, 'w') as file:
        file.write('\n'.join(existing_ids))

    return new_id


def intToRoman(num):
 
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]
 
    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
 
    ans = (thousands + hundreds +
           tens + ones)
 
    return ans


def playable_character(unique_id, name, aspect, level, xp, equipment, unlocked_skins, active_skin, unlocked_skills, active_skills, guardians_path):
    return {
        "unique_id": unique_id,
        "name": name,
        "aspect": aspect,
        "level": level,
        "xp": xp,
        "equipment": equipment,
        "unlocked_skins": unlocked_skins,
        "active_skin": active_skin,
        "unlocked_skills": unlocked_skills,
        "active_skills": active_skills,
        "guardians_path": guardians_path,
    }

def template_character(name, world, rarity, possible_aspects, attack_pattern, story, skins, base_stats, growth_rate, guardian, skills):
    return {
        "name": name,
        "world": world,
        "rarity": rarity,
        "possible_aspects": possible_aspects,
        "attack_pattern": attack_pattern,
        "story": story,
        "skins": skins,
        "base_stats": base_stats,
        "growth_rate": growth_rate,
        "guardian": guardian,
        "skills": skills
    }

def Equipment(name, rarity, set, type, description, skin, stats, skills=[]):
    return {
        "name": name,
        "rarity": rarity,
        "set": set,
        "type": type,
        "description": description,
        "skin": skin,
        "stats": stats,
        "skills": skills,
    }



def Banner(name, description, image, cost):
    return {
        "name": name,
        "description": description,
        "image": image,
        "drops": {str(category): [] for category in SummonableType},
        "rates": {str(category) + "_rate": 0 for category in SummonableType},
        "cost": cost
    }


def Starlight(amount):
    return {
        "type": "starlight",
        "amount": amount
    }

