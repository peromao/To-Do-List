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
    """
    Serve a página inicial quando requisitada.

    Retorno esperado:
        Renderiza e retorna a página inicial da aplicação ('index.html').
    """

    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
