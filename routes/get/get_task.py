from flask import Blueprint, jsonify
from models.task import Task
from models import db

get_routes = Blueprint('get_routes', __name__)

@get_routes.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'status': task.status} for task in tasks])