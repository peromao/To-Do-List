from flask import Blueprint, jsonify, request
from models.task import Task
from models import db
from cache import cache
from auxiliary import clean_input

put_routes = Blueprint('put_routes', __name__)

@put_routes.route('/task/update/<int:id>', methods=['PUT'])
def update_task(id):
    """
    Atualiza o status de uma tarefa existente no banco de dados com base no ID fornecido.

    Parâmetros:
        id (int): O ID da tarefa que será atualizada.

    Requisição:
        A função espera uma requisição JSON contendo o campo 'status' com o valor 'pending' ou 'completed'.
        {
            "status": "pending" | "completed"
        }

    Retorno esperado:
        Uma mensagem de sucesso e o status HTTP 200:
        {
            "message": "Status da tarefa atualizado com sucesso!"
        }
    """
    try:
        task = Task.query.get(id)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        status = clean_input(request.json.get('status'))
        
        if status is None:
            return jsonify({"error": "O campo 'status' é obrigatório."}), 400
        
        if status == task.status:
            return jsonify({"message": "Status era o mesmo, sem alterações."}), 200
        
        if status not in ['pending', 'completed']:
            return jsonify({"error": "Status inválido. Use 'pending' ou 'completed'."}), 400
        
        task.status = status
        
        db.session.commit()

        cache.delete('cached_tasks')

        return jsonify({"message": "Status da tarefa atualizado com sucesso!"})
    
    except Exception as e:
        return jsonify({"error": "Erro ao atualizar a tarefa", "details": str(e)}), 500

