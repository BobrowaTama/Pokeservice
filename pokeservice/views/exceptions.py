import flask
import werkzeug.exceptions

# from flask import jsonify

# api_exception_views_bp = flask.Blueprint('pokeservice_api_exceptions', __name__)


class BaseApiError(werkzeug.exceptions.HTTPException):
    def __init__(self, message, details=None):
        super().__init__(message)

        self.details = dict(details) if details else {}

        # Hack to prevent Flask-Restful interfering with our exception handling
        self.response = self.get_response()


class InvalidApiRequestError(BaseApiError):
    code = 400


class EndpointArgumentsValidaionError(InvalidApiRequestError):
    code = 422


def handle_api_error(e :BaseApiError):
    return handle_http_exception(
        e,
        {'details': e.details}
    )


def handle_http_exception(
    e :werkzeug.exceptions.HTTPException,
    extra=None,
):
    """Return JSON instead of HTML for HTTP errors."""

    details = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    if extra:
        details.update(extra)
    response = flask.jsonify({'error': details})
    response.status_code = e.code
    return response
