import falcon


class Todos():
    def __init__(self): #constructor
        pass

    def on_get(self, req, resp): # because of falcon
        todo = {
            "id": 1,
            "complete": True,
            "name": "Take out the trash",
            "created": 1455151212,
            "completed": 1455171642
        }
        print(todo)
        resp.status = falcon.HTTP_200
        resp.body = "Hello world"
        pass

app = falcon.API()

todos = Todos()

app.add_route('/todos', todos)
