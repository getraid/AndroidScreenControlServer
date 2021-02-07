import logging
from flask import Flask, make_response, render_template, jsonify, request
from flask_cors import CORS
import dataset
import random
import math
import os
from sqlalchemy.pool import SingletonThreadPool
from flask import request

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

tableTodo = db['todo']
tableNotes = db['notes']


def getrandomzitat():
    sizeZ = len(zitate)
    flori = math.floor(random.random()*300)
    chosenZitat = flori % sizeZ
    return zitate[chosenZitat]


def fetch_db(table, id):
    return table.find_one(id=id)


def fetch_db_all(table):
    items = []
    if(table == None):
        return None
    if(table == "All"):
        table = tableTodo
        items = []
        for item in table:
            items.append(item)
        table = tableNotes
    for item in table:
        items.append(item)
    return items


def fetch_db_afterPost_Todo(content):
    lastObjIndex = int(len(list(tableTodo.all())))
    return fetch_db(tableTodo, lastObjIndex)


def fetch_db_afterPostNotes(content):
    lastObjIndex = int(len(list(tableNotes.all())))
    return fetch_db(tableNotes, lastObjIndex)

# Check if request filetypes are matching (application/json)
# TODO: Should be checking if it's using the correct table ¯\_(ツ)_/¯


def postDB_verify(content):
    if (isinstance(content['message'], str)):
        return content
    else:
        return None


def putDB_verify(content, id):
    postDB_verify(content)
    if not "id" in content:
        content['id'] = id
    return content


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


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
    tableTodo.insert({
        "done": False,
        "message": "Demotask"
    })

    tableNotes.insert({
        "message": "This is a demo note"
    })

    return make_response(jsonify(fetch_db_all("All")), 200)


@app.route('/api/todos', methods=['GET', 'POST'])
def api_todos():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all(tableTodo)), 200)
    elif request.method == 'POST':
        content = request.json
        localC = postDB_verify(content)
        tableTodo.insert(localC)
        # 201 = Created
        return make_response(jsonify(content), 201)


@app.route('/api/todos/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_todo_id(id):
    if request.method == "GET":
        todo_obj = fetch_db(tableTodo, id)
        if todo_obj:
            return make_response(jsonify(todo_obj), 200)
        else:
            return make_response(jsonify(todo_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        putC = putDB_verify(content, id)
        tableTodo.update(putC, ['id'])
        todo_obj = fetch_db(tableTodo, id)
        return make_response(jsonify(todo_obj), 200)
    elif request.method == "DELETE":
        tableTodo.delete(id=id)
        return make_response(jsonify({}), 204)


@app.route('/api/notes', methods=['GET', 'POST'])
def api_notes():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all(tableNotes)), 200)
    elif request.method == 'POST':
        content = request.json
        localC = postDB_verify(content)
        tableNotes.insert(localC)
        # 201 = Created
        return make_response(jsonify(content), 201)


@app.route('/api/notes/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_notes_id(id):
    if request.method == "GET":
        note_obj = fetch_db(tableNotes, id)
        if note_obj:
            return make_response(jsonify(note_obj), 200)
        else:
            return make_response(jsonify(note_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        putC = putDB_verify(content, id)
        tableNotes.update(putC, ['id'])
        note_obj = fetch_db(tableNotes, id)
        return make_response(jsonify(note_obj), 200)
    elif request.method == "DELETE":
        tableNotes.delete(id=id)
        return make_response(jsonify({}), 204)


def startServer(whost, wport):
    app.run(debug=False, host=whost, port=wport, threaded=True)


if (__name__ == "__main__"):
    startServer('0.0.0.0', 5000)
