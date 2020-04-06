import flask
import flask.testing

from . import utils


class AnyInt:
    def __eq__(self, other):
        return isinstance(other, int)


class samples:
    post_pokemon_endpoint_request = {
        "name": "Bulbasaur",
    }

    post_pokemon_endpoint_response = {
        "base_experience": 64,
        "height": 7,
        "id": 1,
        "name": "bulbasaur",
        "sprites": {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
            "back_female": None,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
            "back_shiny_female": None,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "front_female": None,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
            "front_shiny_female": None,
        },
        "weight": 69,
    }

    get_pokemon_endpoint_response = [
        {
            "base_experience": 64,
            "height": 7,
            "id": 1,
            "name": "bulbasaur",
            "sprites": {
                "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png",
                "back_female": None,
                "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/1.png",
                "back_shiny_female": None,
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                "front_female": None,
                "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
                "front_shiny_female": None
            },
            "weight": 69
        }
    ]

    post_encounter_request_1 = {
        "note": "I've found Charmander in the forest! 🔥🌳",
        "place": "forest"
    }

    post_encounter_request_2 = {
        "place": "lake"
    }

    post_encounter_response_1 = dict(
        **post_encounter_request_1,
        timestamp=AnyInt(),
    )

    post_encounter_response_2 = dict(
        **post_encounter_request_2,
        timestamp=AnyInt(),
    )

    get_encounter_response = [
        post_encounter_response_1,
        post_encounter_response_2,
    ]


def test_end_to_end(app :flask.Flask, recreate_db):
    test_client :flask.testing.FlaskClient = app.test_client()
    connector = utils.FlaskTestClientJsonApiConnector(test_client)

    response_data = connector.make_json_request('GET', '/api/pokemon')
    assert response_data == []

    response_data = connector.make_json_request('post', '/api/pokemon', samples.post_pokemon_endpoint_request)
    assert response_data == samples.post_pokemon_endpoint_response

    response_data = connector.make_json_request('get', '/api/pokemon')
    assert response_data == samples.get_pokemon_endpoint_response

    response_data = connector.make_json_request('post', '/api/pokemon/1/encounters', samples.post_encounter_request_1)
    assert response_data == samples.post_encounter_response_1

    response_data = connector.make_json_request('post', '/api/pokemon/1/encounters', samples.post_encounter_request_2)
    assert response_data == samples.post_encounter_response_2

    response_data = connector.make_json_request('get', '/api/pokemon/1/encounters')
    assert response_data == samples.get_encounter_response
