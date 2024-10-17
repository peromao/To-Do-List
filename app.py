from flask import Flask, render_template, jsonify, request
from models import db
from models.task import Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/todo_db'

db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/task/add', methods=['POST'])
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
        
        task = Task(title=title, status=status)
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({"message": "Tarefa adicionada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": "Erro ao adicionar a tarefa", "details": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
