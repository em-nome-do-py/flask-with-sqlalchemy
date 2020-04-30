import pytest
import cerberus

from flask_with_sqlalchemy import app
from flask_with_sqlalchemy.models import database, User, Todo


@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def seed():
    with app.app_context():
        user_1 = User(name='Usuário 1')
        user_2 = User(name='usuário 2')
        todo_1 = Todo(task='Todo 1', user=user_1)
        todo_2 = Todo(task='Todo 2', user=user_2)
        todo_3 = Todo(task='Todo 3', user=user_2)

        resources = [user_1, user_2, todo_1, todo_2, todo_3]

        for resource in resources:
            database.session.add(resource)
        database.session.commit()


def test_list_users(client, seed):
    response = client.get('/users')

    assert response.status_code == 200
    assert len(response.json) == 2

    validator = cerberus.Validator({
        'users': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {
                        'type': 'integer',
                        'required': True
                    },
                    'name': {
                        'type': 'string',
                        'required': True
                    }
                }
            }
        }
    })

    data = {'users': response.json}

    assert validator.validate(data)


def test_create_user(client, seed):
    response = client.post('/users', json={
        'name': 'Usuário 3'
    })

    assert response.status_code == 201


def test_list_todos_for_user(client, seed):
    response = client.get('/users/1/todos')

    assert response.status_code == 200
    assert len(response.json) == 1


def test_list_todos(client, seed):
    response = client.get('/todos')

    assert response.status_code == 200
    assert len(response.json) == 3


def test_create_todo(client, seed):
    response = client.post('/todos', json={
        'task': 'Todo 4',
        'user_id': 1
    })

    assert response.status_code == 201


def test_list_todos_after_created(client, seed):
    response = client.get('/todos')

    assert response.status_code == 200
    assert len(response.json) == 4


def test_get_todo_info(client, seed):
    response = client.get('/todos/1')

    assert response.status_code == 200

    validator = cerberus.Validator({
        'todo': {
            'type': 'dict',
            'schema': {
                'id': {
                    'type': 'integer',
                    'required': True
                },
                'task': {
                    'type': 'string',
                    'required': True
                },
                'user': {
                    'type': 'dict',
                    'schema': {
                        'id': {
                            'type': 'integer',
                            'required': True
                        },
                        'name': {
                            'type': 'string',
                            'required': True
                        }
                    }
                }
            }
        }
    })

    data = {'todo': response.json}

    assert validator.validate(data)
    

def test_update_todo(client, seed):
    response = client.put('/todos/1', json={
        'task': 'Nova task',
        'user_id': 2
    })

    assert response.status_code == 200
    assert response.json['task'] == 'Nova task'
    assert response.json['user']['id'] == 2


def test_delete_todo(client, seed):
    response = client.delete('/todos/1')

    assert response.status_code == 204


def test_list_todos_after_deleted(client, seed):
    response = client.get('/todos')

    assert response.status_code == 200
    assert len(response.json) == 3
