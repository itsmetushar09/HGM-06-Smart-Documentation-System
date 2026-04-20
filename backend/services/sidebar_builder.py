from config import docs_collection


def build_sidebar(user_id, repo):

    docs = docs_collection.find(
        {
            "user_id": user_id,
            "repo_name": repo
        },
        {
            "_id": 0,
            "doc_id": 1,
            "title": 1
        }
    )

    return list(docs)