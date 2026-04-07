from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError

# Add todo tests

def test_add_todo_success(authenticated_user):
    client, token = authenticated_user
    response = client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    assert response.status_code == 201

def test_add_todo_without_token(authenticated_user):
    client, _token = authenticated_user
    response = client.post('/api/todos', json={
        "text": "Pick up some bacon",
        "completed": True
    })
    assert response.status_code == 401

def test_add_todo_without_text(authenticated_user):
    client, token = authenticated_user
    response = client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "completed": True
    })
    assert response.status_code == 400

def test_add_todo_with_empty_text(authenticated_user):
    client, token = authenticated_user
    response = client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "",
        "completed": True
    })
    assert response.status_code == 400

# Get todos tests
def test_get_todo_success_with_todos(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    response = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = response.get_json()
    assert response.status_code == 200 and data

def test_get_todo_success_without_todos(authenticated_user):
    client, token = authenticated_user
    response = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = response.get_json()
    assert response.status_code == 200 and data == []

def test_get_todo_success_without_token(authenticated_user):
    client, _token = authenticated_user
    client.post('/api/todos', json={
        "text": "Pick up some bacon",
        "completed": True
    })
    response = client.get('/api/todos')
    assert response.status_code == 401

# Delete todos tests
def test_delete_todo_success(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_todo = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_todo.get_json()
    todo_id = data[0]['id']
    response = client.delete(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200

def test_delete_todo_not_found(authenticated_user):
    client, token = authenticated_user
    client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    todo_id = "id-not-found"
    response = client.delete(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 404

def test_delete_todo_doesnt_belong_to_user(authenticated_user):
    client_1, token_1 = authenticated_user
    client_2, token_2 = authenticated_user
    client_2.post('/api/auth/register', json={
    "email": "test2@test.com",
    "password": "Test123!"
    })
    other_login = client_2.post('/api/auth/login', json={
    "email": "test2@test.com",
    "password": "Test123!"
    })
    data_2 = other_login.get_json()
    token_2 = data_2['access_token']
    response = client_1.post('/api/todos', headers={
        'Authorization': f'Bearer {token_1}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_todo = client_1.get('/api/todos', headers={
        'Authorization': f'Bearer {token_1}'
    })
    data_1 = get_todo.get_json()
    todo_id = data_1[0]['id']
    response = client_1.delete(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token_2}'
    })
    assert response.status_code == 400

def test_delete_todo_without_token(authenticated_user):
    client, _token = authenticated_user
    client.post('/api/todos', json={
        "text": "Pick up some bacon",
        "completed": True
    })
    todo_id = "id-wharever"
    response = client.delete(f'/api/todos/{todo_id}')
    assert response.status_code == 401

def test_delete_todo_500(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_todo = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_todo.get_json()
    todo_id = data[0]['id']

    with patch('controllers.todos_controller.db.session.commit', side_effect=SQLAlchemyError("Database error")):
        response = client.delete(f'/api/todos/{todo_id}', headers={
            'Authorization': f'Bearer {token}'
        })

    assert response.status_code == 500

# reorder todos tests
def test_reorder_todo_success(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some eggs",
        "completed": True
    })
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some milk",
        "completed": False
    })
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some tortillas",
        "completed": False
    })
    get_response = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response.get_json()
    todo_id_bacon = data[0]['id']
    todo_id_eggs = data[1]['id']
    todo_id_milk = data[2]['id']
    todo_id_tortillas = data[3]['id']

    response = client.put('/api/todos/reorder', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "data": [todo_id_tortillas, todo_id_milk, todo_id_eggs, todo_id_bacon]
    })

    get_response_after = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response_after.get_json()
    assert response.status_code == 200 and (data[0]['id'] == todo_id_tortillas and data[1]['id'] == todo_id_milk and data[2]['id'] == todo_id_eggs and data[3]['id'] == todo_id_bacon)

def test_reorder_todo_without_token(authenticated_user):
    client, _token = authenticated_user
    client.post('/api/todos', json={
        "text": "Pick up some bacon",
        "completed": True
    })
    client.post('/api/todos', json={
        "text": "Pick up some eggs",
        "completed": True
    })
    client.post('/api/todos', json={
        "text": "Pick up some milk",
        "completed": False
    })
    client.post('/api/todos', json={
        "text": "Pick up some tortillas",
        "completed": False
    })
    todo_id_bacon = "id-lol"
    todo_id_eggs = "id-2"
    todo_id_milk = "super-id"
    todo_id_tortillas = "another-id"

    response = client.put('/api/todos/reorder', json={
        "data": [todo_id_tortillas, todo_id_milk, todo_id_eggs, todo_id_bacon]
    })

    _get_response_after = client.get('/api/todos')
    assert response.status_code == 401

# Update todos tests
def test_update_todo_with_text(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_response = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response.get_json()
    todo_id = data[0]['id']
    response = client.patch(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token}'
    },  json={
        "text": "Pick up some eggs"
    })
    get_response_after = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response_after.get_json()
    todo_text = data[0]['text']
    assert response.status_code == 200 and todo_text == "Pick up some eggs"

def test_update_todo_with_completed(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_response = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response.get_json()
    todo_id = data[0]['id']
    response = client.patch(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token}'
    },  json={
        "completed": False
    })
    get_response_after = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_response_after.get_json()
    todo_check = data[0]['completed']
    assert response.status_code == 200 and todo_check is False

def test_update_todo_not_found(authenticated_user):
    client, token = authenticated_user
    todo_id = "some-id"
    response = client.patch(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token}'
    },  json={
        "completed": False
    })
    assert response.status_code == 404

def test_update_todo_doesnt_belong_to_user(authenticated_user):
    client_1, token_1 = authenticated_user
    client_2, token_2 = authenticated_user
    client_2.post('/api/auth/register', json={
    "email": "test2@test.com",
    "password": "Test123!"
    })
    other_login = client_2.post('/api/auth/login', json={
    "email": "test2@test.com",
    "password": "Test123!"
    })
    data_2 = other_login.get_json()
    token_2 = data_2['access_token']
    response = client_1.post('/api/todos', headers={
        'Authorization': f'Bearer {token_1}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_todo = client_1.get('/api/todos', headers={
        'Authorization': f'Bearer {token_1}'
    })
    data_1 = get_todo.get_json()
    todo_id = data_1[0]['id']
    response = client_1.patch(f'/api/todos/{todo_id}', headers={
        'Authorization': f'Bearer {token_2}'
    }, json={
        "text": "Pick up some eggs",
        "completed": False
    })
    assert response.status_code == 400

def test_update_without_token(authenticated_user):
    client, _token = authenticated_user
    client.post('/api/todos', json={
        "text": "Pick up some bacon",
        "completed": True
    })
    todo_id = "id-fake"
    response = client.patch(f'/api/todos/{todo_id}',  json={
        "completed": False
    })
    assert response.status_code == 401

def test_update_todo_500(authenticated_user):
    client, token = authenticated_user
    client.post('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        "text": "Pick up some bacon",
        "completed": True
    })
    get_todo = client.get('/api/todos', headers={
        'Authorization': f'Bearer {token}'
    })
    data = get_todo.get_json()
    todo_id = data[0]['id']

    with patch('controllers.todos_controller.db.session.commit', side_effect=SQLAlchemyError("Database error")):
        response = client.patch(f'/api/todos/{todo_id}', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            "text": "Pick up some eggs",
            "completed": False
        })

    assert response.status_code == 500
