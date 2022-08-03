from flask import Flask, render_template, request, json
from flask_cors import CORS  # cors policies
# from markupsafe import escape  # used to get arguments from the url
from flask_bcrypt import Bcrypt  # encryption
import services

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

"""
converter types:
string
int
float
path -> accepts slashes
uuid -> UUID strings

"""


@app.route("/", methods=['GET', 'POST'])
def index():
    return "home"
    # return render_template("index/index.html")


@app.route("/users/signup", methods=['POST'])
def signup():
    req = request.get_json()
    status = services.validate_data_signup(req)

    if (status['code'] == 'ok'):
        post_request = {
            "username": req["username"],
            "password": req["password"],
            "email": req["email"]
        }

        services.add_user(post_request, bcrypt)
        status['user_id'] = str(
            services.get_user_id('username', req['username'])
        )

    res = app.response_class(
        response=json.dumps(status),
        status=200,
        mimetype="application/json"
    )
    return res


@app.route("/users/login", methods=['GET', 'POST'])
def login():
    req = request.get_json()
    status = services.validate_data_login(req, bcrypt)

    res = app.response_class(
        response=json.dumps(status),
        status=200,
        mimetype="application/json"
    )
    return res


@ app.route("/users/add")
def add():
    params = request.args
    query = {
        "name": params['name'],
        "last_name": params['lastname']
    }

    response = services.add_user(query)

    return response


@ app.route("/users/find")
def find():
    query_id = request.args.get('id')
    data = services.get_user(query_id)

    res = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype="application/json"
    )
    return res


@app.route("/users/findall")
def findAll():
    return services.get_user('all')


@ app.route("/users/delete")
def delete():
    query_id = request.args.get('id')
    return services.del_user(query_id)


@ app.route("/api", methods=['GET', 'POST'])
def read_request():
    return request.get_json()
