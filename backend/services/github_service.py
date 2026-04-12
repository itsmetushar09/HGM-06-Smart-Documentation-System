import requests
from datetime import datetime

from flask import session

from config import docs_collection
from services.markdown_parser import extract_title


def fetch_repo_tree(owner, repo):

    token = session["github_token"]

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.json()["tree"]


def fetch_markdown(owner, repo, path):

    token = session["github_token"]

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.text


def save_markdown(owner, repo):

    user_id = session["github_user_id"]

    tree = fetch_repo_tree(owner, repo)

    for file in tree:

        if file["path"].endswith(".md"):

            path = file["path"]

            markdown = fetch_markdown(owner, repo, path)

            title = extract_title(markdown)

            doc_id = path.split("/")[-1].replace(".md", "")

            docs_collection.update_one(
                {
                    "user_id": user_id,
                    "repo_name": repo,
                    "doc_id": doc_id
                },
                {
                    "$set": {
                        "title": title,
                        "content": markdown,
                        "path": path,
                        "owner": owner,
                        "last_updated": datetime.utcnow()
                    }
                },
                upsert=True
            )