import pyodbc
import json

class ParroquiaModel:
    def __init__(self):
        # Inicializa la conexion a la base de datos usando la configuracion del config.json
        with open('config.json', 'r') as f:
            config = json.load(f)
        connection_string = (
            f"DRIVER={config['driver']};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"UID={config['username']};"
            f"PWD={config['password']}"
        )
        self.conexion = pyodbc.connect(connection_string)

    def listar(self):
        # Obtiene todas las parroquias ejecutando el procedimiento almacenado correspondiente.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC sch_pro.sp_listarParroquias")
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def insertar(self, arquideosis_id, nombre_parroquia, parroco_id, telefono, direccion, es_principal):
        # Inserta una nueva parroquia en la base de datos.
        cursor = self.conexion.cursor()
        cursor.execute(
            "EXEC sch_pro.sp_insertarParroquia ?, ?, ?, ?, ?, ?",
            arquideosis_id, nombre_parroquia, parroco_id, telefono, direccion, es_principal
        )
        self.conexion.commit()

    def actualizar(self, parroquia_id, nombre_parroquia, parroco_id, telefono, direccion, es_principal, arquideosis_id):
        # Actualiza los datos de una parroquia existente.
        cursor = self.conexion.cursor()
        cursor.execute(
            "EXEC sch_pro.sp_actualizarParroquia ?, ?, ?, ?, ?, ?, ?",
            parroquia_id, nombre_parroquia, parroco_id, telefono, direccion, es_principal, arquideosis_id
        )
        self.conexion.commit()

    def eliminar(self, parroquia_id):
        # Elimina una parroquia por su ID usando el procedimiento almacenado correspondiente.
        cursor = self.conexion.cursor()
        print(f"Eliminando parroquia con ID: {parroquia_id}")
        cursor.execute("EXEC sch_pro.sp_eliminarParroquia ?", parroquia_id)
        self.conexion.commit()