import pyodbc
import json

class CatequistasModel:
    def __init__(self):
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
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_listarCatequistas")
        return cursor.fetchall()

    def insertar(self, nombres, apellidos, rol, telefono, correo, direccion):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_insertarCatequista ?,?,?,?,?,?",
                       nombres, apellidos, rol, telefono, correo, direccion)
        self.conexion.commit()

    def actualizar(self, catequista_id, telefono, correo):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_actualizarCatequista ?,?,?",
                       catequista_id, telefono, correo)
        self.conexion.commit()

    def eliminar(self, catequista_id):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_eliminarCatequista ?", catequista_id)
        self.conexion.commit()
