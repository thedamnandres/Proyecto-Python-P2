from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from datetime import datetime
import re
from bson import ObjectId as BsonObjectId
from ..config import Config

class PersonaModel:
    def __init__(self):
        """Inicializar conexión a MongoDB"""
        try:
            self.client = MongoClient(Config.MONGODB_URI, tlsAllowInvalidCertificates=True)
            self.db = self.client[Config.MONGODB_DATABASE]
            self.collection = self.db.personas
            
            # Probar la conexión
            self.client.admin.command('ping')
            print(f"✅ Conectado exitosamente a MongoDB: {Config.MONGODB_DATABASE}")
            
        except Exception as e:
            print(f"❌ Error conectando a MongoDB: {e}")
            raise


    def _preparar_datos(self, datos):
        """Preparar y validar datos para inserción/actualización"""
        try:
            fecha = datetime.strptime(datos.get('fecha_nacimiento', ''), '%Y-%m-%d')
        except ValueError:
            raise ValueError('La fecha de nacimiento no es válida.')
        
        if fecha > datetime.now():
            raise ValueError('La fecha de nacimiento no puede ser mayor a la fecha actual.')

        # Preparar datos de bautismo
        bautismo_data = {
            'nombre_padrino': datos.get('nombre_padrino', 'N/A'),
            'nombre_madrina': datos.get('nombre_madrina', 'N/A'),
            'nombre_abuelo_materno': datos.get('nombre_abuelo_materno', 'N/A'),
            'nombre_abuela_materno': datos.get('nombre_abuela_materno', 'N/A'),
            'nombre_abuelo_paterno': datos.get('nombre_abuelo_paterno', 'N/A'),
            'nombre_abuela_paterno': datos.get('nombre_abuela_paterno', 'N/A'),
            'lugar_bautizo': datos.get('lugar_bautizo', 'N/A')
        }
        
        # Manejar fecha de bautizo
        if datos.get('fecha_bautizo'):
            try:
                bautismo_data['fecha_bautizo'] = datetime.strptime(datos.get('fecha_bautizo'), '%Y-%m-%d')
            except ValueError:
                bautismo_data['fecha_bautizo'] = datetime.now()
        else:
            bautismo_data['fecha_bautizo'] = datetime.now()

        return {
            'cedula': datos.get('cedula', ''),
            'nombres': datos.get('nombres', ''),
            'apellidos': datos.get('apellidos', ''),
            'fecha_nacimiento': fecha,
            'lugar_nacimiento': datos.get('lugar_nacimiento', 'Quito'),
            'edad': int(datos.get('edad', 0)),
            'sexo': datos.get('sexo', ''),
            'rol': datos.get('rol', ''),
            'telefono_domicilio': datos.get('telefono_domicilio', ''),
            'direccion_domicilio': datos.get('direccion_domicilio', ''),
            'unidad_educativa': datos.get('unidad_educativa', ''),
            'alergias': datos.get('alergias', ''),
            'tipo_sangre': datos.get('tipo_sangre', ''),
            'contacto_emergencia': datos.get('contacto_emergencia', ''),
            'consideraciones': datos.get('consideraciones', ''),
            'parroquia_id': datos.get('parroquia_id', ''),
            'madre_id': BsonObjectId(datos.get('madre_id')) if datos.get('madre_id') else BsonObjectId("000000000000000000000000"),
            'padre_id': BsonObjectId(datos.get('padre_id')) if datos.get('padre_id') else BsonObjectId("000000000000000000000000"),
            'bautismo': bautismo_data
        }


    def listar(self, query={}):
        """Obtener todas las personas con filtros opcionales"""
        try:
            personas = list(self.collection.find(query))
            # Convertir ObjectId a string para JSON
            for persona in personas:
                persona['_id'] = str(persona['_id'])
                if persona.get('madre_id'):
                    persona['madre_id'] = str(persona['madre_id'])
                if persona.get('padre_id'):
                    persona['padre_id'] = str(persona['padre_id'])
            return personas
        except Exception as e:
            print(f"Error al listar personas: {e}")
            return []


    def obtener_por_id(self, persona_id):
        """Obtener una persona por ID"""
        try:
            persona = self.collection.find_one({'_id': ObjectId(persona_id)})
            if persona:
                persona['_id'] = str(persona['_id'])
                # Convertir fecha para formulario
                if isinstance(persona.get('fecha_nacimiento'), datetime):
                    persona['fecha_nacimiento'] = persona['fecha_nacimiento'].strftime('%Y-%m-%d')
                # Convertir fecha de bautizo para formulario
                if persona.get('bautismo') and isinstance(persona['bautismo'].get('fecha_bautizo'), datetime):
                    persona['bautismo']['fecha_bautizo'] = persona['bautismo']['fecha_bautizo'].strftime('%Y-%m-%d')
            return persona
        except Exception as e:
            print(f"Error al obtener persona: {e}")
            return None


    def insertar(self, datos):
        """Insertar nueva persona"""
        try:
            persona_data = self._preparar_datos(datos)
            result = self.collection.insert_one(persona_data)
            return str(result.inserted_id), 'Persona creada exitosamente'
            
        except DuplicateKeyError:
            return None, 'La cédula ya existe'
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f'Error al crear persona: {str(e)}'


    def actualizar(self, persona_id, datos):
        """Actualizar persona existente"""
        try:
            persona_existente = self.collection.find_one({'_id': ObjectId(persona_id)})
            if not persona_existente:
                return False, 'Persona no encontrada'

            datos_actualizados = self._preparar_datos(datos)
            result = self.collection.update_one(
                {'_id': ObjectId(persona_id)}, 
                {'$set': datos_actualizados}
            )
            
            return result.modified_count > 0, 'Persona actualizada exitosamente'
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f'Error al actualizar: {str(e)}'

    def eliminar(self, persona_id):
        """Eliminar persona"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(persona_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error al eliminar persona: {e}")
            return False


    def buscar_por_nombre(self, nombre):
        """Buscar personas por nombre"""
        try:
            query = {
                '$or': [
                    {'nombres': {'$regex': nombre, '$options': 'i'}},
                    {'apellidos': {'$regex': nombre, '$options': 'i'}}
                ]
            }
            return self.listar(query)
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []


    def buscar_avanzada(self, campo, valor):
        """Búsqueda avanzada por campo específico"""
        try:
            if campo == 'madre_nombre':
                return self._buscar_por_familiar('madres', valor, 'madre_id')
            elif campo == 'padre_nombre':
                return self._buscar_por_familiar('padres', valor, 'padre_id')
            else:
                query = {}
                if campo in ['nombres', 'apellidos', 'rol', 'bautismo.nombre_padrino', 
                           'bautismo.nombre_madrina', 'bautismo.lugar_bautizo']:
                    query[campo] = {'$regex': valor, '$options': 'i'}
                else:
                    query[campo] = valor
                return self.listar(query)
        except Exception as e:
            print(f"Error en búsqueda avanzada: {e}")
            return []


    def _buscar_por_familiar(self, coleccion, valor, campo_id):
        """Método auxiliar para buscar por familiar"""
        familiares = list(self.db[coleccion].find({
            '$or': [
                {'nombres': {'$regex': valor, '$options': 'i'}},
                {'apellidos': {'$regex': valor, '$options': 'i'}}
            ]
        }))
        if familiares:
            ids = [familiar['_id'] for familiar in familiares]
            return self.listar({campo_id: {'$in': ids}})
        return []

    def obtener_con_familia(self, persona_id):
        """Obtener persona con información de madre y padre"""
        try:
            persona = self.collection.find_one({'_id': ObjectId(persona_id)})
            if not persona:
                return None, None, None
                
            null_id = BsonObjectId("000000000000000000000000")
            
            # Buscar madre y padre
            madre = None
            padre = None
            
            if persona.get('madre_id') and persona['madre_id'] != null_id:
                madre = self.db.madres.find_one({'_id': persona['madre_id']})
                
            if persona.get('padre_id') and persona['padre_id'] != null_id:
                padre = self.db.padres.find_one({'_id': persona['padre_id']})
                
            # Convertir ObjectIds a string
            for item in [persona, madre, padre]:
                if item:
                    item['_id'] = str(item['_id'])
                
            return persona, madre, padre
            
        except Exception as e:
            print(f"Error al obtener familia: {e}")
            return None, None, None


    def obtener_madres(self):
        """Obtener todas las madres disponibles"""
        try:
            madres = list(self.db.madres.find())
            for madre in madres:
                madre['_id'] = str(madre['_id'])
            return madres
        except Exception as e:
            print(f"Error al obtener madres: {e}")
            return []

    def obtener_padres(self):
        """Obtener todos los padres disponibles"""
        try:
            padres = list(self.db.padres.find())
            for padre in padres:
                padre['_id'] = str(padre['_id'])
            return padres
        except Exception as e:
            print(f"Error al obtener padres: {e}")
            return []