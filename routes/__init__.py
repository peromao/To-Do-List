from .post.post_task import post_routes

def register_blueprints(app):
    app.register_blueprint(post_routes)
