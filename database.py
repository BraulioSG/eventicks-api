import re
from pymongo import MongoClient  # Mongo db
from bson.objectid import ObjectId  # parse mongo db documents id
import bson.json_util as json_util  # parse mongo db results
import json  # manages json files

# environment variables
import os
from dotenv import load_dotenv


DATABASE_URL = os.getenv("DATABASE_URL")


# connects to MongoDB
client = MongoClient(DATABASE_URL)

# connects to the database
db = client['eventicksAPI']

# getting a collection
users = db['users']


#!PARSE DOCUMENTS
def _parse_mongo_doc(document):
    return json.loads(json_util.dumps(document))  # ! JUST KEEP IT


def add_user_to_db(user):

    saved = users.insert_one(user).inserted_id

    return _parse_mongo_doc(find_user(saved))


def get_user_id(key: str, val: str):
    res = find_user_by_parameter(key, val)
    return res["_id"]


def find_user_by_parameter(key: str, val: str):
    result = users.find_one({key: val})
    return result


def find_user(id: str):
    user = {"_id": ObjectId(id)}
    try:
        result = users.find_one(user)
        response = {
            "id": str(result["_id"]),
            "username": result['username'],
            "email": result['email'],
            "error": None
        }
        return response
    except:
        return {"error": "invalid id"}


def show_users():
    results = []

    for user in users.find():
        results.append(_parse_mongo_doc(user))

    return results


def delete_user(id: str):
    user = {"_id": ObjectId(id)}
    result = users.find_one_and_delete(user)
    return _parse_mongo_doc(result)
