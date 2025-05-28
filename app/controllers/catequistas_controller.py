from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.catequistas_model import CatequistaModel

# Blueprint para las rutas de catequistas
catequistas_bp = Blueprint('catequistas', __name__)
modelo = CatequistaModel()

# Muestra la lista de catequistas.
@catequistas_bp.route('/catequistas')
def listar():
    # Obtiene y muestra todos los catequistas.
    datos = modelo.listar()
    return render_template('catequistas/listar.html', catequistas=datos)

# Muestra el formulario y procesa la creación de un nuevo catequista.
@catequistas_bp.route('/catequistas/nuevo', methods=['GET', 'POST'])
def nuevo():
    # Si es POST, inserta un nuevo catequista; si es GET, muestra el formulario.
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
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('catequistas.listar'))
    return render_template('catequistas/form.html')

# Actualiza los datos de un catequista existente (teléfono y correo).
@catequistas_bp.route('/catequistas/editar/<int:id>', methods=['POST'])
def editar(id):
    # Actualiza el teléfono y correo del catequista con el ID dado.
    try:
        modelo.actualizar(
            id,
            request.form['telefono'],
            request.form['correo']
        )
        flash('Catequista actualizado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al actualizar: {e}', 'danger')
    return redirect(url_for('catequistas.listar'))

# Elimina un catequista por su ID.
@catequistas_bp.route('/catequistas/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Elimina el catequista con el ID dado.
    try:
        modelo.eliminar(id)
        flash('Catequista eliminado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('catequistas.listar'))
