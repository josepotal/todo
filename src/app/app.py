import falcon


class Todos():
    def __init__(self): #constructor
        pass

    def on_get(self, req, resp): # because of falcon
        resp.status = falcon.HTTP_200
        resp.body = "Hello world"
        pass

app = falcon.API()

todos = Todos()

app.add_route('/todos', todos)
