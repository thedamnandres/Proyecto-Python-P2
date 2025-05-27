import pyodbc
import json

class CatequistasModel:
    def __init__(self):
        try:
            with open('config.json', 'r') as archivo_config:
                config = json.load(archivo_config)

            connection_string = (
                f"DRIVER={config['driver']};"
                f"SERVER={config['server']};"
                f"DATABASE={config['database']};"
                f"UID={config['username']};"
                f"PWD={config['password']}"
            )
            self.conexion = pyodbc.connect(connection_string)
        except Exception as e:
            print("Error al conectar a SQL Server:", e)

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_listarCatequistas")
        return cursor.fetchall()

    def insertar(self, nombres, apellidos, rol, telefono, correo, direccion):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_insertarCatequista ?,?,?,?,?,? ",
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

    def obtener_por_id(self, catequista_id):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_obtenerCatequistaPorId ?", catequista_id)
        return cursor.fetchone()
