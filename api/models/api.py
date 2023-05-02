import datetime

from api.extensions import db
from api import shortcuts


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # url column
    url = db.Column(db.String(2040), nullable=False)
    old = db.Column(db.String(2040))  # old shortcode
    new = db.Column(db.String(5), unique=True)  # new shortcode
    hits = db.Column(db.Integer, default=0)  # number of hits
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    def generate_shortcode(self):
        """
        Generate a new shortcode for the url
        """
        return shortcuts.generate_shortcode(self)

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<URL %s>' % self.old
