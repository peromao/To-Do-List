from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from cache import cache
from routes import register_blueprints
from flask_jwt_extended import jwt_required

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    cache.init_app(app)
    db.init_app(app)

    jwt = JWTManager(app)

    register_blueprints(app)

    @app.route('/home')
    def home():
        return render_template('index.html')
    
    @app.route('/serve_register')
    def serve_register():
        return render_template('register.html')
    
    @app.route('/')
    def login():
        return render_template('login.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
