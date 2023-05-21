from flask import Blueprint, render_template, request
from ..App.db_config import connection
from flask import session

director_bp = Blueprint('director', __name__)

@director_bp.route('/')
def director():
    return render_template('director/director.html')

@director_bp.route('/theatres', methods=['GET'])
def list_theatres():
     # Replace with your database name
     
    date = request.args.get('date')
    time_slot = request.args.get('time_slot')
    cursor = connection.cursor()
    cursor.execute("""SELECT theatre_name, Theatres.theatre_id, district, theatre_capacity 
                    FROM Theatres 
                    LEFT JOIN MovieSessions 
                    ON Theatres.theatre_id = MovieSessions.theatre_id 
                        AND session_date = %s AND time_slot= %s
                    WHERE MovieSessions.theatre_id IS NULL """, (date, time_slot))
    theatres = cursor.fetchall()

    # Execute the query to retrieve theatres for the given time slot
    if not theatres:
        message = "No theatres available for the given date and time slot."
    else:
        message = None
    return render_template('director/theatres.html', theatres=theatres, message=message)

session_id=1

@director_bp.route('/add_movie_session', methods=['POST'])
def add_movie_session():
    # Retrieve the form data
    cursor = connection.cursor()
    global session_id
    cursor.execute("""SELECT *
                    FROM Directors""")
    print(cursor.fetchall())
    
    movie_id = request.form.get('movie_id')
    movie_name = request.form.get('movie_name')
    theatre_id = request.form.get('theatre_id')
    time_slot = request.form.get('time_slot')
    date = request.form.get('date')
    duration = request.form.get('duration')

    username = session.get('username')
    print(username)
    
    cursor.execute("""INSERT IGNORE INTO Movies
    (movie_id, movie_name, average_rating, username, duration)
    VALUES (%s, %s, %s, %s, %s)
    """, (movie_id, movie_name, 0, username, duration))
    cursor.execute("""INSERT INTO MovieSessions 
    (session_id, time_slot, session_date, movie_id, theatre_id)
    VALUES (%s, %s, %s, %s, %s)
    """, (session_id, time_slot, date, movie_id, theatre_id))
    print(cursor.fetchone())
    # Provide a success message to the director
    message = "Movie session successfully added."
    session_id+=1
    cursor.execute("""SELECT *
                    FROM Movies""")
    print(cursor.fetchall())
    
    return render_template('director/director.html', message=message)