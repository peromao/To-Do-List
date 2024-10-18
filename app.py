from flask import Flask, render_template
from models import db
from routes import register_blueprints
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=Config.DEBUG)
