import falcon
import json
import logging
import time
import datetime
import falcon_cors
import psycopg2
from psycopg2.extras import RealDictCursor


cors = falcon_cors.CORS(
    allow_origins_list=['http://localhost:4200'], allow_all_methods=True, allow_all_headers=True)


class Parent():
    def __init__(self, connection):
        self.connection = connection
        pass

    def get_body(self, req):
        return req.stream.read(req.content_length or 0).decode('utf-8')

    def get_json_body(self, req):
        try:
            return json.loads(self.get_body(req))
        except json.decoder.JSONDecodeError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON')

    def date_handler(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif obj is None:
            return obj
        else:
            raise TypeError


class Todos(Parent):
    # def __init__(self):  # constructor
    #     pass

    # on_get is because of falcon. self is becuse of python functions

    def on_get(self, req, resp):

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM todos ORDER BY created DESC")
        todos = cursor.fetchall()

        self.connection.commit()
        cursor.close()
        logging.warning(todos)

        resp.status = falcon.HTTP_200

        resp.body = json.dumps(todos, default=self.date_handler)

    # on_post is because of falcon. self is becuse of python functions
    def on_post(self, req, resp):
        body = self.get_json_body(req)

        name = body.get('name', None)
        if name is None:
            raise falcon.HTTPError(
                falcon.HTTP_400, 'Name field cannot be empty')

        newTodo = {
            "name": name
        }

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            INSERT INTO todos (name) VALUES ('{name}') RETURNING id,name, created, completed, complete
        """.format(name=newTodo.get('name')))

        # sql_string = "INSERT INTO todos (name) VALUES (%s) RETURNING id;"
        # cursor.execute(sql_string, (newTodo.get('name')))

        output = cursor.fetchone()
        logging.warning(output)
        self.connection.commit()
        cursor.close()

        resp.status = falcon.HTTP_201

        resp.body = json.dumps(output, default=self.date_handler)


class Todo(Parent):
    # def __init__(self):  # constructor
    #     pass

    # on_get is because of falcon. self is because of python functions
    def on_get(self, req, resp, id):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM todos WHERE id={id}
                """.format(id=id))

            todo = cursor.fetchone()

            self.connection.commit()
            cursor.close()
            logging.warning(todos)

            resp.status = falcon.HTTP_200
        except KeyError:
            resp.status = falcon.HTTP_404
            todo = {}

        resp.body = json.dumps(todo, default=self.date_handler)

    # on_put is because of falcon. self is because of python functions
    def on_patch(self, req, resp, id):
        body = self.get_json_body(req)

        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT * FROM todos WHERE id={id}
                """.format(id=id))
            todo = cursor.fetchone()

        except KeyError:
            resp.status = falcon.HTTP_404
            raise falcon.HTTPError(
                falcon.HTTP_400, 'This Todo Id does not exist')

        errors = []
        todoId = body.get('id', None)
        if todoId is not None:
            errors.append('Id cannot be sent')

        name = body.get('name', todo['name'])
        if name is None and todo['name'] is None:
            errors.append('Name field cannot be empty')
        elif type(name) is not str:
            errors.append('Name must be a string')

        complete = body.get('complete', None)
        if complete is None:
            errors.append('Complete field cannot be empty')

        if type(complete) is not bool:
            errors.append('Complete must be a boolean')

        created = body.get('created', None)

        if created is not None:
            try:
                datetime.datetime.fromtimestamp(created)
            except TypeError:  # throw onºy this try the except if TypeError
                errors.append('Created time is not valid')

            if created >= int(time.time()):
                newCreated = created
            else:
                errors.append('Created time cannot be before now')

        completed = body.get('completed', None)
        if completed is not None:
            errors.append('Completed time cannot be sent')

        if todo['completed'] is None and complete is True:
            completed = datetime.datetime.now()

        if todo['completed'] is None and complete is False:
            completed = None

        if todo['complete'] is True and complete is False:
            completed = None

        updatedTodo = {
            "id": todo['id'],
            "complete": complete,
            "name": name,
            "completed": completed,
        }

        if len(errors):
            raise falcon.HTTPError(
                falcon.HTTP_400, 'Errors', errors)

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)

        if complete is True:
            cursor.execute("""
                UPDATE todos SET name=('{name}'),completed=('{completed}'),complete=('{complete}') WHERE id = ('{id}') RETURNING id, name, created, completed, complete
            """.format(name=updatedTodo.get('name'), completed=updatedTodo.get('completed'), complete=updatedTodo.get('complete'), id=updatedTodo.get('id')))
        else:
            cursor.execute("""
                UPDATE todos SET name=('{name}'),completed=NULL,complete=('{complete}') WHERE id = ('{id}') RETURNING id, name, created, completed, complete
            """.format(name=updatedTodo.get('name'), complete=updatedTodo.get('complete'), id=updatedTodo.get('id')))

        output = cursor.fetchone()

        logging.warning(output)
        self.connection.commit()
        cursor.close()

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(output, default=self.date_handler)

    def on_delete(self, req, resp, id):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                DELETE FROM todos WHERE id={id}
                """.format(id=id))

            self.connection.commit()
            cursor.close()

            resp.status = falcon.HTTP_200
        except KeyError:
            resp.status = falcon.HTTP_404

        resp.body = json.dumps({"message": "deleted"})


# // connection to db
def connect_to_database():
    def _do_connnect():
        logging.warning('trying to connect')
        connection = psycopg2.connect(
            dbname='todos',
            user='postgres',
            password='',
            host='database'
        )
        return connection

    tries = 0
    connection = False

    while not connection:
        try:
            connection = _do_connnect()
        except psycopg2.OperationalError as e:
            logging.warning(
                'Database not available, waiting try: {}'.format(tries))

            if tries > 5:
                raise e

            time.sleep(2)
        finally:
            tries += 1

    logging.warning('database available')
    return connection


connection = connect_to_database()

app = falcon.API(middleware=[cors.middleware])

todos = Todos(connection)
todo = Todo(connection)

app.add_route('/todos', todos)
app.add_route('/todos/{id}', todo)
