import flask
import flask_restful
import werkzeug.exceptions

from . import exceptions
from .api_views import Pokemon, Encounters


class Api(flask_restful.Api):
    def handle_error(self, e):
        # Don't interfere, we have out own handlers in place
        if isinstance(e, werkzeug.exceptions.HTTPException):
            raise e

        return super().handle_error(e)


def setup_on_app(app :flask.Flask):
    # app.register_blueprint(api_exception_views_bp)

    app.register_error_handler(exceptions.BaseApiError, exceptions.handle_api_error)
    app.register_error_handler(werkzeug.exceptions.HTTPException, exceptions.handle_http_exception)

    api = Api(app, catch_all_404s=True)
    api.add_resource(api_views.Pokemon, '/api/pokemon')
    api.add_resource(api_views.Encounters, '/api/pokemon/<int:pokemon_id>/encounters')
