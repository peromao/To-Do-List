from flask import Blueprint, jsonify, request
from models.task import Task
from models import db

put_routes = Blueprint('put_routes', __name__)

@put_routes.route('/task/update/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        task = Task.query.get(id)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        status = request.json.get('status')
        
        if status is None:
            return jsonify({"error": "O campo 'status' é obrigatório."}), 400
        
        if status == task.status:
            return jsonify({"message": "Status era o mesmo, sem alterações."}), 200
        
        if status not in ['pending', 'completed']:
            return jsonify({"error": "Status inválido. Use 'pending' ou 'completed'."}), 400
        
        task.status = status
        
        db.session.commit()

        return jsonify({"message": "Status da tarefa atualizado com sucesso!"})
    
    except Exception as e:
        return jsonify({"error": "Erro ao atualizar a tarefa", "details": str(e)}), 500

