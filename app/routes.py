from flask import Blueprint, render_template

# Blueprint para las rutas principales (home)
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    # Renderiza la página principal de inicio
    return render_template('index.html')
