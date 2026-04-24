import base64
from urllib.parse import quote, urlparse

import requests
from flask import Blueprint, jsonify, request, session

from config import docs_collection, repos_collection
from services.rag_service import embed_and_store

docs_bp = Blueprint("docs", __name__)


def _github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    token = session.get("github_token")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def _parse_repo_reference(data):
    owner = (data.get("owner") or "").strip()
    repo = (data.get("repo") or "").strip()
    repo_url = (data.get("repoUrl") or data.get("repo_url") or "").strip()

    if owner and repo:
        return owner, repo

    if repo_url.startswith("git@github.com:"):
        repo_path = repo_url.removeprefix("git@github.com:").strip("/")
        parts = [part for part in repo_path.split("/") if part]

        if len(parts) >= 2:
            return parts[0], parts[1].removesuffix(".git")

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


def _github_get(url):
    return requests.get(url, headers=_github_headers(), timeout=30)


def _github_error_message(response):
    if response.status_code == 404:
        return "Repository not found, private, or inaccessible."

    if response.status_code == 403:
        if response.headers.get("X-RateLimit-Remaining") == "0":
            return "GitHub API rate limit reached. Please wait and try again."

        return "GitHub denied the request. Please try again in a moment."

    try:
        payload = response.json()
        message = payload.get("message")
    except ValueError:
        message = None

    return message or "GitHub request failed."


def _is_markdown_path(path):
    lowered = path.lower()
    return lowered.endswith(".md") or lowered.endswith(".mdx") or lowered.endswith(".markdown")


def _decode_blob_content(content):
    cleaned = "".join(content.splitlines())
    decoded = base64.b64decode(cleaned)
    return decoded.decode("utf-8", errors="replace")


def fetch_markdown_files(owner, repo):
    repo_response = _github_get(f"https://api.github.com/repos/{owner}/{repo}")

    if repo_response.status_code != 200:
        return [], _github_error_message(repo_response), repo_response.status_code

    repo_info = repo_response.json()
    default_branch = repo_info.get("default_branch")

    if not default_branch:
        return [], "Could not determine the repository default branch.", 502

    tree_response = _github_get(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/{quote(default_branch, safe='')}?recursive=1"
    )

    if tree_response.status_code != 200:
        return [], _github_error_message(tree_response), tree_response.status_code

    tree = tree_response.json().get("tree", [])
    markdown_files = sorted(
        [
            item for item in tree
            if item.get("type") == "blob" and _is_markdown_path(item.get("path", ""))
        ],
        key=lambda item: item["path"].lower()
    )

    if not markdown_files:
        return [], "No markdown files were found in this public repository.", 404

    entries = []
    fetch_errors = 0

    for item in markdown_files:
        sha = item.get("sha")

        if not sha:
            fetch_errors += 1
            continue

        blob_response = _github_get(f"https://api.github.com/repos/{owner}/{repo}/git/blobs/{sha}")

        if blob_response.status_code != 200:
            fetch_errors += 1
            continue

        blob = blob_response.json()
        content = blob.get("content", "")

        entries.append({
            "path": item["path"],
            "name": item["path"].split("/")[-1],
            "content": _decode_blob_content(content) if content else ""
        })

    if not entries:
        if fetch_errors:
            return [], "Markdown files were found, but their contents could not be fetched.", 502

        return [], "No markdown files were found in this public repository.", 404

    return entries, "", 200


@docs_bp.route("/docs/load-repo", methods=["POST"])
def load_repo():
    data = request.get_json() or {}
    owner, repo = _parse_repo_reference(data)

    if not owner or not repo:
        return jsonify({"error": "owner/repo or a GitHub repository URL is required"}), 400

    entries, error_message, status_code = fetch_markdown_files(owner, repo)

    if not entries:
        return jsonify({"error": error_message}), status_code

    embed_and_store(repo, owner, entries)

    docs_collection.delete_many({"repo": repo, "owner": owner})

    for file in entries:
        docs_collection.insert_one({
            "repo": repo,
            "owner": owner,
            "doc_id": file["path"],
            "title": file["name"].rsplit(".", 1)[0],
            "content": file["content"]
        })

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


@docs_bp.route("/docs", methods=["GET"])
def list_docs():
    repo = request.args.get("repo")
    owner = request.args.get("owner") or session.get("owner")

    if not repo or not owner:
        return jsonify([])

    cur = docs_collection.find(
        {"repo": repo, "owner": owner},
        {"_id": 0, "content": 0}
    )

    return jsonify(list(cur))


@docs_bp.route("/docs/<path:doc_id>", methods=["GET"])
def get_doc(doc_id):
    repo = request.args.get("repo") or session.get("repo")
    owner = request.args.get("owner") or session.get("owner")

    if not repo or not owner:
        return jsonify({"content": ""})

    doc = docs_collection.find_one(
        {"repo": repo, "owner": owner, "doc_id": doc_id},
        {"_id": 0}
    )

    if not doc:
        return jsonify({"content": ""})

    return jsonify({"content": doc.get("content", "")})
