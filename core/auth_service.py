from core.db import users_col


def register(username, password):
    if users_col.find_one({"username": username}):
        return False

    users_col.insert_one({
        "username": username,
        "password": password
    })
    return True


def login(username, password):
    user = users_col.find_one({
        "username": username,
        "password": password
    })

    return user  # ✅ KHÔNG có dấu ,