import database as db
import json


def validate_data_signup(data):
    status = {
        "code": "ok",
        "errors": []
    }
    keys = data.keys()

    # verifies if the data contains the following keys
    if not('username' in keys and 'password' in keys and 'email' in keys):
        status["code"] = "failed"
        status["errors"].append('not valid request')
    else:
        existing_email = db.find_user_by_parameter(
            "email", data['email'])
        existing_username = db.find_user_by_parameter(
            "username", data['username']) != None
        print(existing_email)
        if (existing_email or existing_username):
            status['code'] = 'failed'
            if (existing_email):
                status['errors'].append('existing email')
            if (existing_username):
                status['errors'].append('existing username')

    return status


def validate_data_login(data, bcrypt):
    status = {
        "code": "ok",
        "errors": []
    }

    def change_status(error: str):
        status['code'] = 'failed'
        status['errors'].append(error)

    keys = data.keys()

    # verifies if the data contains the following keys
    if not('username' in keys and 'password' in keys):
        change_status('not valid request')
    else:
        existing_username = db.find_user_by_parameter(
            "username", data['username']) != None

        if not(existing_username):
            change_status('not existing username')

        else:
            user_info = db.find_user_by_parameter('username', data['username'])
            hashed_password = user_info['password']
            if not(bcrypt.check_password_hash(hashed_password, data['password'])):
                change_status('wrong password')

    if(status['code'] == 'ok'):
        res = db.get_user_id('username', data['username'])
        status['user_id'] = str(res)

    return status


def get_user_id(key: str, val: str):
    return db.get_user_id(key, val)


def add_user(user, bcrypt):
    # encrypts the password
    encrypted = bcrypt.generate_password_hash(user['password'])
    user['password'] = encrypted
    result = db.add_user_to_db(user)

    return result


def get_user(id):
    if not(id == 'all'):
        return db.find_user(id)

    else:
        results = db.show_users()
        response = f"results: {len(results)} \n"
        for result in results:
            response += json.dumps(result)

        return response


def del_user(id):
    return db.delete_user(id)
