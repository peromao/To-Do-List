from .post.post_task import post_routes
from .get.get_task import get_routes

def register_blueprints(app):
    app.register_blueprint(post_routes)
    app.register_blueprint(get_routes)
