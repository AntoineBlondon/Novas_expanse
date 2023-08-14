from data_manager import *
from constants import PLAYERS_DATA_FILE_PATH

def new_player():
    return {"characters": [], "inventory": {"starlight": 0, "equipment": [] }, "current_battle": {}}

def get_players():
    data = load_data(PLAYERS_DATA_FILE_PATH)
    players = []
    for player in data:
        players.append(player)
    return players

def get_characters_of_player(player):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player in data:
        data[player] = new_player()
        save_data(PLAYERS_DATA_FILE_PATH, data)
    return data[player]["characters"] 

def set_characters_of_player(player, characters):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player in data:
        data[player]["characters"] = characters
        save_data(PLAYERS_DATA_FILE_PATH, data)
    
def edit_character_of_player(player, unique_id, new_character):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player in data:
        characters = get_characters_of_player(player)
        for i, c in enumerate(characters):
            if c["unique_id"] == unique_id:
                characters.remove(c)
                characters.insert(i, new_character)
        set_characters_of_player(player, characters)
    
def get_character_of_player(player, unique_id):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player in data:
        characters = get_characters_of_player(player)
        for c in characters:
            if c["unique_id"] == unique_id:
                return c


def add_character_to_player(player, playable_character):
    characters = get_characters_of_player(player)
    characters.append(playable_character)
    set_characters_of_player(player, characters)


def remove_character_from_player(player, unique_id):
    characters = get_characters_of_player(player)
    for char in characters:
        if char["unique_id"] == unique_id:
            characters.remove(char)
    set_characters_of_player(player, characters)


def get_player(player):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player in data:
        return data[player]


def get_equipment_of_player(player):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player in data:
        data[player] = new_player()
        save_data(PLAYERS_DATA_FILE_PATH, data)
    return data[player]["inventory"]["equipment"] 

def set_equipment_of_player(player, equipments):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player in data:
        data[player]["inventory"]["equipment"] = equipments
        save_data(PLAYERS_DATA_FILE_PATH, data)

def add_equipment_to_player(player, equipment):
    current_equipments = get_equipment_of_player(player)
    current_equipments.append(equipment)
    set_equipment_of_player(player, current_equipments)

def remove_equipment_from_player(player, equipment):
    current_equipments = get_equipment_of_player(player)
    current_equipments.remove(equipment)
    set_equipment_of_player(player, current_equipments)


def get_current_battle(player_name):
    return get_player(player_name)["current_battle"]

def set_current_battle(player_name, battle_inventory):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if player_name in data:
        data[player_name]["current_battle"] = battle_inventory
    
    save_data(PLAYERS_DATA_FILE_PATH, data)

def get_starlight_of_player(player_name):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
        save_data(PLAYERS_DATA_FILE_PATH, data)
    return int(data[player_name]["inventory"]["starlight"])


def set_starlight_of_player(player_name, amount):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
    data[player_name]["inventory"]["starlight"] = amount
    save_data(PLAYERS_DATA_FILE_PATH, data)

def add_starlight_to_player(player_name, amount):
    starlight = get_starlight_of_player(player_name)
    starlight += amount
    set_starlight_of_player(player_name, starlight)



def add_to_mail(player_name, item):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
    if not "mailbox" in data[player_name]:
        data[player_name]["mailbox"] = []
    data[player_name]["mailbox"].append(item)

    save_data(PLAYERS_DATA_FILE_PATH, data)

def get_mails(player_name):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
    if not "mailbox" in data[player_name]:
        data[player_name]["mailbox"] = []
    return data[player_name]["mailbox"]

def remove_from_mail(player_name, index):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
    if not "mailbox" in data[player_name]:
        data[player_name]["mailbox"] = []
    data[player_name]["mailbox"].pop(index)

    save_data(PLAYERS_DATA_FILE_PATH, data)

def claim_mail(player_name, index):
    data = load_data(PLAYERS_DATA_FILE_PATH)
    if not player_name in data:
        data[player_name] = new_player()
    if not "mailbox" in data[player_name]:
        data[player_name]["mailbox"] = []
    
    item =  data[player_name]["mailbox"].pop(index)
    save_data(PLAYERS_DATA_FILE_PATH, data)
    
    collect_summoned_item(player_name, item)

    

def claim_all_mail(player_name):
    while len(get_mails(player_name)):
        claim_mail(player_name, 0)


def collect_summoned_item(player_name, reward):
    if is_starlight(reward):
        add_starlight_to_player(player_name, reward["amount"])
    if is_equipment(reward):
        add_equipment_to_player(player_name, reward)
    if is_playable_character(reward):
        character = reward
        character["unique_id"] = get_unique_id()
        add_character_to_player(player_name, character)

def is_playable_character(reward):
    return 'aspect' in reward and 'level' in reward

def is_equipment(reward):
    return 'rarity' in reward and 'set' in reward

def is_starlight(reward):
    return 'amount' in reward
