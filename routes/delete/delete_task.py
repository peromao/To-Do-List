from flask import Blueprint, jsonify
from models.task import Task
from models import db
from flask_jwt_extended import jwt_required
from cache import cache

delete_routes = Blueprint('delete_routes', __name__)

@delete_routes.route('/task/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
    Remove uma tarefa do banco de dados com base no ID fornecido.

    Parâmetros:
        id (int): O ID da tarefa que será deletada.

    Retorno esperado:
        Um JSON com os detalhes da tarefa removida e o status HTTP 200:
        {
            'id': <id_da_tarefa>,
            'title': <titulo_da_tarefa>,
            'status': <status_da_tarefa>,
            "message": "Tarefa removida com sucesso!"
        }
    """
    try:
        task = Task.query.get(id)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        db.session.delete(task)
        db.session.commit()

        cache.delete('cached_tasks')
        
        return jsonify({
            'id': task.id,
            'title': task.title,
            'status': task.status,
            "message": "Tarefa removida com sucesso!"
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar a tarefa", "details": str(e)}), 500
    
@delete_routes.route('/tasks', methods=['DELETE'])
@jwt_required()
def delete_all_tasks():
    """
    Remove todas as tarefas do banco de dados.

    Retorno esperado:
        Um JSON confirmando a remoção e o status HTTP 200:
        {
            "message": "Todas as tarefas foram deletadas com sucesso!"
        }
    """
    try:
        tasks = Task.query.all()

        if not tasks:
            return jsonify({"message": "Nenhuma tarefa encontrada para deletar."}), 404

        Task.query.delete()
        db.session.commit()

        cache.delete('cached_tasks')

        return jsonify({"message": "Todas as tarefas foram deletadas com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar as tarefas", "details": str(e)}), 500