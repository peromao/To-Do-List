from flask import Blueprint, jsonify, request
from models.task import Task
from models import db

post_routes = Blueprint('post_routes', __name__)

@post_routes.route('/task/add', methods=['POST'])
def add_task():
    try:
        data = request.json

        allowed_fields = {'title', 'status'}
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            return jsonify({"error": f"Campos não permitidos: {', '.join(extra_fields)}"}), 400
        
        title = data.get('title')
        status = data.get('status', 'pending')
        
        if not title:
            return jsonify({"error": "O título não pode estar vazio"}), 400
        
        if status not in ['pending', 'completed']:
            return jsonify({"error": "Status inválido. Use 'pending' ou 'completed'."}), 400
        
        task = Task(title=title, status=status)
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({"message": "Tarefa adicionada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": "Erro ao adicionar a tarefa", "details": str(e)}), 500