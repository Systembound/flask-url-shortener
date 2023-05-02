# helpers functions
import string
from random import choice

from api.extensions import db
from api.models.api import Url


def gen(url: Url) -> str:
    chars = string.ascii_letters + string.digits
    length = 3
    code = ''.join(choice(chars) for x in range(length))
    # print("Checking", code)
    exists = db.session.query(
        db.exists().where(url.new == code)).scalar()
    if not exists:
        # print("Your new code is:", code)
        return code

    code = gen(url)
    while code is None:
        code = gen(url)

    return code
