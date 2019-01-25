import falcon
import json
import uuid
import logging
import time
import datetime

firstId = str(uuid.uuid4().hex)
secondId = str(uuid.uuid4().hex)

todosStore = {
    "a0a8b37ce1ee4140b12cc5bd1a59f763": {
        "id": "a0a8b37ce1ee4140b12cc5bd1a59f763",
        "complete": True,
        "name": "Take out the trash",
        "created": 1455151212,
        "completed": 1455171642
    },
    "9b7d25372dd747e190a649e1975ad3ce": {
        "id": "9b7d25372dd747e190a649e1975ad3ce",
        "complete": False,
        "name": "Buy tomatoes",
        "created": 1455151252,
        "completed": None
    }
}


class Parent():
    def __init__(self):
        pass

    def get_body(self, req):
        return req.stream.read(req.content_length or 0).decode('utf-8')

    def get_json_body(self, req):
        try:
            return json.loads(self.get_body(req))
        except json.decoder.JSONDecodeError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON')


class Todos(Parent):
    def __init__(self):  # constructor
        pass

    # on_get is because of falcon. self is becuse of python functions
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(todosStore)

    # on_post is because of falcon. self is becuse of python functions
    def on_post(self, req, resp):
        body = self.get_json_body(req)

        name = body.get('name', None)
        if name is None:
            raise falcon.HTTPError(
                falcon.HTTP_400, 'Name field cannot be empty')

        newId = uuid.uuid4().hex
        output = {
            "id": newId,
            "complete": False,
            "name": name,
            "created": int(time.time()),
            "completed": None
        }

        todosStore[newId] = output
        logging.warning(todosStore)

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(output)


class Todo(Parent):
    def __init__(self):  # constructor
        pass

    # on_get is because of falcon. self is becuse of python functions
    def on_get(self, req, resp, id):
        try:
            todo = todosStore[id]
            resp.status = falcon.HTTP_200
        except KeyError:
            resp.status = falcon.HTTP_404
            todo = {}

        resp.body = json.dumps(todo)

    # on_put is because of falcon. self is becuse of python functions
    def on_patch(self, req, resp, id):
        body = self.get_json_body(req)

        try:
            todo = todosStore[id]
        except KeyError:
            resp.status = falcon.HTTP_404
            raise falcon.HTTPError(
                falcon.HTTP_400, 'This Todo Id does not exist')

        errors = []
        todoId = body.get('id', None)
        if todoId is not None:
            errors.append('Id cannot be sent')

        name = body.get('name', None)
        if name is None:
            errors.append('Name field cannot be empty')
        elif type(name) is not str:
            errors.append('Name must be a string')

        complete = body.get('complete', None)
        if complete is None:
            errors.append('Complete field cannot be empty')

        if type(complete) is not bool:
            errors.append('Complete must be a boolean')

        created = body.get('created', None)
        newCreated = todo['created']
        if created is not None:
            try:
                datetime.datetime.fromtimestamp(created)
            except TypeError:  # throw only this try the except if TypeError
                errors.append('Created time is not valid')

            if created >= int(time.time()):
                newCreated = created
            else:
                errors.append('Created time cannot be before now')

        completed = body.get('completed', None)
        if completed is not None:
            errors.append('Completed time cannot be sent')

        if todo['complete'] is False and complete is True:
            completed = int(time.time())

        if todo['complete'] is True and complete is False:
            completed = None

        updatedTodo = {
            "id": todo['id'],
            "complete": complete,
            "name": name,
            "created": newCreated,
            "completed": completed
        }

        if len(errors):
            raise falcon.HTTPError(
                falcon.HTTP_400, 'Errors', errors)

        todosStore[id] = updatedTodo
        resp.status = falcon.HTTP_201
        resp.body = json.dumps(updatedTodo)


app = falcon.API()

todos = Todos()
todo = Todo()

app.add_route('/todos', todos)
app.add_route('/todos/{id}', todo)
