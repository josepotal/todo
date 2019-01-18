import falcon
import json
import uuid
import logging
import time

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
        # is this useful/necessary?
        self.todosStore = todosStore
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


class Todo():
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
        #todo = todosStore.get(id, {})
        logging.warning(todo)

        resp.body = json.dumps(todo)

    # on_put is because of falcon. self is becuse of python functions
    def on_patch(self, req, resp, id):
        body = req.stream.read(req.content_length or 0).decode('utf-8')

        data = json.loads(body)

        updatedTodo = {}
        for x in todosStore:
            if todosStore[x].get('id') == id:
                updatedTodo = todosStore[x].update(data)
                #updatedTodo = todosStore[x].update(data)
        logging.warning(updatedTodo)

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(updatedTodo)


app = falcon.API()

todos = Todos()
todo = Todo()

app.add_route('/todos', todos)
app.add_route('/todos/{id}', todo)
