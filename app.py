from flask import Flask, session, redirect, url_for, render_template, request
from functools import wraps
from character_handler import *
from equipment_handler import *
from player_inventory import *
from banners_handler import *
from data_manager import *
from constants import *
from battle import *
from helper import *
from story import *


app = Flask(__name__)
app.secret_key = '8e5f02a4ea054b3cb4ff41db3f7b4810'

def check_user_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def main_page():
    """
    A route decorator that handles requests to the root URL.
    
    Returns:
        The rendered template for the main page, with the logged-in user's information.
    """
    if not is_connected(session):
        return redirect(url_for('login'))
    username = session['username']
    return render_template('main.html', player=get_player(username), mails=get_mails(username))

@app.route('/claim_mail')
def claim_mail():
    """
    Route decorator for the '/claim_mail' endpoint.

    Returns:
        A redirect response to the login page if the user is not connected.
        A redirect response to the main page after claiming all mail.
    """
    if not is_connected(session):
        return redirect(url_for('login'))
    username = session['username']
    claim_all_mail(username)
    return redirect(url_for("main_page"))




@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login functionality for the application.

    Parameters:
    - None

    Returns:
    - If the request method is 'POST' and the given username and password are valid, the function redirects to the main page.
    - If the request method is 'POST' and the given username and password are invalid, the function returns the string 'Invalid credentials'.
    - If the request method is 'GET', the function renders the login.html template.

    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'secret':
            session['username'] = username
            return redirect(url_for('main_page'))
        else:
            return 'Invalid credentials'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs out the current user by removing the 'username' key from the session.
    
    Returns:
        A redirect response to the main page.
    """
    session.pop('username', None)
    return redirect(url_for('main_page'))

@app.route('/characters')
def characters_page():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('characters.html', characters=get_characters_of_player(username), player=get_player(username))

@app.route('/characters/<id>')
def character_sheet(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    characters = get_characters_of_player(username)
    character = next((character for character in characters if character["unique_id"] == id), None)

    template = get_template_character(character_name=character["name"])
    slots = [e.value for e in EquipmentSlot]
    character_equipment = [character["equipment"].get(slot, None) for slot in slots]

    return render_template('character_sheet.html', 
                           character=character, 
                           player=get_player(username), 
                           template=template, 
                           stats=get_stats_of_character(character), 
                           equipment=get_equipment_of_player(username),
                           character_equipment=character_equipment)

@app.route('/characters/<id>/remove_equipment/<slot>')
def remove_equipment(id, slot):
    """
    Removes equipment from a character in the game.

    Parameters:
        id (str): The unique identifier of the character.
        slot (str): The slot from which the equipment needs to be removed.

    Returns:
        redirect: A redirect to the character's page after removing the equipment.
    """
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    character = [character for character in get_characters_of_player(username) if character["unique_id"] == id][0]
    slot = int(slot)
    if slot in [2,3]:
        equipment_slot = EquipmentSlot.ACCESSORY_1.value if slot == 2 else EquipmentSlot.ACCESSORY_2.value
    else:
        equipment_slot = [EquipmentSlot.HAT.value, EquipmentSlot.CLOTHING.value][slot]
    switch_equipment_of_character(username, character, equipment_slot)
    return redirect("/characters/" + str(id))


@app.route('/characters/<id>/switch_equipment/<equipment>')
def switch_equipment(id, equipment):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    equipment = get_equipment_of_player(username)[int(equipment)]
    characters = get_characters_of_player(username)
    
    character = next((character for character in characters if character["unique_id"] == id), None)
    if character is None:
        return redirect("/characters/" + str(id))
    
    equipment_type = equipment["type"]
    if equipment_type == EquipmentType.ACCESSORY.value:
        equipment_slot = get_available_accessory_slot(character)
        if not equipment_slot:
            return redirect("/characters/" + str(id))
    else:
        equipment_slot = equipment_type
    
    switch_equipment_of_character(username, character, equipment_slot, equipment)
    return redirect("/characters/" + str(id))



@app.route('/update_skin', methods=['POST'])
def update_skin():
    unique_id = request.form.get('unique_id')
    new_skin = request.form.get('new_skin')
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    character = get_character_of_player(username, unique_id)
    if new_skin in character["unlocked_skins"]:
        character["active_skin"] = new_skin
        edit_character_of_player(username, unique_id, character)
    return redirect('/characters/' + str(unique_id))


@app.route('/admin/character-template-sheet/<name>')
def character_template_sheet(name):
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    
    template = get_template_character(name)
    return render_template('character_template_sheet.html', template=template)

@app.route('/rewards')
def rewards():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session["username"]

    return render_template("rewards.html")

@app.route('/battle', defaults={'chapter_name': None})
@app.route('/battle/<chapter_name>')
@check_user_session
def battle(chapter_name):
    username = session['username']
    
    if chapter_name is None:
        return redirect(url_for('battle', chapter_name='None'))
    
    username = session['username']
    battle = get_current_battle(username)
    
    enemies = [character for character in battle["characters"] if character["owner"] == "enemy"]
    allies = [character for character in battle["characters"] if character["owner"] == username]

    active_character_ids = {char[1]['unique_id'] if isinstance(char[1], dict) else char['unique_id'] for char in battle["active_characters"]}
    active_characters = [char for char in battle["characters"] if char["unique_id"] in active_character_ids]

    character_names = {
        character['unique_id']: get_character_of_player(character['owner'], character["unique_id"])["name"]
        for character in battle["characters"]
    }

    return render_template("current_battle.html", 
                           enemies=enemies, 
                           allies=allies, 
                           active_characters=active_characters, 
                           names=character_names, 
                           get_character_of_player=get_character_of_player, 
                           plan=battle["plan"], 
                           current_phase=battle["turn"], 
                           goto=chapter_name)


@app.route('/battle/specific', methods=['GET'])
@check_user_session
def specific_battle_page():
    username = session['username']
    battle_name = request.args.get('battle_name')
    chapter_name = request.args.get('chapter_name')
    
    if not battle_name or not chapter_name:
        # Handle error or provide a default action.
        return redirect(url_for('battle'))

    start_battle(username, get_battle(battle_name))
    return redirect(url_for('battle', chapter_name=chapter_name))

@app.route('/battle/advance', methods=['GET'])
@check_user_session
def battle_advance():
    username = session['username']
    goto = request.args.get('goto', 'None')

    battle = get_current_battle(username)

    if is_battle_ended(battle):
        if is_battle_ended(battle) != username:
            add_rewards(username, battle)
        return redirect(url_for("main_page") if goto == "None" else url_for("chapter_page", arc_name=get_arc_of_chapter(goto), chapter_name=goto))

    set_current_battle(username, advance(battle))
    return redirect(url_for("battle"))


@app.route('/admin/add')
def admin_add():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    username = session['username']
    """
    iria = create_playable_character("Iria", Aspect.TIME.value, 1, ["Iria.png", "Iria_beach.png", "Iria_undercover.png"])
    add_character_to_player(username, iria)
    """
    
    simple_banner()

    start_battle(username, get_battle("simple_battle"))

    return redirect(url_for("characters_page"))

@app.route('/admin')
def admin_page():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    characters = get_template_characters()
    return render_template('admin.html', characters=characters, players=get_players(), equipments=get_equipments())

@app.route('/admin/new-equipment')
def new_equipment():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    return render_template('new_equipment.html')

@app.route('/admin/create-equipment', methods=['POST'])
def create_equipment_page():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    name = request.form['name']
    rarity = request.form['rarity']
    set = request.form['set']
    type = request.form['type']
    description = request.form['description']
    stats = [float(i) for i in request.form['stats'].split(",")]
    skills = request.form['skills'].split(",")
    skin = request.form['skin']

    equipement = Equipment(name, rarity, set, type, description, skin, stats, skills)

    create_equipment(name, equipement)
    return redirect('/admin')

@app.route('/admin/new-character-template')
def new_character_template():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    return render_template('new_character_template.html')



@app.route('/admin/create-character-template', methods=['POST'])
def create_character_template():
    if 'username' not in session or session['username'] != "admin":
        return redirect(url_for('main_page'))
    name = request.form['name']
    world = request.form['world']
    rarity = int(request.form['rarity'])
    possible_aspects = request.form.getlist('possible_aspects[]')
    attack_pattern = request.form['attack_pattern']
    story = request.form['story']
    skins = request.form['skins'].split(",")
    base_stats = [float(i) for i in request.form['base_stats'].split(",")]
    growth_rate = [float(i) for i in request.form['growth_rate'].split(",")]
    guardian = request.form['guardian']
    skills = request.form['skills'].split(",")

    char = template_character(
        name=name,
        world=world,
        rarity=rarity,
        possible_aspects=possible_aspects,
        attack_pattern=attack_pattern,
        story=story,
        skins=skins,
        base_stats=base_stats,
        growth_rate=growth_rate,
        guardian=guardian,
        skills=skills
        )

    create_template_character(char)
    return redirect('/admin')



@app.route('/summon')
def summon_page():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    return render_template('summon.html', player=get_player(username), banners=get_banners())


@app.route('/summon/<name>')
def banner_sheet(name):
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    return render_template('banner_sheet.html', player=get_player(username), banner=get_banner(name))


@app.route('/summon/<name>/<amount>')
def summoning_banner(name, amount):
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    amount = int(amount)
    summon_banner(username, name, amount)

    return redirect("/summon/" + name)



@app.route('/story')
def story_page():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    return render_template('story.html', player=get_player(username), arcs=get_story(), get_arc=get_arc, roman=intToRoman)

@app.route('/story/arc/<name>')
def arc_page(name):
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    return render_template('story_arc.html', player=get_player(username), chapters=get_arc(name)["chapters"], arc_name=name)

@app.route('/story/arc/<arc_name>/chapter/<chapter_name>')
def chapter_page(arc_name, chapter_name):
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    return render_template('story_chapter.html', player=get_player(username),chapter_name=chapter_name, episodes=get_chapter(chapter_name), get_series=load_series, arc_name=arc_name)


@app.route('/story/arc/<arc_name>/chapter/<chapter_name>/episode/<episode_name>')
def episode_page(arc_name, chapter_name, episode_name):
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']

    scenes=load_series(episode_name)

    return render_template('novel.html', player=get_player(username), username=username, scenes=scenes, arc_name=arc_name, chapter_name=chapter_name, battle=series_get_battle(episode_name))



@app.route('/novel')
def novel_page():
    if not 'username' in session:
        return redirect(url_for('login'))
    username = session['username']
    scenes = load_series("chapter_1")
    return render_template('novel.html', scenes=scenes)

if __name__ == '__main__':
    app.run(debug=True)
