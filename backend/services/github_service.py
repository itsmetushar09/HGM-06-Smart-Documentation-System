import requests
from datetime import datetime
from flask import session

from config import docs_collection
from services.markdown_parser import extract_title


def github_api_request(url):

    token = session.get("github_token")

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error ({response.status_code}): {response.text}"
        )

    return response.json()


def get_default_branch(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"

    data = github_api_request(url)

    return data["default_branch"]


def fetch_repo_tree(owner, repo):

    branch = get_default_branch(owner, repo)

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    data = github_api_request(url)

    return data["tree"]




def fetch_markdown(owner, repo, branch, path):

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch markdown file: {path}"
        )

    return response.text



def save_markdown(owner, repo):

    user_id = session.get("github_user_id")

    if not user_id:
        raise Exception("User not authenticated with GitHub")

    branch = get_default_branch(owner, repo)

    tree = fetch_repo_tree(owner, repo)

    saved_docs = []

    for file in tree:

        if file["path"].lower().endswith(".md"):

            path = file["path"]

            try:

                markdown = fetch_markdown(
                    owner,
                    repo,
                    branch,
                    path
                )

                title = extract_title(markdown)

                doc_id = path.replace("/", "_").replace(".md", "")

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
                            "repo": repo,
                            "last_updated": datetime.utcnow()
                        }
                    },
                    upsert=True
                )

                saved_docs.append(path)

            except Exception as e:

                print(f"Skipping file {path}: {e}")

    return saved_docs
