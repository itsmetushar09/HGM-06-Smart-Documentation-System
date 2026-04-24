import json
import os
import time
from urllib.parse import urlparse
import requests

from flask import Blueprint, jsonify, request, session
from config import qdrant_client as client
from config import docs_collection, repos_collection
from services.rag_service import embed_and_store

docs_bp = Blueprint("docs", __name__)


# agent logging helper
def _agent_log(hypothesis_id: str, location: str, message: str, data: dict | None = None) -> None:
    try:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(root, "debug-6be4ef.log")

        payload = {
            "sessionId": "6be4ef",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }

        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

    except OSError:
        pass


_agent_log("H1", "docs_routes.py:module", "docs_routes module loaded", {})


# github request header helper
def _github_headers():

    token = session.get("github_token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def _parse_repo_reference(data):
    owner = (data.get("owner") or "").strip()
    repo = (data.get("repo") or "").strip()
    repo_url = (data.get("repoUrl") or data.get("repo_url") or "").strip()

    if owner and repo:
        return owner, repo

    if repo_url and "/" in repo_url and "github.com" not in repo_url:
        parts = [part for part in repo_url.strip("/").split("/") if part]

        if len(parts) >= 2:
            return parts[0], parts[1].removesuffix(".git")

    if repo_url:
        parsed = urlparse(repo_url)
        path_parts = [part for part in parsed.path.split("/") if part]

        if "github.com" in parsed.netloc and len(path_parts) >= 2:
            return path_parts[0], path_parts[1].removesuffix(".git")

    return "", ""


# recursive markdown fetcher
def fetch_markdown_files(owner, repo, path=""):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    r = requests.get(
        url,
        headers=_github_headers(),
        timeout=30
    )

    if r.status_code != 200:
        return []

    files = []

    for item in r.json():

        # markdown file
        if item["type"] == "file" and item["name"].lower().endswith(".md"):

            dl = requests.get(
                item["download_url"],
                headers=_github_headers(),
                timeout=30
            )

            files.append({
                "path": item["path"],
                "name": item["name"],
                "content": dl.text if dl.ok else ""
            })

        # directory → recurse
        elif item["type"] == "dir":

            files.extend(
                fetch_markdown_files(
                    owner,
                    repo,
                    item["path"]
                )
            )

    return files


# load repo route
@docs_bp.route("/docs/load-repo", methods=["POST"])
def load_repo():

    _agent_log("H2", "docs_routes.py:load_repo", "load_repo entry", {})

    data = request.get_json() or {}

    owner, repo = _parse_repo_reference(data)

    if not owner or not repo:
        return jsonify({"error": "owner/repo or a GitHub repository URL is required"}), 400

    # fetch markdown recursively
    entries = fetch_markdown_files(owner, repo)

    if not entries:
        return jsonify({
            "error": "No public markdown files found, or the repository is not accessible"
        }), 404

    embed_and_store(repo, owner, entries)


    # clear previous docs for repo
    docs_collection.delete_many({
        "repo": repo,
        "owner": owner
    })


    # insert docs into mongodb
    for file in entries:

        docs_collection.insert_one({

            "repo": repo,
            "owner": owner,
            "doc_id": file["path"],
            "title": file["name"].replace(".md", ""),
            "content": file["content"]

        })


    # track repo usage
    repos_collection.update_one(
        {"repo": repo, "owner": owner},
        {"$set": {"repo": repo, "owner": owner}},
        upsert=True
    )


    return jsonify({
        "ok": True,
        "files_loaded": len(entries),
        "owner": owner,
        "repo": repo,
        "full_name": f"{owner}/{repo}",
    })


# list docs route
@docs_bp.route("/docs", methods=["GET"])
def list_docs():

    repo = request.args.get("repo")
    owner = request.args.get("owner") or session.get("owner")

    if not repo or not owner:
        return jsonify([])


    cur = docs_collection.find(
        {
            "repo": repo,
            "owner": owner
        },
        {
            "_id": 0,
            "content": 0
        }
    )

    return jsonify(list(cur))


# get single doc route
@docs_bp.route("/docs/<path:doc_id>", methods=["GET"])
def get_doc(doc_id):

    repo = request.args.get("repo") or session.get("repo")
    owner = request.args.get("owner") or session.get("owner")

    if not repo or not owner:
        return jsonify({"content": ""})


    doc = docs_collection.find_one(
        {
            "repo": repo,
            "owner": owner,
            "doc_id": doc_id
        },
        {
            "_id": 0
        }
    )


    if not doc:
        return jsonify({"content": ""})


    return jsonify({
        "content": doc.get("content", "")
    })
