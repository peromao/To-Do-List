from models import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="pending")

    def __repr__(self):
        return f'<Task {self.title}>'
