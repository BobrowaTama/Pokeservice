import urllib.parse

import flask_restful
import flask_restful.fields
import sqlalchemy as sa
import sqlalchemy.orm
import requests
import webargs.flaskparser

from .. import models
from ..db import current_request_transaction

from .exceptions import InvalidApiRequestError
from .flask_restful_extra_fields import TimestampSeconds


class UnknownPokemonNameError(InvalidApiRequestError):
    pass


class PokemonNotInDbError(InvalidApiRequestError):
    pass


_pokemon_response_fields = dict(
    id                 = flask_restful.fields.Integer(attribute='pokeapi_id'),
    name               = flask_restful.fields.String,
    base_experience    = flask_restful.fields.Integer,
    height             = flask_restful.fields.Integer,
    weight             = flask_restful.fields.Integer,
    sprites            = flask_restful.fields.Raw,
)


POKEAPI_BASE_URL = 'https://pokeapi.co'


class Pokemon(flask_restful.Resource):
    @webargs.flaskparser.use_args({
        'name': webargs.fields.Str(required=True)
    })
    def post(self, args):
        pokemon_name :str = args['name']

        pokemon_name = pokemon_name.lower()

        with current_request_transaction() as session:
            pokemon = session.query(models.Pokemon).filter_by(name=pokemon_name).one_or_none()

            if not pokemon:
                pokemon = self._try_fetch_pokemon_from_pokeapi(pokemon_name)

                if pokemon:
                    session.add(pokemon)
                else:
                    raise UnknownPokemonNameError(f"Cannot find Pokemon with name {pokemon_name!r}.")

            pokemon_json = flask_restful.marshal(pokemon, _pokemon_response_fields)

        return pokemon_json

    def get(self):
        with current_request_transaction() as session:
            all_pokemon = session.query(models.Pokemon).all()
            all_pokemon_json = flask_restful.marshal(all_pokemon, _pokemon_response_fields)

        return all_pokemon_json

    def _try_fetch_pokemon_from_pokeapi(self, pokemon_name :str):
        escaped_name = urllib.parse.quote(pokemon_name)

        url = POKEAPI_BASE_URL + '/api/v2/pokemon/' + escaped_name
        response = requests.get(url)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        pokemon_data = response.json()

        pokemon = models.Pokemon(
            pokeapi_id=pokemon_data['id'],
            name=pokemon_data['name'],
            base_experience=pokemon_data['base_experience'],
            height=pokemon_data['height'],
            weight=pokemon_data['weight'],
            sprites=pokemon_data['sprites'],
        )

        return pokemon


_encounter_response_fields = dict(
    note               = flask_restful.fields.String,
    place              = flask_restful.fields.String,
    timestamp          = TimestampSeconds,
)


class Encounters(flask_restful.Resource):
    @webargs.flaskparser.use_args({
        'place': webargs.fields.Str(required=True),
        'note': webargs.fields.Str()
    })
    def post(self, args, pokemon_id):
        place = args['place']
        note = args.get('note')

        with current_request_transaction() as session:
            pokemon = self._get_pokemon(session, pokemon_id)
            encounter = models.Encounter(place=place, note=note)

            pokemon.encounters.append(encounter)

            session.flush()

            encounter_json = self._marshal_encounter(encounter)

        return encounter_json

    def get(self, pokemon_id):
        with current_request_transaction() as session:
            pokemon = self._get_pokemon(session, pokemon_id)

            encounters_json = self._marshal_encounter(pokemon.encounters)

        return encounters_json

    def _get_pokemon(self, session :sa.orm.Session, pokemon_id):
        pokemon = session.query(models.Pokemon).get(pokemon_id)

        if not pokemon:
            raise PokemonNotInDbError(
                f"No Pokemon with id={pokemon_id!r} exists in our database.\n"
                f"Did you remember to import it first using POST /pokemon endpoint?"
            )

        return pokemon

    @staticmethod
    def _marshal_encounter(encounter):
        # Unfortunately, Flask-RESTful does not support optional keys when marshalling objects,
        #  so we need to post-process the dict

        ret = flask_restful.marshal(encounter, _encounter_response_fields)
        ret = _filter_none_values(ret, {'note'})

        return ret


def _filter_none_values(dict_or_list, keys_to_filter):
    if isinstance(dict_or_list, list):
        return type(dict_or_list)(
            _filter_none_values(item, keys_to_filter)
            for item in dict_or_list
        )

    if isinstance(dict_or_list, dict):
        return type(dict_or_list)(
            (key, value)
            for key, value in dict_or_list.items()
            if value or key not in keys_to_filter
        )
