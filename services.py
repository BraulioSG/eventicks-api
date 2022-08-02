import database
import json


def connection():

    return "connected"


def add_user(user):
    result = database.add_user_to_db(
        {
            "name": user['name'],
            "last_name": user['last_name']
        })

    return result


def get_user(id):
    if not(id == 'all'):
        return database.find_user(id)

    else:
        results = database.show_users()
        response = f"results: {len(results)} \n"
        for result in results:
            response += json.dumps(result)

        return response


def del_user(id):
    return database.delete_user(id)
