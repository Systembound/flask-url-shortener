# helpers functions
import string
from random import choice

from api.extensions import db


def generate_shortcode(url: 'import api.models.api') -> str:

    def code():
        chars = string.ascii_letters + string.digits
        length = 3
        return ''.join(choice(chars) for x in range(length))

    if url is None:
        return code()

    exists = db.session.query(
        db.exists().where(url.new == code)).scalar()
    if not exists:
        # print("Your new code is:", code)
        return code()

    code = generate_shortcode(url)
    while code is None:
        code = generate_shortcode(url)

    return code
