from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from auxiliary import clean_input
from models import db
from models.user import User

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    """
    Registra um novo usuário.

    Espera um JSON na requisição com os campos 'username' e 'password'.
    Verifica se o usuário já existe. Se não existir, gera uma senha
    hash e salva o novo usuário no banco de dados. Retorna uma
    mensagem de sucesso ou erro.
    """

    data = request.json
    username = clean_input(data.get('username'))
    password = clean_input(data.get('password'))

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Usuário já existe."}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Realiza o login de um usuário.

    Espera um JSON na requisição com os campos 'username' e 'password'.
    Verifica se as credenciais estão corretas. Se sim, gera um token de
    acesso JWT e o retorna. Caso contrário, retorna um erro de
    credenciais inválidas.
    """

    data = request.json
    username = clean_input(data.get('username'))
    password = clean_input(data.get('password'))

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Credenciais inválidas."}), 401
