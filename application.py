import requests
from bing_images import bing
from flask import Flask, render_template, request

app = Flask(__name__)

def get_characteristics(character):
        response = requests.get(f"https://swapi.dev/api/people/?search={character}")
        if response.status_code != 200:
            return None
        else:
            data = response.json()
            if data["results"]:
                filtered_data = data["results"][0]
                character_data = {}
                character_data["Name"] = filtered_data["name"]
                character_data["Height"] = filtered_data["height"]
                character_data["Eye Color"] = filtered_data["eye_color"].capitalize()
                character_data["Gender"] = filtered_data["gender"].capitalize()
                character_data["Mass"] = filtered_data["mass"]
                character_data["Films"] = len(filtered_data["films"])
                character_data["Starships Piloted"] = len(filtered_data["starships"])
                character_data["Vehicles Piloted"] = len(filtered_data["vehicles"])
            else:
                return None

            return character_data

def compute_characteristics(characters):
    for character in characters:
        score = 0
        for value in character.values():
            if type(value) == int:
                score += value
            elif type(value) == str and value.isnumeric():
                score += int(value)
        character["Score"] = score

    if characters[0]["Score"] > characters[1]["Score"]:
        winner = characters[0]["Name"]
    else:
        winner = characters[1]["Name"]

    return characters, winner

def get_images(characters):
    image_urls = []
    for character in characters:
        url = bing.fetch_image_urls(character["Name"], limit=1, file_type='png', filters='+filterui:aspect-square+filterui:color2-bw', extra_query_params='&first=1')
        if url:
            image_urls.append(url)
    return image_urls

@app.route("/", methods =["GET", "POST"])
def choose_character():
    error=None
    characters = []

    if request.method == "POST":
        character1 = request.form.get("character1")
        character2 = request.form.get("character2")
        character1_data = get_characteristics(character=character1)
        character2_data = get_characteristics(character=character2)

        if character1_data and character2_data:
            characters.append(character1_data)
            characters.append(character2_data)
            characters_scored, winner = compute_characteristics(characters)
            return show_comparison(characters_scored, winner)

        elif not character1:
            error = "{} could not be found, please try again.".format(character1)

        else:
            error = "{} could not be found, please try again.".format(character1)

    return render_template('choose_character.jinja2', error=error)

@app.route("/compare")
def show_comparison(characters_scored, winner):
    images = get_images(characters=characters_scored)
    return render_template('compare_characters.jinja2', characters=characters_scored, winner=winner, images=images)
