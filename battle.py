from data_manager import *
from player_inventory import *
from character_handler import *
from constants import *
import random


def empty_plan():
    return [[] for x in range(12)]

def empty_battle_inventory():
    return {
        "terrain": "",
        "characters": [],
        "active_characters": [],
        "plan": empty_plan(),
        "turn": 0,
        "validated": False,
        "rewards": {"starlight": 100}
    }


def add_pattern_to_plan(plan, pattern):
    for i, state in enumerate(pattern):
        if state != []:
            plan[i].append(state)
    return plan

def get_pattern(owner, character):
    template = get_template_character(character["name"])
    attack_pattern = [(owner, character) if state != "-" else [] for state in template["attack_pattern"].split('/')]
    return attack_pattern

def add_character_to_plan(plan, owner, character):
    return add_pattern_to_plan(plan, get_pattern(owner, character))




def print_plan(plan):
    for i in range(12):
        for a in plan[i]:
            try:
                print(f"{a[0]},{a[1]['name']}", end="/")
            except:
                print("[]", end="/")
        print()


def get_fighting_character(owner, playable_character):
    return {
        "unique_id": playable_character["unique_id"],
        "owner": owner,
        "health": float(get_stats_of_character(playable_character)[0]),
        "stats": get_stats_of_character(playable_character),
        "bonus_stats": [0.0 for x in range(9)],
        "dead": False,
        "state": None
    }

def add_character_to_battle(battle_inventory, owner, playable_character):
    battle_inventory["characters"].append(get_fighting_character(owner, playable_character))
    battle_inventory["plan"] = add_character_to_plan(battle_inventory["plan"], owner, playable_character)
    return battle_inventory

def set_reward_to_battle(battle_inventory, item, amount):
    battle_inventory["rewards"][item] = amount
    return battle_inventory

def get_fighting_character_from_game(battle_inventory, unique_id):
    for fighting_character in battle_inventory["characters"]:
        if fighting_character["unique_id"] == unique_id:
            return fighting_character

def set_fighting_character_of_game(battle_inventory, unique_id, new_fighting_character):
    for i, fighting_character in enumerate(battle_inventory["characters"]):
        if fighting_character["unique_id"] == unique_id:
            battle_inventory["characters"][i] = new_fighting_character
    return battle_inventory

def type_of_attack(fighting_character):
    return AttackType.PHYSICAL if fighting_character["stats"][Stat.ATTACK_PHYSICAL.value] > fighting_character["stats"][Stat.ATTACK_ASPECT.value] else AttackType.ASPECT


def calculate_damage(attacker, defender):
    attack_type = type_of_attack(attacker)

    attack_stat = attacker["stats"][Stat.ATTACK_ASPECT.value]
    defence_stat = defender["stats"][Stat.RESISTANCE_ASPECT.value]
    if attack_type == AttackType.PHYSICAL:
        attack_stat = attacker["stats"][Stat.ATTACK_PHYSICAL.value]
        defence_stat = defender["stats"][Stat.DEFENCE_PHYSICAL.value]
    
    crit_chance = attacker["stats"][Stat.CRITICAL_CHANCE.value]
    crit_damage = attacker["stats"][Stat.CRITICAL_DAMAGE.value]

    base_damage = attack_stat

    damage_reduction = defence_stat / (defence_stat + 100)

    net_damage = base_damage * (1 - damage_reduction)


    if random.random() < crit_chance / 100:
        net_damage *= 1 + crit_damage / 100

    net_damage = max(0, net_damage)

    return round(net_damage, 1)

def attack(battle_inventory, attacker_id, defender_id):
    attacker = get_fighting_character_from_game(battle_inventory, attacker_id)
    defender = get_fighting_character_from_game(battle_inventory, defender_id)

    damage = calculate_damage(attacker, defender)

    defender["health"] = round(defender["health"] - damage, 1)
    if defender["health"] <= 0:
        defender["health"] = 0
        defender["dead"] = True

    battle_inventory = set_fighting_character_of_game(battle_inventory, defender_id, defender)

    return battle_inventory
    

    
def refresh_plan(battle_inventory):
    battle_inventory["plan"] = empty_plan()
    for fighting_character in battle_inventory["characters"]:
        if fighting_character["health"] > 0:
            character = get_character_of_player(fighting_character["owner"], fighting_character["unique_id"])
            battle_inventory["plan"] = add_character_to_plan(battle_inventory["plan"], fighting_character["owner"], character)
    return battle_inventory


