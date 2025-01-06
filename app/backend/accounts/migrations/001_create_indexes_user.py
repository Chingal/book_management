from backend.mongodb import db

def run():
    user_collection = db["users"]

    user_collection.create_index("username", unique=True)
    user_collection.create_index("email", unique=True)

    print("The user indexes were successfully created")