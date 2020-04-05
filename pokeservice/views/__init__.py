import flask
import flask_restful

from .exceptions import api_exception_views_bp
from .api_views import Pokemon, Encounters


def setup_on_app(app :flask.Flask):
    app.register_blueprint(api_exception_views_bp)

    api = flask_restful.Api(app)
    api.add_resource(api_views.Pokemon, '/api/pokemon')
    api.add_resource(api_views.Encounters, '/api/pokemon/<int:pokemon_id>/encounters')
