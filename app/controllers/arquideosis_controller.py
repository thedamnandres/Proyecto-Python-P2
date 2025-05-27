from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.arquideosis_model import ArquideosisModel

arquideosis_bp = Blueprint('arquideosis', __name__)
modelo = ArquideosisModel()

@arquideosis_bp.route('/arquideosis')
def listar():
    datos = modelo.listar()
    return render_template('arquideosis/listar.html', arquideosis=datos)

@arquideosis_bp.route('/arquideosis/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            modelo.insertar(
                request.form['nombre'],
                request.form['region']
            )
            flash('Arquidiócesis agregada exitosamente!', 'success')
        except Exception as e:
            print(f"Error al agregar: {e}")  # <- Para ver el error en la consola
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('arquideosis.listar'))
    return render_template('arquideosis/form.html')


@arquideosis_bp.route('/arquideosis/editar/<int:id>', methods=['POST'])
def editar(id):
    try:
        modelo.actualizar(
            id,
            request.form['nombre'],
            request.form['region']
        )
        flash('Arquidiócesis actualizada exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al actualizar: {e}', 'danger')
    return redirect(url_for('arquideosis.listar'))

@arquideosis_bp.route('/arquideosis/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        modelo.eliminar(id)
        flash('Arquidiócesis eliminada exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('arquideosis.listar'))
