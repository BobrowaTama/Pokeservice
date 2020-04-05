import typing as tp

import datetime

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy_utc as sa_utc

from .base import ModelBase


def tz_aware_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


class Pokemon(ModelBase):
    __tablename__ = 'pokemon'

    # We are re-using PokeAPI-assigned ID-s, so no autoincrement please!
    pokeapi_id      = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
    name            = sa.Column(sa.Text, unique=True, nullable=False)

    base_experience = sa.Column(sa.Integer)
    height          = sa.Column(sa.Integer)
    weight          = sa.Column(sa.Integer)
    sprites         = sa.Column(sa.JSON)

    encounters :tp.List['Encounter'] = sa.orm.relationship(
        'Encounter', back_populates='pokemon'
    )


class Encounter(ModelBase):
    __tablename__ = 'encounter'

    pokemon_id = sa.Column(sa.ForeignKey(Pokemon.pokeapi_id), primary_key=True)
    timestamp  = sa.Column(sa_utc.UtcDateTime, primary_key=True, default=tz_aware_utc_now)
    place      = sa.Column(sa.Text, nullable=False)
    note       = sa.Column(sa.Text)

    pokemon :Pokemon = sa.orm.relationship(
        'Pokemon', back_populates='encounters'
    )
