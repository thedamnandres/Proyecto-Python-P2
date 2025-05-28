from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.arquideosis_model import ArquideosisModel

# Blueprint para las rutas de arquidiócesis
arquideosis_bp = Blueprint('arquideosis', __name__)
modelo = ArquideosisModel()


# Muestra la lista de arquidiócesis.
@arquideosis_bp.route('/arquideosis')
def listar(): 
    # Obtiene y muestra todas las arquidiócesis.
    datos = modelo.listar()
    return render_template('arquideosis/listar.html', arquideosis=datos)


# Muestra el formulario y procesa la creación de una nueva arquidiócesis.
@arquideosis_bp.route('/arquideosis/nuevo', methods=['GET', 'POST'])
def nuevo():
    # Si es POST, inserta una nueva arquidiócesis; si es GET, muestra el formulario.
    if request.method == 'POST':
        try:
            modelo.insertar(
                request.form['nombre'],
                request.form['region']
            )
            flash('Arquidiócesis agregada exitosamente!', 'success')
        except Exception as e:
            print(f"Error al agregar: {e}")  # Error en la consola
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('arquideosis.listar'))
    return render_template('arquideosis/form.html')


# Muestra el formulario y procesa la edición de una arquidiócesis existente.
@arquideosis_bp.route('/arquideosis/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Si es POST, actualiza la arquidiócesis; si es GET, muestra el formulario con los datos actuales.
    if request.method == 'POST':
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
    else:
        # Obtener datos actuales para mostrar en el formulario
        datos = next((a for a in modelo.listar() if a['Arquideosis_Id'] == id), None)
        if not datos:
            flash('Arquidiócesis no encontrada', 'danger')
            return redirect(url_for('arquideosis.listar'))
        return render_template('arquideosis/form.html', arquideosis=datos)


# Elimina una arquidiócesis por su ID.
@arquideosis_bp.route('/arquideosis/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Elimina la arquidiócesis con el ID dado.
    try:
        modelo.eliminar(id)
        flash('Arquidiócesis eliminada exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('arquideosis.listar'))
