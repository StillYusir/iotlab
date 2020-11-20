import os
from peewee import MySQLDatabase

try:
    import ConfigParser
except:
    import configparser as ConfigParser

config = ConfigParser.ConfigParser()

def load_service_config():
    config_filename = os.path.join(os.path.dirname(__file__), 'config.ini').replace(r'\\', '/')
    #print(config_filename)
    config.read(config_filename,encoding='utf-8')
    return config


service_config = load_service_config()

DBNAME = service_config.get('database', 'database_name')
DBUSER = service_config.get('database', 'user')
DBPSWD = service_config.get('database', 'password')
DBPORT = service_config.get('database', 'port')
DBHOST = service_config.get('database', 'host')
kunshan_db = MySQLDatabase(DBNAME, user=DBUSER, password=DBPSWD, host=DBHOST, port=int(DBPORT))



