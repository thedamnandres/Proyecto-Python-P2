import json
import os
import pyodbc
from pymongo import MongoClient

class DatabaseConfig:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def get_sql_connection(self):
        """Retorna conexión a SQL Server"""
        sql_config = self.config['SQL_SERVER']
        connection_string = (
            f"DRIVER={{{sql_config['driver']}}};"
            f"SERVER={sql_config['server']};"
            f"DATABASE={sql_config['database']};"
            f"UID={sql_config['username']};"
            f"PWD={sql_config['password']};"
        )
        return pyodbc.connect(connection_string)
    
    def get_mongo_client(self):
        """Retorna cliente de MongoDB"""
        mongo_config = self.config['MONGODB']
        client = MongoClient(mongo_config['uri'])
        return client[mongo_config['database']]