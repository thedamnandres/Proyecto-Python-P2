from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Importar y registrar Blueprints
    from .controllers.catequistas_controller import catequistas_bp
    app.register_blueprint(catequistas_bp)
    
    from .controllers.arquideosis_controller import arquideosis_bp
    app.register_blueprint(arquideosis_bp)

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
