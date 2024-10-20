from flask import Blueprint, jsonify
from models.task import Task
from cache import cache

get_routes = Blueprint('get_routes', __name__)

@get_routes.route('/tasks', methods=['GET'])
@cache.cached(timeout=60, key_prefix='cached_tasks')
def list_tasks():
    """
    Retorna a lista de todas as tarefas no banco de dados.
    
    Retorno esperado:
        Retorna um JSON com a lista de tarefas e o status HTTP 200:
        [
            {
                'id': <id_da_tarefa>,
                'title': <titulo_da_tarefa>,
                'status': <status_da_tarefa>
            },
            ...
        ]
    """
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'status': task.status} for task in tasks])