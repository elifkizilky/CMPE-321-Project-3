from flask import Flask
import mysql.connector
import os


app = Flask(__name__)

def execute_sql_file(file_path):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=process.env.PASSWORD,
            database="",
            auth_plugin=""
        )
        cursor = connection.cursor()

        with open(file_path, 'r') as sql_file:
            statements = sql_file.read().split(';')

            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)

        connection.commit()
        return "SQL file executed successfully"
    except mysql.connector.Error as error:
        return "Error executing SQL file: {}".format(error)
    finally:
        if connection:
            connection.close()

@app.route('/')
def index():
    result = execute_sql_file("../CreateDatabase/createTables.sql")
    return result

if __name__ == '__main__':
    app.run()
