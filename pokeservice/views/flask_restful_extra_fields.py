import datetime

import flask_restful.fields


class TimestampSeconds(flask_restful.fields.Raw):
    def format(self, value :datetime.datetime) -> int:
        return int(value.timestamp())
