import os
import json

class Config:
    # Configuración de SQL Server (existente)
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    
    # SQL Server
    SERVER = config_data['server']
    DATABASE = config_data['database']
    USERNAME = config_data['username']
    PASSWORD = config_data['password']
    DRIVER = config_data['driver']
    
    # MongoDB (nueva configuración)
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://thedamnandres:Alone2001@clusterudla01.uv1cb0v.mongodb.net/')
    MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'ProyectoIntegrador_G4')
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_secret_key_aqui')
    DEBUG = True