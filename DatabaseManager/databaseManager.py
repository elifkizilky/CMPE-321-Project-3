from flask import render_template, request, redirect, Blueprint
from ..App.db_config import connection

databaseManager_bp = Blueprint('databaseManager', __name__)

@databaseManager_bp.route('/')
def databaseManager():
    return render_template('databaseManager/databaseManager.html')


@databaseManager_bp.route('/addUser', methods=['POST', 'GET'])
def addUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        user_type = request.form['user_type']  # "audience" or "director"
        cursor = connection.cursor()
        
        if user_type == "director":
            nationality = request.form['nationality']
            platform_id = request.form['platform_id']
            
            # Insert into Users table
            query_user = "INSERT INTO Users (username, password, name, surname) VALUES (%s, %s, %s, %s)"
            values_user = (username, password, name, surname)
            cursor.execute(query_user, values_user)
            
            # Insert into Directors table
            query_director = "INSERT INTO Directors (username, nationality, platform_id) VALUES (%s, %s, %s)"
            values_director = (username, nationality, platform_id)
            cursor.execute(query_director, values_director)
        else:
            # Insert into Users table
            query_user = "INSERT INTO Users (username, password, name, surname) VALUES (%s, %s, %s, %s)"
            values_user = (username, password, name, surname)
            cursor.execute(query_user, values_user)
        
        connection.commit()
        
        # Display success message or redirect to relevant page
        if user_type == "audience":
            return "User added successfully"
        else:
            return "Director added successfully"
    
    return render_template('databaseManager/addUser.html')


@databaseManager_bp.route('/deleteAudience', methods=['POST'])
def deleteAudience():
    username = request.form['username']
    cursor = connection.cursor()

    # Check if the audience exists and delete if found
    query = "SELECT * FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    audience = cursor.fetchone()
    error_message = None
    success_message = None

    if audience:
        # Delete the audience
        query_delete = "DELETE FROM Users WHERE username = %s"
        cursor.execute(query_delete, (username,))
        connection.commit()
        success_message = "Audience deleted successfully"
    else:
        error_message = "Audience not found"

    return render_template('databaseManager/databaseManager.html', success_message=success_message, error_message=error_message)


@databaseManager_bp.route('/updateDirectorPlatform', methods=['POST'])
def updateDirectorPlatform():
    username = request.form['username']
    platform_id = request.form['platform_id']
    cursor = connection.cursor()

    # Check if the director exists
    query = "SELECT * FROM Directors WHERE username = %s"
    cursor.execute(query, (username,))
    director = cursor.fetchone()
    error_message2 = None
    success_message2 = None

    if director:
        # Update the platform ID
        query_update = "UPDATE Directors SET platform_id = %s WHERE username = %s"
        cursor.execute(query_update, (platform_id, username))
        connection.commit()
        success_message2 = "Platform ID updated successfully"
    else:
        error_message2 = "Director not found"

    return render_template('databaseManager/databaseManager.html', success_message2=success_message2, error_message2=error_message2)

@databaseManager_bp.route('/viewDirectors')
def viewDirectors():
    cursor = connection.cursor()

    # Retrieve all directors
    query = "SELECT u.username, u.name, u.surname, d.nationality, d.platform_id FROM Users u JOIN Directors d ON u.username = d.username"
    cursor.execute(query)
    directors = cursor.fetchall()
    #print(directors)

    return render_template('databaseManager/viewDirectors.html', directors=directors)


@databaseManager_bp.route('/viewDirectorMovies', methods=['GET', 'POST'])
def viewDirectorMovies():
    if request.method == 'POST':
        director_username = request.form['director_username']
        cursor = connection.cursor()

        # Retrieve movies of the specified director
        query = "SELECT m.movie_id, m.movie_name, ms.theatre_id, t.district, ms.time_slot FROM Movies m JOIN Directors d ON m.username = d.username JOIN MovieSessions ms ON ms.movie_id = m.movie_id JOIN Theatres t ON ms.theatre_id = t.theatre_id WHERE d.username = %s"
        cursor.execute(query, (director_username,))
        movies = cursor.fetchall()
        
        if not movies:
            message = "This director does not have a movie yet"
            return render_template('databaseManager/viewDirectorMovies.html', message=message)
        
        return render_template('databaseManager/viewDirectorMovies.html', movies=movies)

    return render_template('databaseManager/viewDirectorMovies.html')
