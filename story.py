from data_manager import *
from constants import *



def set_story(*arcs):
    data = load_data(SCENES_FILE_PATH)
    data["story"] = arcs
    save_data(SCENES_FILE_PATH, data)

def get_story():
    data = load_data(SCENES_FILE_PATH)
    return data["story"]

def create_arc(arc_name, image, *chapters):
    data = load_data(SCENES_FILE_PATH)
    if arc_name not in data["arcs"]:
        data["arcs"][arc_name] = {}
        data["arcs"][arc_name]["chapters"] = chapters
        data["arcs"][arc_name]["image"] = image
        save_data(SCENES_FILE_PATH, data)

def get_arc(arc_name):
    data = load_data(SCENES_FILE_PATH)
    return data["arcs"][arc_name]

def get_arc_of_chapter(chapter_name):
    data = load_data(SCENES_FILE_PATH)
    for arc in data["arcs"]:
        if chapter_name in data["arcs"][arc]["chapters"]:
            return data["arcs"][arc]

def create_chapter(chapter_name, *series):
    data = load_data(SCENES_FILE_PATH)
    if chapter_name not in data["chapters"]:
        data["chapters"][chapter_name] = series
        save_data(SCENES_FILE_PATH, data)

def get_chapter(chapter_name):
    data = load_data(SCENES_FILE_PATH)
    return data["chapters"][chapter_name]

def create_series(series_name, *scenes):
    data = load_data(SCENES_FILE_PATH)
    if series_name not in data["series"]:
        data["series"][series_name] = scenes
        save_data(SCENES_FILE_PATH, data)

def create_scene(scene_name):
    data = load_data(SCENES_FILE_PATH)
    if scene_name not in data["scenes"]:
        data["scenes"][scene_name] = {}
        save_data(SCENES_FILE_PATH, data)


def delete_scene(scene_name):
    data = load_data(SCENES_FILE_PATH)
    if scene_name in data["scenes"]:
        data["scenes"][scene_name] = None
        save_data(SCENES_FILE_PATH, data)


def get_scene(scene_name) -> dict:
    data = load_data(SCENES_FILE_PATH)
    if scene_name in data["scenes"]:
        return data["scenes"][scene_name]
    
def set_scene(scene_name, new_value):
    data = load_data(SCENES_FILE_PATH)
    if scene_name in data["scenes"]:
        data["scenes"][scene_name] = new_value
        save_data(SCENES_FILE_PATH, data)

def set_scene_element(scene_name, value, *paths):
    scene = get_scene(scene_name)
    if scene is None:
        return

    # Navigate through the nested dictionary using paths
    temp = scene
    for path in paths[:-1]:
        if path not in temp:
            return
        temp = temp[path]

    temp[paths[-1]] = value
    set_scene(scene_name, scene)


def get_scene_element(scene_name, *paths):
    scene = get_scene(scene_name)
    if scene is None:
        return

    # Navigate through the nested dictionary using paths
    temp = scene
    for path in paths:
        if path not in temp:
            return
        temp = temp[path]
    return temp



def scene_set_background(scene_name, background):
    set_scene_element(scene_name, background, "background")


def scene_add_character(scene_name, name, image, position):
    character = {'name': name, 'image': image, 'position': position}
    current_characters = get_scene_element(scene_name, "characters")
    if current_characters == None: current_characters = []

    if name in [character['name'] for character in current_characters]:
        return
    current_characters.append(character)
    set_scene_element(scene_name, current_characters, "characters")

def remove_character(scene_name, name):
    current_characters = get_scene_element(scene_name, "characters")
    current_characters = [character for character in current_characters if character['name'] != name]
    set_scene_element(scene_name, current_characters, "characters")


def scene_add_dialogue(scene_name, character_name, text):
    dialogue = {'speaker': character_name, 'text': text}
    current_dialogue = get_scene_element(scene_name, "dialogue")
    if current_dialogue == None: current_dialogue = []
    current_dialogue.append(dialogue)
    set_scene_element(scene_name, current_dialogue, "dialogue")

def scene_remove_dialogue(scene_name, index):
    current_dialogue = get_scene_element(scene_name, "dialogue")
    current_dialogue.pop(index)
    set_scene_element(scene_name, current_dialogue, "dialogue")


def get_series(series_name):
    data = load_data(SCENES_FILE_PATH)
    if series_name in data["series"]:
        return data["series"][series_name]["scenes"]


def load_series(series_name):
    series = get_series(series_name)
    for i, scene in enumerate(series):
        series[i] = get_scene(scene)
    return series


def series_set_battle(series_name, battle):
    data = load_data(SCENES_FILE_PATH)
    if series_name in data["series"]:
        data["series"][series_name]["battle"] = battle
        save_data(SCENES_FILE_PATH, data)

def series_get_battle(series_name):
    data = load_data(SCENES_FILE_PATH)
    if series_name in data["series"]:
        return data["series"][series_name]["battle"]

