import mysql.connector
from ..config import Config

connection = mysql.connector.connect(
    host=Config.HOST,
    user=Config.USER,
    password=Config.PASSWORD,
    database=Config.DATABASE
)