import os, requests
from flask import Flask, render_template, request

app = Flask(__name__)

def get_characteristics(character):
    # Get the information for the given character from the SWAPI
    response = requests.get(f"https://swapi.dev/api/people/?search={character}", timeout=15)
    if response.status_code != 200:
        return "Error", None
    else:
        data = response.json()
        if data.get("results"):
            filtered_data = data["results"][0]
            character_id = extract_character_id(filtered_data["url"])
            character_data = {}
            character_data["Name"] = filtered_data["name"]
            character_data["Height"] = filtered_data["height"]
            character_data["Eye Color"] = filtered_data["eye_color"].capitalize()
            character_data["Gender"] = filtered_data["gender"].capitalize()
            character_data["Mass"] = filtered_data["mass"]
            character_data["Films"] = len(filtered_data["films"])
            character_data["Starships"] = len(filtered_data["starships"])
            character_data["Vehicles"] = len(filtered_data["vehicles"])
        else:
            return None, None

        return character_data, character_id


def extract_character_id(url):
    # Extract the character id from the character url
    if url[-3].isnumeric():
        id = url[-3:-1]
    else:
        id = url[-2:-1]
    return id


def compute_characteristics_score(characters):
    # Compute the score for each character and return the winner
    for character in characters:
        score = 0
        for value in character.values():
            if isinstance(value, int):
                score += value
            elif isinstance(value, str) and value.isnumeric():
                score += int(value)
        character["Score"] = score

    if characters[0]["Score"] > characters[1]["Score"]:
        winner = characters[0]["Name"]
    else:
        winner = characters[1]["Name"]

    return characters, winner


def get_images(id_1, id_2):
    # Generate the image url with the character id's in string format
    images = []
    if os.path.exists(f"static/images/{id_1}.jpg"):
        images.append(f"{id_1}.jpg")
    else:
        images.append("image_not_found.jpg")
    if os.path.exists(f"static/images/{id_2}.jpg"):
        images.append(f"{id_2}.jpg")
    else:
        images.append("image_not_found.jpg")

    return images


@app.route("/", methods =["GET", "POST"])
def choose_character():
    error=None
    characters = []

    if request.method == "POST":
        character1 = request.form.get("character1")
        character2 = request.form.get("character2")
        character1_data, id_1 = get_characteristics(character=character1)
        character2_data, id_2 = get_characteristics(character=character2)

        if character1_data and character2_data:
            if character1_data == "Error" or character2_data == "Error":
                return render_template('choose_character.jinja2',
                                       error="Oops, SWAPI could not be accessed now, sorry!")
            characters.append(character1_data)
            characters.append(character2_data)
            characters_scored, winner = compute_characteristics_score(characters)
            return show_comparison(characters_scored, winner, id_1, id_2)

        if not character1:
            error = f"{character1} could not be found, please try again."
        else:
            error = f"{character2} could not be found, please try again."

    return render_template('choose_character.jinja2', error=error)

@app.route("/compare")
def show_comparison(characters_scored, winner, id_1, id_2):
    images = get_images(id_1, id_2)
    return render_template('compare_characters.jinja2',
                           characters=characters_scored, winner=winner, images=images)
