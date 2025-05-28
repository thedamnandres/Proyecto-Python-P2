from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.parroquias_model import ParroquiaModel
from app.models.arquideosis_model import ArquideosisModel
from app.models.catequistas_model import CatequistaModel

# Blueprint para las rutas de parroquias
parroquia_bp = Blueprint('parroquia', __name__)
modelo = ParroquiaModel()
arquideosis_model = ArquideosisModel()
catequista_model = CatequistaModel()


# Muestra la lista de parroquias.
@parroquia_bp.route('/parroquia')
def listar():
    # Obtiene y muestra todas las parroquias, incluyendo nombres de arquidiócesis y párrocos.
    datos = modelo.listar()
    arquideosis_dict = {a['Arquideosis_Id']: a['Nombre'] for a in arquideosis_model.listar()}
    catequistas_dict = {c['Catequista_Id']: f"{c['Nombres']} {c['Apellidos']}" for c in catequista_model.listar()}
    for p in datos:
        p['Nombre_Arquideosis'] = arquideosis_dict.get(p['Arquideosis_Id'], 'Desconocida')
        p['Nombre_Parroco'] = catequistas_dict.get(p['Parroco_Id'], 'Desconocido')
    return render_template('parroquia/listar.html', parroquias=datos)


# Muestra el formulario y procesa la creación de una nueva parroquia.
@parroquia_bp.route('/parroquia/nuevo', methods=['GET', 'POST'])
def nuevo():
    # Si es POST, inserta una nueva parroquia; si es GET, muestra el formulario.
    arquideosis = arquideosis_model.listar()
    catequistas = catequista_model.listar()

    if request.method == 'POST':
        try:
            modelo.insertar(
                request.form['arquideosis_id'],
                request.form['nombre_parroquia'],
                request.form['parroco_id'],
                request.form['telefono'],
                request.form['direccion'],
                request.form.get('es_principal') == 'on'
            )
            flash('Parroquia agregada exitosamente!', 'success')
        except Exception as e:
            print(f"Error al agregar: {e}")
            flash(f'Error al agregar: {e}', 'danger')
        return redirect(url_for('parroquia.listar'))

    return render_template('parroquia/form.html', arquideosis=arquideosis, catequistas=catequistas)


# Muestra el formulario y procesa la edición de una parroquia existente.
@parroquia_bp.route('/parroquia/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Si es POST, actualiza la parroquia; si es GET, muestra el formulario con los datos actuales.
    parroquia = next((p for p in modelo.listar() if p['Parroquia_Id'] == id), None)
    if not parroquia:
        flash('Parroquia no encontrada', 'danger')
        return redirect(url_for('parroquia.listar'))

    arquideosis = arquideosis_model.listar()
    catequistas = catequista_model.listar()

    if request.method == 'POST':
        nombre_parroquia = request.form['nombre_parroquia']
        parroco_id = request.form['parroco_id']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        es_principal = request.form.get('es_principal') == 'on'
        arquideosis_id = request.form['arquideosis_id']

        try:
            modelo.actualizar(
                id,
                nombre_parroquia,
                parroco_id,
                telefono,
                direccion,
                es_principal,
                arquideosis_id
            )
            flash('Parroquia actualizada exitosamente!', 'success')
            return redirect(url_for('parroquia.listar'))
        except Exception as e:
            flash(f'Error al actualizar: {e}', 'danger')

    return render_template('parroquia/form.html', parroquia=parroquia, arquideosis=arquideosis, catequistas=catequistas)


# Elimina una parroquia por su ID.
@parroquia_bp.route('/parroquia/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Elimina la parroquia con el ID dado.
    try:
        modelo.eliminar(id)
        flash('Parroquia eliminada exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {e}', 'danger')
    return redirect(url_for('parroquia.listar'))
