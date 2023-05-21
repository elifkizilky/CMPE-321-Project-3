from flask import Flask
import mysql.connector
import os


app = Flask(__name__)

# mydb= mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="***",
#     database="sys"
   
# )

# print(mydb)
# mycursor= mydb.cursor()
# try:
#     mycursor.execute("CREATE TABLE IF NOT EXISTS DatabaseManagers (username CHAR(20) NOT NULL, password CHAR(20) NOT NULL, PRIMARY KEY (username))")

#     print("Table created successfully.")
# except mysql.connector.Error as error:
#     print("Error creating table:", error)



def execute_sql_file(file_path):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="****",
            database="sys"
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

def execute_sql_line(line):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Hoplamaz1",
            database="sys"
        )
        cursor = connection.cursor()
        cursor.execute(line)
        for x in cursor:
            print(x)
        return "SQL file executed successfully"
    except mysql.connector.Error as error:
        return "Error executing SQL file: {}".format(error)
    finally:
        if connection:
            connection.close()

@app.route('/')
def index():
    result = execute_sql_file("../CreateDatabase/create_db_notrigger.sql")
    result= execute_sql_line("SHOW TABLES")
    return result

if __name__ == '__main__':
    
    app.run()
    
