from flask import Flask

def create_app():
    # Crea y configura la aplicación Flask
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Importa y registra el blueprint de catequistas
    from .controllers.catequistas_controller import catequistas_bp
    app.register_blueprint(catequistas_bp)
    
    # blueprint de arquidiócesis
    from .controllers.arquideosis_controller import arquideosis_bp
    app.register_blueprint(arquideosis_bp)
    
    # blueprint de parroquias
    from .controllers.parroquias_controller import parroquia_bp
    app.register_blueprint(parroquia_bp)
    
    # blueprint de personas (MongoDB)
    from .controllers.personas_controller import personas_bp
    app.register_blueprint(personas_bp)
    
    # Ruta principal (home)
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
