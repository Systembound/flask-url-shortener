from marshmallow.validate import URL as UrlValidator

from marshmallow import post_load

from api.api.schemas.validators import validate_url_length
from api.extensions import ma, db
from api.models.api import Url as UrlModel
from api.models.user import User


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
    new = ma.String(dump_only=True)
    old = ma.String(dump_only=True)

    class Meta:
        model = UrlModel
        sqla_session = db.session
        load_instance = True

    url = ma.URL(required=True, validate=[
        UrlValidator(), validate_url_length
    ])

    def generate_shortcode(self):
        return UrlModel.generate_shortcode(
            self.context.get('url', None)
        )

    @post_load
    def generate_new(self, data, **kwargs):
        data['new'] = self.generate_shortcode()
        return data
