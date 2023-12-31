from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request
from .config import SECRET, TOKEN_ENDPOINT, CLIENT_ID
import requests

bp = Blueprint("root", __name__)


@bp.route("/")
def index():
    app.logger.warning("sample message")
    return render_template("index.html")


@bp.route("/redirect", methods=["GET"])
def redirect():
    code = request.args.get("code")
    state = request.args.get("state")
    session_state = request.args.get("session_state")

    code_challenge = app.config["CODE_CHALLENGE"]
    code_challenge_method = app.config["CODE_CHALLENGE_METHOD"]
    scope = app.config["SCOPE"]

    print("Received code: ", code)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "*"
    }

    data = {
        "client_id": CLIENT_ID,
        "scope": scope,
        "code": code,
        "redirect_uri": "https://127.0.0.1:5000/redirect",
        "grant_type": "authorization_code",
        "code_verifier": code_challenge
    }

    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data, proxies={
        "http": "127.0.0.1:8080",
        "https": "127.0.0.1:8080"
    }, verify=False)

    token_type = response.json()["token_type"] 
    scope = response.json()["scope"]
    expires_in = response.json()["expires_in"]
    ext_expires_in = response.json()["ext_expires_in"]
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")

    return code
