import os
import requests

from flask import Blueprint, redirect, request, session, jsonify
from dotenv import load_dotenv

from models.user_model import save_user

load_dotenv()

auth_bp = Blueprint("auth", __name__)

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


def _frontend_docs_url():
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    return f"{frontend_url}/docs"


@auth_bp.route("/auth/github/login")
def github_login():

    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&scope=repo"
    )

    return redirect(github_url)


@auth_bp.route("/auth/github/callback")
def github_callback():

    code = request.args.get("code")

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }
    )

    token_json = token_response.json()

    if "access_token" not in token_json:
        return jsonify({
            "message": "OAuth code already used or expired",
            "github_response": token_json
        }), 400

    access_token = token_json["access_token"]

    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user_data = user_response.json()

    github_id = user_data["id"]
    username = user_data["login"]

    session["github_token"] = access_token
    session["github_user_id"] = github_id
    session["username"] = username

    save_user({
        "github_id": github_id,
        "username": username,
        "access_token": access_token
    })

    print("TOKEN STORED:", access_token)
    print("SESSION:", dict(session))

    return redirect(_frontend_docs_url())

@auth_bp.route("/auth/github/repos")
def get_user_repos():

    if "github_token" not in session:
        return jsonify({"error": "User not authenticated"}), 401

    token = session["github_token"]

    repos = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
    )

    return jsonify(repos.json())
