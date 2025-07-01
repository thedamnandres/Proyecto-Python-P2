import json

class Config:
    # Leer configuración desde config.json
    with open('config.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)
    
    # SQL Server
    SQL_CONFIG = config_data['SQL_SERVER']
    SERVER = SQL_CONFIG['server']
    DATABASE = SQL_CONFIG['database']
    USERNAME = SQL_CONFIG['username']
    PASSWORD = SQL_CONFIG['password']
    DRIVER = SQL_CONFIG['driver']
    
    # MongoDB
    MONGO_CONFIG = config_data['MONGODB']
    MONGODB_URI = MONGO_CONFIG['uri']
    MONGODB_DATABASE = MONGO_CONFIG['database']
    
    # Flask
    FLASK_CONFIG = config_data['FLASK']
    SECRET_KEY = FLASK_CONFIG['secret_key']
    DEBUG = FLASK_CONFIG['debug']