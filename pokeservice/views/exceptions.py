import flask

# from flask import jsonify

api_exception_views_bp = flask.Blueprint('pokeservice_api_exceptions', __name__)


class BaseApiError(Exception):
    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)

        if status_code is not None:
            self.status_code = status_code

        self.details = dict(details) if details else {}
        self.details['message'] = message

    def to_dict(self):
        return self.details


class InvalidApiRequestError(BaseApiError):
    status_code = 400


# class ApiRequestMissingRequiredFieldError(InvalidApiRequestError):
#     def __init__(self, field_name):
#         super().__init__(f"{field_name!r} is a required request field for this endpoint.")


@api_exception_views_bp.errorhandler(BaseApiError)
def handle_invalid_usage(error):
    contents = {'error': error.to_dict()}

    response = flask.jsonify(contents)
    response.status_code = error.status_code

    return response
