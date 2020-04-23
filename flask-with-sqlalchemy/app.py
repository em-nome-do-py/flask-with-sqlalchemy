from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/users')
def get_users():
    """ Retorna a lista de usuários """
    return jsonify([
        {'id': 1, 'name': 'Usuário 1'},
        {'id': 2, 'name': 'Usuário 2'},
        {'id': 3, 'name': 'Usuário 3'}
    ]), 200


@app.route('/users', methods=['POST'])
def create_user():
    """ Retorna a lista de usuários """
    return jsonify({
        'id': 1, 
        'name': 'Usuário 1'
    }), 201


@app.route('/users/<id>/todos')
def get_user_todos(id):
    """ Retorna as tarefas do usuário """
    return jsonify([
        {'id': 1, 'task': 'Criar o CRUD'},
        {'id': 2, 'task': 'Criar os modelos do ORM'}
    ]), 200


@app.route('/todos')
def get_todos():
    """ Retorna a lista de tarefas """
    return jsonify([
        {
            'id': 1, 
            'task': 'Criar o CRUD', 
            'user': {
                'id': 1,
                'name': 'Usuário 1'
            }
        },
        {
            'id': 2, 
            'task': 'Criar os modelos do ORM', 
            'user': {
                'id': 1,
                'name': 'Usuário 1'
            }
        }
    ]), 200


@app.route('/todos', methods=['POST'])
def create_todo():
    """ Cria uma nova tarefa """
    return jsonify({
        'id': 3, 
        'task': 'Nova tarefa', 
        'user': {
            'id': 1,
            'name': 'Usuário 1'
        }
    }), 201


@app.route('/todos/<id>')
def get_todo(id):
    """ Retorna uma tarefa específica """
    return jsonify({
        'id': 1,
        'task': 'Criar o CRUD',
        'user': {
            'id': 1,
            'name': 'Usuário 1'
        }
    }), 200


@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    """ Atualiza uma tarefa específica """
    return jsonify({
        'id': 3,
        'task': 'Tarefa alterada',
        'user': {
            'id': 1,
            'name': 'Usuário 1'
        }
    }), 200


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    """ Exclui uma tarefa específica """
    return jsonify({}), 204
