import logging
import os

from flask import Flask, redirect

from api import api, commons
from api import auth
from api import manage
from api.extensions import db
from api.extensions import jwt
from api.extensions import migrate

logger = logging.getLogger(__name__)


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("api")
    app.config.from_object("api.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    configure_error_handlers(app)
    register_blueprints(app)

    return app


def configure_error_handlers(app):
    @app.errorhandler(404)
    def redirect_to_url(error):
        logger.error(error)
        return redirect(
            os.getenv("BRAND_WEBSITE"), 302
        )


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    # apispec.init_app(app, security=[{"jwt": []}])
    # apispec.spec.components.security_scheme(
    #     "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    # )
    # apispec.spec.components.schema(
    #     "PaginatedResult",
    #     {
    #         "properties": {
    #             "total": {"type": "integer"},
    #             "pages": {"type": "integer"},
    #             "next": {"type": "string"},
    #             "prev": {"type": "string"},
    #         }
    #     },
    # )
    pass


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(commons.views.blueprint)
    app.register_blueprint(api.views.blueprint)
