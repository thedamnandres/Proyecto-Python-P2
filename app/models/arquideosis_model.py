import pyodbc
import json

class ArquideosisModel:
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
        cursor.execute("EXEC dbo.sp_listarArquideosis")
        return cursor.fetchall()

    def insertar(self, nombre, region):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_insertarArquideosis ?,?", nombre, region)
        self.conexion.commit()

    def actualizar(self, id, nombre, region):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_actualizarArquideosis ?,?,?", id, nombre, region)
        self.conexion.commit()

    def eliminar(self, id):
        cursor = self.conexion.cursor()
        cursor.execute("EXEC dbo.sp_eliminarArquideosis ?", id)
        self.conexion.commit()
