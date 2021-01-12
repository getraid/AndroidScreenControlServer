import logging
from flask import Flask, make_response, render_template, jsonify, request
from flask_cors import CORS
import dataset
import random
import math
import os
from sqlalchemy.pool import SingletonThreadPool

app = Flask(__name__, static_url_path='',
            static_folder='static')
CORS(app)

tpath = 'Modules/TodoServer/sqlite.db'
if not os.path.isdir('Modules'):
    tpath = 'sqlite.db'

db = dataset.connect(url='sqlite:///' + tpath,
                     engine_kwargs={'connect_args': {'check_same_thread': False}})

log = logging.getLogger('werkzeug')
log.setLevel(logging.FATAL)


zitate = []

tpath = 'Modules/TodoServer/zitate.txt'
if os.path.isfile('zitate.txt'):
    tpath = 'zitate.txt'
f = open(tpath, "rb")
for x in f:
    zitate.append(x)
f.close()

table = db['todo']


def fetch_db(id):
    return table.find_one(id=id)


def getrandomzitat():
    sizeZ = len(zitate)
    flori = math.floor(random.random()*300)
    chosenZitat = flori % sizeZ
    return zitate[chosenZitat]


def fetch_db_all():
    todos = []
    for todo in table:
        todos.append(todo)
    return todos


def fetch_db_afterPost(content):
    lastObjIndex = int(len(list(table.all())))
    return fetch_db(lastObjIndex)

# Check if request filetypes are matching (application/json)


def postDB_verify(content):
    if (isinstance(content['done'], bool) and isinstance(content['message'], str)):
        return content
    else:
        return None


def putDB_verify(content, id):
    postDB_verify(content)
    if not "id" in content:
        content['id'] = id
    return content


@app.route('/api/motivationalsentence', methods=['GET'])
def motivationszitat():
    return make_response((getrandomzitat()),
                         200)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    # return make_response("",200)


@app.route('/api/db_populate', methods=['GET'])
def db_populate():
    table.insert({
        "done": False,
        "message": "Demotask"
    })

    return make_response(jsonify(fetch_db_all()),
                         200)


@app.route('/api/todos', methods=['GET', 'POST'])
def api_todos():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        localC = postDB_verify(content)
        table.insert(localC)
        # 201 = Created
        return make_response(jsonify(fetch_db_afterPost(content)), 201)


@app.route('/api/todos/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(id):
    if request.method == "GET":
        todo_obj = fetch_db(id)
        if todo_obj:
            return make_response(jsonify(todo_obj), 200)
        else:
            return make_response(jsonify(todo_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        putC = putDB_verify(content, id)
        table.update(putC, ['id'])
        todo_obj = fetch_db(id)
        return make_response(jsonify(todo_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=id)
        return make_response(jsonify({}), 204)


def startServer(whost, wport):
    app.run(debug=False, host=whost, port=wport, threaded=True)


if (__name__ == "__main__"):
    startServer('0.0.0.0', 5000)
