import pyodbc
import json

class CatequistaModel:
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
        # Obtiene todos los catequistas ejecutando el procedimiento almacenado correspondiente.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_listarCatequistas")
        columns = [column[0] for column in cursor.description]
        resultados = []
        for row in cursor.fetchall():
            resultados.append(dict(zip(columns, row)))
        return resultados

    def insertar(self, nombres, apellidos, rol, telefono, correo, direccion):
        # Inserta un nuevo catequista en la base de datos.
        cursor = self.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_insertarCatequista ?,?,?,?,?,?",
            nombres, apellidos, rol, telefono, correo, direccion
        )
        self.conexion.commit()

    def actualizar(self, catequista_id, telefono, correo):
        # Actualiza el telefono y correo de un catequista existente.
        cursor = self.conexion.cursor()
        cursor.execute(
            "EXEC dbo.sp_actualizarCatequista ?,?,?",
            catequista_id, telefono, correo
        )
        self.conexion.commit()

    def eliminar(self, catequista_id):
        # Elimina un catequista por su ID.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_eliminarCatequista ?", catequista_id)
        self.conexion.commit()
