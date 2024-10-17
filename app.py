from flask import Flask, render_template, jsonify, request
from models import db
from models.task import Task
from routes import register_blueprints

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/todo_db'

db.init_app(app)

register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'status': task.status} for task in tasks])

@app.route('/task/delete/<int:id>', methods=['DELETE'])
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
    
@app.route('/tasks', methods=['DELETE'])
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


@app.route('/task/update/<int:id>', methods=['PUT'])
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
