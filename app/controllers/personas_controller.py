from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..models.personas_model import PersonaModel

# Blueprint para las rutas de personas
personas_bp = Blueprint('personas', __name__, url_prefix='/personas')

@personas_bp.route('/')
def listar():
    """Lista todas las personas desde MongoDB con búsqueda avanzada"""
    persona_model = PersonaModel()
    search_fields = [
        'cedula', 'nombres', 'apellidos', 'parroquia_id', 'rol',
        'madre_nombre', 'padre_nombre',
        'bautismo.nombre_padrino', 'bautismo.nombre_madrina', 
        'bautismo.lugar_bautizo'
    ]
    
    # Valores por defecto
    selected_field = ''
    search_value = ''
    personas = []
    
    if request.method == 'POST':
        if 'mostrar_todo' in request.form:
            personas = persona_model.listar()
        else:
            selected_field = request.form.get('search_field', '')
            search_value = request.form.get('search_value', '').strip()
            
            if selected_field and search_value:
                personas = persona_model.buscar_avanzada(selected_field, search_value)
            else:
                personas = persona_model.listar()
    else:
        personas = persona_model.listar()
    
    return render_template('personas/listar.html', 
                         personas=personas,
                         search_fields=search_fields,
                         search_field=selected_field,
                         search_value=search_value)



@personas_bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Endpoint para búsqueda (GET y POST)"""
    persona_model = PersonaModel()
    search_fields = [
        'cedula', 'nombres', 'apellidos', 'parroquia_id', 'rol',
        'madre_nombre', 'padre_nombre',
        'bautismo.nombre_padrino', 'bautismo.nombre_madrina', 
        'bautismo.lugar_bautizo'
    ]
    
    selected_field = ''
    search_value = ''
    personas = []
    
    if request.method == 'POST':
        if 'mostrar_todo' in request.form:
            personas = persona_model.listar()
        else:
            selected_field = request.form.get('search_field', '')
            search_value = request.form.get('search_value', '').strip()
            
            if selected_field and search_value:
                personas = persona_model.buscar_avanzada(selected_field, search_value)
            else:
                personas = persona_model.listar()
    else:
        # GET request
        nombre = request.args.get('nombre', '')
        if nombre:
            personas = persona_model.buscar_por_nombre(nombre)
            search_value = nombre
        else:
            personas = persona_model.listar()
    
    return render_template('personas/listar.html', 
                         personas=personas,
                         search_fields=search_fields,
                         search_field=selected_field,
                         search_value=search_value)




@personas_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Crear nueva persona"""
    persona_model = PersonaModel()
    
    if request.method == 'POST':
        datos = request.form.to_dict()
        
        persona_id, mensaje = persona_model.insertar(datos)
        
        if persona_id:
            flash(mensaje, 'success')
            return redirect(url_for('personas.listar'))
        else:
            flash(mensaje, 'error')
            madres = persona_model.obtener_madres()
            padres = persona_model.obtener_padres()
            return render_template('personas/form.html', form_data=datos, madres=madres, padres=padres)
    
    madres = persona_model.obtener_madres()
    padres = persona_model.obtener_padres()
    return render_template('personas/form.html', madres=madres, padres=padres)




@personas_bp.route('/ver/<persona_id>')
def ver(persona_id):
    """Ver detalle de persona con información familiar"""
    try:
        persona_model = PersonaModel()
        persona, madre, padre = persona_model.obtener_con_familia(persona_id)
        
        if not persona:
            flash('Persona no encontrada', 'error')
            return redirect(url_for('personas.listar'))
        
        return render_template('personas/ver.html', 
                             persona=persona, 
                             madre=madre, 
                             padre=padre)
    except Exception as e:
        flash(f'Error al obtener la persona: {str(e)}', 'error')
        return redirect(url_for('personas.listar'))



@personas_bp.route('/editar/<persona_id>', methods=['GET', 'POST'])
def editar(persona_id):
    """Editar persona existente"""
    persona_model = PersonaModel()
    
    if request.method == 'POST':
        datos = request.form.to_dict()
        
        success, mensaje = persona_model.actualizar(persona_id, datos)
        
        if success:
            flash(mensaje, 'success')
            return redirect(url_for('personas.listar'))
        else:
            flash(mensaje, 'error')
            persona = persona_model.obtener_por_id(persona_id)
            madres = persona_model.obtener_madres()
            padres = persona_model.obtener_padres()
            return render_template('personas/form.html', persona=persona, madres=madres, padres=padres)
    
    persona = persona_model.obtener_por_id(persona_id)
    if not persona:
        flash('Persona no encontrada', 'error')
        return redirect(url_for('personas.listar'))
    
    madres = persona_model.obtener_madres()
    padres = persona_model.obtener_padres()
    return render_template('personas/form.html', persona=persona, madres=madres, padres=padres)



@personas_bp.route('/eliminar/<persona_id>', methods=['POST'])
def eliminar(persona_id):
    """Eliminar persona"""
    try:
        persona_model = PersonaModel()
        if persona_model.eliminar(persona_id):
            flash('Persona eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la persona', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('personas.listar'))



@personas_bp.route('/api/personas')
def api_listar():
    """API endpoint para obtener todas las personas en formato JSON"""
    try:
        persona_model = PersonaModel()
        personas = persona_model.listar()
        return jsonify(personas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@personas_bp.route('/api/personas/<persona_id>')
def api_obtener(persona_id):
    """API endpoint para obtener una persona específica"""
    try:
        persona_model = PersonaModel()
        persona = persona_model.obtener_por_id(persona_id)
        if persona:
            return jsonify(persona)
        else:
            return jsonify({"error": "Persona no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500