from flask import request
from flask_restful import Resource

from api.api.schemas.user import URLShortenerSchema
from api.extensions import db


# TODO: add loggers


class URLShortenerResource(Resource):
    # TODO: more methods

    def get(self, short_url_id):
        schema = URLShortenerSchema()
        _shortner = db.session.query(URLShortenerSchema.Meta.model).filter_by(new=short_url_id).first()
        return schema.dump(_shortner)

    def post(self):
        schema = URLShortenerSchema()
        schema.validate(request.json)
        url = schema.load(request.json)

        db.session.add(url)
        db.session.commit()

        return {
            "msg": "URL for shortening has been created!",
            "url": schema.dump(url)
        }, 201
