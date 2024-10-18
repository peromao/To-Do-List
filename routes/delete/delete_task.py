from flask import Blueprint, jsonify
from models.task import Task
from models import db

delete_routes = Blueprint('delete_routes', __name__)

@delete_routes.route('/task/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.query.get(id)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        db.session.delete(task)
        db.session.commit()
        
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
def delete_all_tasks():
    try:
        tasks = Task.query.all()

        if not tasks:
            return jsonify({"message": "Nenhuma tarefa encontrada para deletar."}), 404

        Task.query.delete()
        db.session.commit()

        return jsonify({"message": "Todas as tarefas foram deletadas com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro ao deletar as tarefas", "details": str(e)}), 500