from flask import Flask, render_template, request
from flask_cors import CORS
from markupsafe import escape  # used to get arguments from the url

import services

app = Flask(__name__)
CORS(app)

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


@app.route("/users/add")
def add():
    params = request.args
    query = {
        "name": params['name'],
        "last_name": params['lastname']
    }

    response = services.add_user(query)

    return response


@app.route("/users/find")
def find():
    query_id = request.args.get('id', default='all', type='str')
    return services.get_user(query_id)


@app.route("/users/delete")
def delete():
    query_id = request.args.get('id')
    return services.del_user(query_id)


@app.route("/api", methods=['GET', 'POST'])
def read_request():
    return request.get_json()
