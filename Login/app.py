import sys
sys.path.append("../App")
from ..App.db_config import connection

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # Perform database validation here
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DatabaseManagers WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            # Login successful, redirect to the dashboard or appropriate page
            # Example: return redirect('/dashboard')
            return "Database Manager Login successful"
        else:
            # Login failed, display an error message or redirect to login page
            # Example: return render_template('login.html', error="Invalid credentials")
            cursor.execute("SELECT * FROM Users u JOIN Directors d ON d.username = u.username WHERE d.username = %s AND u.password = %s", (username, password))
            result2 = cursor.fetchone()
            
            if result2:
                return "director login successfull"
            else:
                cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
                result3 = cursor.fetchone()
                if result3:
                    return "Audience login successfull"
                else:
                    return "Invalid credentials"
                
            return "Invalid credentials"

    return render_template('login.html')