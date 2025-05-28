import pyodbc
import json

class ArquideosisModel:
    def __init__(self):
        # Inicializa la conexion a la base de datos usando la configuración del config.json
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
        # Obtiene todas las arquidiosis ejecutando el procedimiento almacenado correspondiente.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC sch_pro.sp_listarArquideosis")
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def insertar(self, nombre, region):
        # Inserta una nueva arquidiosis en la base de datos.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC sch_pro.sp_insertarArquideosis ?,?", nombre, region)
        self.conexion.commit()

    def actualizar(self, id, nombre, region):
        # Actualiza el nombre y la region de una arquidiosis existente.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC sch_pro.sp_actualizarArquideosis ?,?,?", id, nombre, region)
        self.conexion.commit()

    def eliminar(self, id):
        # Elimina una arquidiócesis por su ID.
        cursor = self.conexion.cursor()
        cursor.execute("EXEC sch_pro.sp_eliminarArquideosis ?", id)
        self.conexion.commit()
