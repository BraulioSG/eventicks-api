from pymongo import MongoClient  # Mongo db
from bson.objectid import ObjectId  # parse mongo db documents id
import bson.json_util as json_util  # parse mongo db results
import json  # manages json files


# connects to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# connects to the database
db = client['eventicksAPI']

# getting a collection
collection = db['users']


#!PARSE DOCUMENTS
def _parse_mongo_doc(document):
    return json.loads(json_util.dumps(document))  # ! JUST KEEP IT


def add_user_to_db(user):
    post = {
        "name": user['name'],
        "last_name":  user['last_name']
    }

    saved = collection.insert_one(post).inserted_id

    return _parse_mongo_doc(find_user(saved))


def find_user(id):
    user = {"_id": ObjectId(id)}
    result = collection.find_one(user)
    return _parse_mongo_doc(result)


def show_users():
    results = []

    for user in collection.find():
        results.append(_parse_mongo_doc(user))

    return results


def delete_user(id):
    user = {"_id": ObjectId(id)}
    result = collection.find_one_and_delete(user)
    return _parse_mongo_doc(result)