def simple_battle():
    create_battle("simple_battle")
    battle_inventory = get_battle("simple_battle")
    simple_enemy = get_characters_of_player("enemy")[0]
    simple_enemy2 = get_characters_of_player("enemy")[1]

    

    add_character_to_battle(battle_inventory, "enemy", simple_enemy)
    add_character_to_battle(battle_inventory, "enemy", simple_enemy2)
    set_reward_to_battle(battle_inventory, "starlight", 100)

    set_battle("simple_battle", battle_inventory)


def start_battle(player_name, battle_inventory):
    for character in get_characters_of_player(player_name):
        add_character_to_battle(battle_inventory, player_name, character)
    battle_inventory = refresh_active_characters(battle_inventory)
    battle_inventory = refresh_plan(battle_inventory)
    set_current_battle(player_name, battle_inventory)

    
def print_battle(battle_inventory):
    print(f"Turn: {battle_inventory['turn']}")
    for character in battle_inventory["characters"]:
        playable_character = get_character_of_player(character["owner"], character["unique_id"])
        print(f"{playable_character['name']},{character['owner']},{character['health']}")



def get_active_characters(battle_inventory):
    return battle_inventory["plan"][battle_inventory["turn"]]


def refresh_active_characters(battle_inventory):
    battle_inventory["active_characters"] = get_active_characters(battle_inventory)
    return battle_inventory


def choose_enemy_from(enemies):
    chosen = enemies[0]
    for character in enemies:
        if character["health"] < chosen["health"]:
            chosen = character
    return chosen

def advance(battle):
    battle = refresh_plan(battle)
    if len(battle["active_characters"]) > 0:
        owner, character = battle["active_characters"][0]

        enemy = ""
        for char in battle["characters"]:
            other = char["owner"]
            if owner != other:
                enemy = other
        
        enemy_character_id = choose_enemy_from(get_alive_characters_of_team(battle, enemy))["unique_id"]

        battle = attack(battle, character["unique_id"], enemy_character_id)

        battle["active_characters"].pop(0)
    else:
        battle = next_turn(battle)

    return battle


def next_turn(battle):
    battle["turn"] += 1

    battle["turn"] %= 12

    battle = refresh_active_characters(battle)

    return battle

def get_alive_characters_of_team(battle, team):
    return [char for char in get_characters_of_team(battle, team) if not char["dead"]]

def get_characters_of_team(battle, team):
    return [char for char in battle["characters"] if char["owner"] == team]

def get_teams_of_battle(battle):
    teams = []
    for char in battle["characters"]:
        team = char["owner"]
        if team not in teams:
            teams.append(team)
    return teams


def is_battle_ended(battle):
    """
    Checks if a battle has ended by determining if all characters in all teams are dead.

    Parameters:
    - battle: The battle object representing the ongoing battle.

    Returns:
    - The team that has won the battle, or None if the battle has not ended.
    """
    for team in get_teams_of_battle(battle):
        ended = True
        for character in get_characters_of_team(battle, team):
            fighting_charcater = get_fighting_character_from_game(battle, character["unique_id"])
            if not fighting_charcater["dead"]:
                ended = False
        if ended: return team

    


def add_rewards(player_name, battle):
    if "starlight" in battle["rewards"]:
        add_starlight_to_player(player_name, battle["rewards"]["starlight"])





def get_current_battle(player_name):
    return get_player(player_name)["current_battle"]




def create_battle(battle_name):
    data = load_data(BATTLES_FILE_PATH)
    if battle_name not in data:
        data[battle_name] = empty_battle_inventory()
        save_data(BATTLES_FILE_PATH, data)

def delete_battle(battle_name):
    data = load_data(BATTLES_FILE_PATH)
    if battle_name in data:
        del data[battle_name]
        save_data(BATTLES_FILE_PATH, data)


def set_battle(battle_name, battle_inventory):
    data = load_data(BATTLES_FILE_PATH)
    if battle_name in data:
        data[battle_name] = battle_inventory
        save_data(BATTLES_FILE_PATH, data)

def get_battle(battle_name):
    data = load_data(BATTLES_FILE_PATH)
    if battle_name in data:
        return data[battle_name]