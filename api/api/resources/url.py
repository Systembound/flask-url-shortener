from flask import request
from flask_restful import Resource

from api.api.schemas.user import URLShortenerSchema
from api.extensions import db


class URLShortenerResource(Resource):

    def post(self):
        schema = URLShortenerSchema()
        url = schema.load(request.json)

        db.session.add(url)
        db.session.commit()

        return {
            "msg": "URL for shortening has been created!",
            "url": schema.dump(url)
        }, 201
