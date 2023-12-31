import logging.config
import requests
import hashlib
import base64
import os

from flask import Flask

from oauth_testing_flask import views
from .config import AUTHZ_ENDPOINT, CLIENT_ID


def configure_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )


def create_app(config_overrides=None):
    configure_logging()  # should be configured before any access to app.logger
    app = Flask(__name__)
    app.config.from_object("oauth_testing_flask.default_settings")
    app.config.from_prefixed_env()

    if config_overrides is not None:
        app.config.from_mapping(config_overrides)

    code_verifier = os.urandom(32)  # Generate a random 32-byte string
    code_verifier_encoded = base64.urlsafe_b64encode(
        code_verifier).rstrip(b'=').decode('utf-8')
    code_challenge = hashlib.sha256(
        code_verifier_encoded.encode('utf-8')).digest()
    code_challenge_encoded = base64.urlsafe_b64encode(
        code_challenge).rstrip(b'=').decode('utf-8')
    code_challenge_method = "plain"
    app.register_blueprint(views.bp)

    app.config["CODE_CHALLENGE"] = code_challenge_encoded
    app.config["CODE_CHALLENGE_METHOD"] = code_challenge_method
    scope = "mail.read"
    app.config["SCOPE"] = scope

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "https://127.0.0.1:5000/redirect",
        "scope": "mail.read",
        "state": "12345",
        "code_challenge": code_challenge_encoded,
        "code_challenge_method": code_challenge_method,
    }
    full_uri = requests.Request("GET", AUTHZ_ENDPOINT, params=params).prepare().url
    print(full_uri)

    return app
