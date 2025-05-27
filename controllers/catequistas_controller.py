from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.catequistas_model import CatequistasModel

catequistas_bp = Blueprint('catequistas', __name__)
modelo = CatequistasModel()

# Redirige al listado de catequistas al acceder a la raíz
@catequistas_bp.route('/')
def index():
    return redirect(url_for('catequistas.listar'))

# Listar todos los catequistas
@catequistas_bp.route('/catequistas')
def listar():
    datos = modelo.listar()
    return render_template('listar.html', catequistas=datos)

# Ruta para agregar un nuevo catequista
@catequistas_bp.route('/catequistas/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            modelo.insertar(
                request.form['nombres'],
                request.form['apellidos'],
                request.form['rol'],
                request.form['telefono'],
                request.form['correo'],
                request.form['direccion']
            )
            flash('Catequista agregado exitosamente!', 'success')
        except Exception as e:
            flash(f'Error al agregar el catequista: {e}', 'danger')
        return redirect(url_for('catequistas.listar'))
    return render_template('form.html')

# Ruta para editar un catequista
@catequistas_bp.route('/catequistas/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        try:
            modelo.actualizar(
                id,
                request.form['telefono'],
                request.form['correo']
            )
            flash('Catequista actualizado exitosamente!', 'success')
        except Exception as e:
            flash(f'Error al actualizar el catequista: {e}', 'danger')
        return redirect(url_for('catequistas.listar'))
    
    # Si es un GET, se debería cargar el formulario de edición con los datos existentes
    catequista = modelo.obtener_por_id(id)
    return render_template('editar.html', catequista=catequista)

# Ruta para eliminar un catequista
@catequistas_bp.route('/catequistas/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        modelo.eliminar(id)
        flash('Catequista eliminado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar el catequista: {e}', 'danger')
    return redirect(url_for('catequistas.listar'))
