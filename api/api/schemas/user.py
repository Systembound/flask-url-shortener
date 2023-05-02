from marshmallow.fields import URL

from api.api.schemas.validators import validate_url_length
from api.extensions import ma, db
from api.models import User
from api.models.api import Url


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)


class URLShortenerSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    hits = ma.Int(dump_only=True)
    created = ma.DateTime(dump_only=True)
    url = ma.URL(required=True, validate=[
        URL(require_tld=True, message="Invalid URL"), validate_url_length
    ])

    class Meta:
        model = Url
        sqla_session = db.session
        load_instance = True
