# API

The REST API endpoint will always have its version in the URL: `/api/v1/`

## Authentication

Authentication to the API is performed via HTTP Basic Auth. The client will provide an API key as the basic auth username and will not provide a password.

## Errors

Any HTTP Status in the range of 4XX will represent an error and will be accompanied by an error object.

```HTTP
    Status: 401 Unauthorized
```
```json
    {
        "error": "BAD_CREDENTIALS",
        "message": "Helpful message"
    }
```

## Resources


## ToDo

*ToDo* objects are the base of everything… as these are ToDo apps.

### The ToDo Object

|  Attribute   |  Type      |             Description               |
|--------------|------------|---------------------------------------|
|   id         |  int       |                                       |
|   complete   |  bool      |                                       |
|   name       |  string    |                                       |
|   created    |  timestamp |                                       |
|   completed  |  timestamp |  When was marked as complete \| false |
|   notes      |  string    |  Text that can be added as a note.    |

```json
    {
        "id": 1,
        "complete": true,
        "name": "Take out the trash",
        "created": 1455151212,
        "completed": 1455171642
    }
```

### Retrieve the list of ToDO's

```HTTP
GET /todos/
```

#### Example Request

```sh
curl https://example.com/api/v1/todos/ \
-u 94558272d85d065dcfb2:
```

#### Response

```HTTP
    Status: 200 OK
```

```json
    {
        "todos": [
            {
                "id": 1,
                "complete": true,
                "name": "Take out the trash",
                "created": 1455151212,
                "completed": 1455171642,
                "notes": ""
            },
            {
                "id": 2,
                "complete": false,
                "name": "Buy milk",
                "created": 1455151212,
                "completed": false,
                "notes": "Only buy light or soy milk"
            }
        ]
    }
```

#### Parameters

|   Parameter   |   Type      |   Description   |
|---------------|-------------|-----------------|
|   complete    |   bool      |  Will filter the list by completion status |
|   since       |   timestamp |  Will return ToDos created at or after the specified UNIX timestamp. |

### Retrieve a single ToDo

```HTTP
GET /todos/:id
```

#### Example Request

```sh
curl https://example.com/api/v1/todos/1 \
-u 94558272d85d065dcfb2:
```

#### Response

```HTTP
    Status: 200 OK
```

```json
    {
        "id": 1,
        "complete": true,
        "name": "Take out the trash",
        "created": 1455151212,
        "completed": 1455171642,
        "notes": ""
    }
```

### Delete a ToDo

```HTTP
DELETE /todos/:id
```

#### Example Request

```sh
curl https://example.com/api/v1/todos/1 \
-u 94558272d85d065dcfb2: \
-X DELETE
```

#### Response

```HTTP
    Status: 200 OK
```

```json
    {
        "deleted": true,
        "id": 1
    }
```

### Update a ToDo

```HTTP
PATCH /todos/:id
```

#### Accepted Data

Must include at least one.

|  Attribute   |  Type      |
|--------------|------------|
|   complete   |  bool      |
|   name       |  string    |
|   created    |  timestamp |
|   completed  |  timestamp |
|   notes      |  string    |


#### Example Request

```sh
curl http://localhost:3000/api/v1/todos/1 \
-u 94558272d85d065dcfb2:  \
-H 'Content-Type: application/json' \
-d '{"notes":"It is starting to smell!"}' \
-X PATCH
```

#### Response

```HTTP
    Status: 200 OK
```

```json
    {
        "id": 1,
        "complete": true,
        "name": "Take out the trash",
        "created": 1455151212,
        "completed": 1455171642,
        "notes": "It is starting to smell!"
    }
```

### Create a ToDo

```HTTP
POST /todos/
```

#### Accepted Data


|  Attribute   |  Type      |  Required |
|--------------|------------|-----------|
|   name       |  string    |  true     |
|   complete   |  bool      |  false    |
|   created    |  timestamp |  false    |
|   completed  |  timestamp |  false    |
|   notes      |  string    |  false    |

#### Example Request

```sh
curl https://example.com/api/v1/todos/ \
-u 94558272d85d065dcfb2: \
-H 'Content-Type: application/json' \
-d '{"name":"Write API Docs", "created":1455171642}'
```

#### Response

```HTTP
    Status: 201 Created
```
```json
    {
        "id": 3,
        "complete": false,
        "name": "Write API Docs",
        "created": 1455151212,
        "completed": false
    }
```
