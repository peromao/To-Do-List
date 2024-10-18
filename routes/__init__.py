from .post.post_task import post_routes
from .get.get_task import get_routes
from .delete.delete_task import delete_routes
from .put.update_task import put_routes

def register_blueprints(app):
    app.register_blueprint(post_routes)
    app.register_blueprint(get_routes)
    app.register_blueprint(delete_routes)
    app.register_blueprint(put_routes)
