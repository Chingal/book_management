from backend.mongodb import db

def run():
    user_collection = db["books"]

    user_collection.create_index("title", unique=True)

    print("The book indexes were successfully created")