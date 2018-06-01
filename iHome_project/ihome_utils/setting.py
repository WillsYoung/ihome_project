
import os

from ihome_utils.functions import get_database_uri

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

STATIC_DIR = os.path.join(BASE_DIR, 'static')


DATABASE = {

    'db': 'mysql',
    'driver': 'pymysql',
    'name': 'ihome_database',
    'user': 'root',
    'password': 'root123',
    'host': '47.106.162.144',
    'port': '3306',
}

SQLALCHEY_DATABASE_URI = get_database_uri(DATABASE)

UPLOAD_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')