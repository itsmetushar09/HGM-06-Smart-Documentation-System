from config import users_collection


def save_user(user):

    users_collection.update_one(
        {"github_id": user["github_id"]},
        {"$set": user},
        upsert=True
    )
