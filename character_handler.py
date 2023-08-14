from data_manager import *
from constants import TEMPLATE_CHARACTERS_FILE_PATH





def create_template_character(character):
    data = load_data(TEMPLATE_CHARACTERS_FILE_PATH)
    if character["name"] not in data:
        data[character["name"]] = character
        save_data(TEMPLATE_CHARACTERS_FILE_PATH, data)
    

def edit_template_character(character_name, new_character_data):
    # Load data file
    # Find character
    # Update character data
    # Save data file
    data = load_data(TEMPLATE_CHARACTERS_FILE_PATH)
    if character_name in data:
        data[character_name] = new_character_data
        save_data(TEMPLATE_CHARACTERS_FILE_PATH, data)

def delete_template_character(character_name):
    data = load_data(TEMPLATE_CHARACTERS_FILE_PATH)
    if character_name in data:
        data[character_name] = None
        save_data(TEMPLATE_CHARACTERS_FILE_PATH, data)

def get_template_character(character_name):
    data = load_data(TEMPLATE_CHARACTERS_FILE_PATH)
    if character_name in data:
        return data[character_name]

def get_template_characters():
    data = load_data(TEMPLATE_CHARACTERS_FILE_PATH)
    characters = []
    for char in data:
        characters.append(data[char])
    return characters


def create_playable_character(character_name, aspect, level=1, unlocked_skins=["Nebula_Wisp.png"], unlocked_skills=[], guardians_path=[]):
    id = get_unique_id()
    character_template = get_template_character(character_name)
    if aspect not in character_template["possible_aspects"]: return None
    for skin in unlocked_skins:
        if skin not in character_template["skins"]: return None
    for skill in unlocked_skills:
        if skill not in character_template["skills"]: return None
    return playable_character(id, character_name,aspect=aspect, level=level, xp=0, equipment={}, unlocked_skins=unlocked_skins, active_skin=unlocked_skins[0], unlocked_skills=unlocked_skills, active_skills=[], guardians_path=guardians_path)


def get_stats_of_character(playable_character):
    template = get_template_character(playable_character["name"])

    stats = []
    level = playable_character["level"]
    base_stats = template["base_stats"]
    growth_rate = template["growth_rate"]

    for i in range(9):
        stats.append(base_stats[i] + (level - 1) * growth_rate[i])
    return stats

