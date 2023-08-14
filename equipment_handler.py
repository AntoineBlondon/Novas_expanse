from constants import *
from data_manager import *
from player_inventory import *



def create_equipment(name, equipment):
    data = load_data(EQUIPMENT_FILE_PATH)
    if name not in data:
        data[name] = equipment
        save_data(EQUIPMENT_FILE_PATH, data)

def edit_equipment(name, equipment):
    data = load_data(EQUIPMENT_FILE_PATH)
    if name in data:
        data[name] = equipment
        save_data(EQUIPMENT_FILE_PATH, data)


def set_equipment(name, equipment):
    data = load_data(EQUIPMENT_FILE_PATH)
    data[name] = equipment
    save_data(EQUIPMENT_FILE_PATH, data)


def get_equipment(name):
    data = load_data(EQUIPMENT_FILE_PATH)
    if name in data:
        return data[name]

def get_equipments():
    data = load_data(EQUIPMENT_FILE_PATH)
    return [data[name] for name in data]



def set_equipment_of_character(player, playable_character, equipment_set):
    unique_id = playable_character["unique_id"]
    playable_character["equipment"] = equipment_set
    edit_character_of_player(player, unique_id, playable_character)


def set_equipment_in_slot(player, playable_character, equipment_slot, item):
    unique_id = playable_character["unique_id"]
    playable_character["equipment"][equipment_slot] = item
    edit_character_of_player(player, unique_id, playable_character)






def get_equipment_of_character(playable_character):
    return playable_character["equipment"]





def get_available_accessory_slot(playable_character):
    print(playable_character)
    if not EquipmentSlot.ACCESSORY_1.value in playable_character["equipment"]:
        return EquipmentSlot.ACCESSORY_1.value
    if not EquipmentSlot.ACCESSORY_2.value in playable_character["equipment"]:
        return EquipmentSlot.ACCESSORY_2.value
    if not playable_character["equipment"][EquipmentSlot.ACCESSORY_1.value]:
        return EquipmentSlot.ACCESSORY_1.value
    if not playable_character["equipment"][EquipmentSlot.ACCESSORY_2.value]:
        return EquipmentSlot.ACCESSORY_2.value
    return None


def switch_equipment_of_character(player, playable_character, equipment_slot, item=False):
    

    unique_id = playable_character["unique_id"]
    current_equipment = None
    if equipment_slot in playable_character["equipment"]:
        current_equipment = playable_character["equipment"][equipment_slot]
    set_equipment_in_slot(player, playable_character, equipment_slot, item if item else None)
    if item:
        remove_equipment_from_player(player, item)
    if current_equipment:
        add_equipment_to_player(player, current_equipment)
    edit_character_of_player(player, unique_id, playable_character)