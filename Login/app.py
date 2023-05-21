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
            return "Login successful"
        else:
            # Login failed, display an error message or redirect to login page
            # Example: return render_template('login.html', error="Invalid credentials")
            return "Invalid credentials"

    return render_template('login.html')