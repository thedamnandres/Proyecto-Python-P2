from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.catequistas_model import CatequistaModel

catequistas_bp = Blueprint('catequistas', __name__)
modelo = CatequistaModel()

@catequistas_bp.route('/catequistas')
def listar():
    datos = modelo.listar()
    return render_template('catequistas/listar.html', catequistas=datos)

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
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('catequistas.listar'))
    return render_template('catequistas/form.html')

@catequistas_bp.route('/catequistas/editar/<int:id>', methods=['POST'])
def editar(id):
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

@catequistas_bp.route('/catequistas/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        modelo.eliminar(id)
        flash('Catequista eliminado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('catequistas.listar'))
