from flask import Flask, jsonify, request
from .models import database, User, Todo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)
with app.app_context():
    database.create_all()


@app.route('/users')
def get_users():
    """ Retorna a lista de usuários """
    users = [user.to_dict() for user in User.query.all()]

    return jsonify(users), 200


@app.route('/users', methods=['POST'])
def create_user():
    """ Cria um novo usuário """
    payload = request.json

    user = User(name=payload['name'])

    database.session.add(user)
    database.session.commit()

    return jsonify(user.to_dict()), 200


@app.route('/users/<id>/todos')
def get_user_todos(id):
    """ Retorna as tarefas do usuário """
    user = User.query.get(id)

    if user is None:
        return 'Usuário não encontrado', 404

    todos = [todo.to_dict() for todo in user.todos]

    return jsonify(todos), 200


@app.route('/todos')
def get_todos():
    """ Retorna a lista de tarefas """
    todos = [todo.to_dict() for todo in Todo.query.all()]

    return jsonify(todos), 200


@app.route('/todos', methods=['POST'])
def create_todo():
    """ Cria uma nova tarefa """
    payload = request.json

    todo = Todo(task=payload['task'], user_id=payload['user_id'])

    database.session.add(todo)
    database.session.commit()

    return jsonify(todo.to_dict()), 201


@app.route('/todos/<id>')
def get_todo(id):
    """ Retorna uma tarefa específica """
    todo = Todo.query.get(id)

    if todo is None:
        return 'Tarefa não encontrada', 404

    return jsonify(todo.to_dict()), 200


@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    """ Atualiza uma tarefa específica """
    payload = request.json

    todo = Todo.query.get(id)

    if todo is None:
        return 'Tarefa não encontrada', 404

    todo.task = payload['task']
    todo.user_id = payload['user_id']

    database.session.commit()

    return jsonify(todo.to_dict()), 200


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    """ Exclui uma tarefa específica """
    todo = Todo.query.get(id)

    if todo is None:
        return 'Tarefa não encontrada', 404

    database.session.delete(todo)
    database.session.commit()

    return jsonify({}), 204
