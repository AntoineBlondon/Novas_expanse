from constants import BANNERS_FILE_PATH, SummonableType
from data_manager import *
import random
from player_inventory import *
from character_handler import *
from equipment_handler import *

def create_banner(banner):
    data = load_data(BANNERS_FILE_PATH)
    name = banner["name"]
    if name not in data:
        data[name] = banner
        save_data(BANNERS_FILE_PATH, data)

def edit_banner(name, banner):
    data = load_data(BANNERS_FILE_PATH)
    if name in data:
        data[name] = banner
        save_data(BANNERS_FILE_PATH, data)


def set_banner(name, banner):
    data = load_data(BANNERS_FILE_PATH)
    data[name] = banner
    save_data(BANNERS_FILE_PATH, data)


def get_banner(name):
    data = load_data(BANNERS_FILE_PATH)
    if name in data:
        return data[name]

def get_banners():
    data = load_data(BANNERS_FILE_PATH)
    return [data[name] for name in data]

def add_item(banner, category, item):
    # Convert the Enum to a string
    category = str(category)

    # Remove item from all categories
    for category_items in banner['drops'].values():
        while item in category_items:
            category_items.remove(item)
    # Add item to the specified category
    if item not in banner['drops'][category]:
        banner['drops'][category].append(item)



def set_rates(banner, category, rate):
    banner[str(category) + '_rate'] = rate

def calculate_normal_drop_rate(banner):
    total_rate = sum(banner.get(str(category) + '_rate', 0) for category in SummonableType)
    banner[str(SummonableType.NORMAL_DROP) + '_rate'] = max(0, 1 - total_rate)


def summon(banner_name):
    banner = get_banner(banner_name)
    # Calculate total weights
    total_weights = sum(banner[str(category) + '_rate'] for category in SummonableType)
    
    # Generate a random number between 0 and total_weights
    rand_num = random.uniform(0, total_weights)
    
    # Find which category the random number falls into
    sum_weights = 0
    for category in SummonableType:
        sum_weights += banner[str(category) + '_rate']
        if rand_num <= sum_weights:
            # Randomly select an item from the chosen category
            item = random.choice(banner['drops'][str(category)])
            return item





def simple_banner():
    # Create a banner
    my_banner = Banner("New Year's Banner", "Special New Year's banner with increased rates for festive items!", "banner.png", 200)

    # Add items to banner
    character_1 = create_playable_character("Isabella", "Void", unlocked_skins=["Isabella.png"])
    character_2 = create_playable_character("Iria", "Space", unlocked_skins=["Iria.png", "Iria_undercover.png"])
    equipment_1 = get_equipment("Navigator's Amulet")
    equipment_2 = get_equipment("Navigator's Garb")
    equipment_3 = get_equipment("Navigator's Ring")
    equipment_4 = get_equipment("Navigator's Elixir")
    equipment_5 = get_equipment("Navigator's Helmet")
    starlight = {"amount": 90}

    
    add_item(my_banner, SummonableType.FEATURED, character_1)
    add_item(my_banner, SummonableType.FEATURED, character_2)
    add_item(my_banner, SummonableType.BEST_DROP, equipment_1)
    add_item(my_banner, SummonableType.GOOD_DROP, equipment_2)
    add_item(my_banner, SummonableType.BEST_DROP, equipment_3)
    add_item(my_banner, SummonableType.GOOD_DROP, equipment_4)
    add_item(my_banner, SummonableType.BEST_DROP, equipment_5)
    add_item(my_banner, SummonableType.NORMAL_DROP, starlight)

    # Set rates
    set_rates(my_banner, SummonableType.FEATURED, 0.02)
    set_rates(my_banner, SummonableType.BEST_DROP, 0.1)
    set_rates(my_banner, SummonableType.GOOD_DROP, 0.2)
    calculate_normal_drop_rate(my_banner)

    
    set_banner(my_banner["name"], my_banner)

def summoning(player_name):
    reward = summon("New Year's Banner")
    collect_summoned_item(player_name, reward)

def summon_banner(player_name, banner_name, amount):
    for i in range(amount):
        reward = summon(banner_name)
        add_to_mail(player_name, reward)