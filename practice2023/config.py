import os
from dotenv import load_dotenv

load_dotenv()

host = '127.0.0.1'
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')
