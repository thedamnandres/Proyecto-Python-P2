from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.arquideosis_model import ArquideosisModel

# Blueprint para las rutas de arquidiosis
arquideosis_bp = Blueprint('arquideosis', __name__)
modelo = ArquideosisModel()


# Muestra la lista de arquidiosis.
@arquideosis_bp.route('/arquideosis')
def listar(): 
    # Obtiene y muestra todas las arquidiosis.
    datos = modelo.listar()
    return render_template('arquideosis/listar.html', arquideosis=datos)


# Muestra el formulario y procesa la creación de una nueva arquidiosis.
@arquideosis_bp.route('/arquideosis/nuevo', methods=['GET', 'POST'])
def nuevo():
    # Si es POST, inserta una nueva arquidiosis; si es GET, muestra el formulario.
    if request.method == 'POST':
        try:
            modelo.insertar(
                request.form['nombre'],
                request.form['region']
            )
            flash('Arquidiosis agregada exitosamente!', 'success')
        except Exception as e:
            print(f"Error al agregar: {e}")  # Error en la consola
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('arquideosis.listar'))
    return render_template('arquideosis/form.html')


# Muestra el formulario y procesa la edición de una arquidiosis existente.
@arquideosis_bp.route('/arquideosis/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Si es POST, actualiza la arquidiosis; si es GET, muestra el formulario con los datos actuales.
    if request.method == 'POST':
        try:
            modelo.actualizar(
                id,request.form['nombre'],request.form['region']
            )
            flash('Arquidiosis actualizada exitosamente!', 'success')
        except Exception as e:
            flash(f'Error al actualizar: {e}', 'danger')
        return redirect(url_for('arquideosis.listar'))
    else:
        # Obtener datos actuales para mostrar en el formulario
        datos = next((a for a in modelo.listar() if a['Arquideosis_Id'] == id), None)
        if not datos:
            flash('arquidiosis no encontrada', 'danger')
            return redirect(url_for('arquideosis.listar'))
        return render_template('arquideosis/form.html', arquideosis=datos)


# Elimina una arquidiosis por su ID.
@arquideosis_bp.route('/arquideosis/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Elimina la arquidiosis con el ID dado.
    try:
        modelo.eliminar(id)
        flash('Arquidiosis eliminada exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('arquideosis.listar'))
