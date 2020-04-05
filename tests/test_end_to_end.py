import flask
import flask.testing


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
    client :flask.testing.FlaskClient = app.test_client()

    resp = client.get('/api/pokemon')
    assert resp.status_code == 200
    assert resp.get_json() == []

    resp = client.post('/api/pokemon', json=samples.post_pokemon_endpoint_request)
    assert resp.status_code == 200
    assert resp.get_json() == samples.post_pokemon_endpoint_response

    resp = client.get('/api/pokemon')
    assert resp.status_code == 200
    assert resp.get_json() == samples.get_pokemon_endpoint_response

    resp = client.post('/api/pokemon/1/encounters', json=samples.post_encounter_request_1)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    # assert isinstance(resp_json['timestamp'], int)
    # del resp_json['timestamp']
    assert resp_json == samples.post_encounter_response_1

    resp = client.post('/api/pokemon/1/encounters', json=samples.post_encounter_request_2)
    assert resp.status_code == 200
    resp_json = resp.get_json()
    # assert isinstance(resp_json['timestamp'], int)
    # del resp_json['timestamp']
    assert resp_json == samples.post_encounter_response_2

    resp = client.get('/api/pokemon/1/encounters')
    assert resp.status_code == 200
    assert resp.get_json() == samples.get_encounter_response
