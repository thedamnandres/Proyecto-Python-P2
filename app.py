from flask import Flask
from controllers.catequistas_controller import catequistas_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'  # Necesario para usar `flash`
app.register_blueprint(catequistas_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
