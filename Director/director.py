from flask import Blueprint, render_template, request
from ..App.db_config import connection
from flask import session

director_bp = Blueprint('director', __name__)

@director_bp.route('/')
def director():
    return render_template('director/director.html')

@director_bp.route('/theatres', methods=['GET'])
def list_theatres():
    theatres=[]
    date = request.args.get('date')
    time_slot = request.args.get('time_slot')
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT theatre_name, Theatres.theatre_id, district, theatre_capacity 
                        FROM Theatres 
                        LEFT JOIN MovieSessions 
                        ON Theatres.theatre_id = MovieSessions.theatre_id 
                            AND session_date = %s AND time_slot= %s
                        WHERE MovieSessions.theatre_id IS NULL """, (date, time_slot))
        theatres = cursor.fetchall()
    except Exception as e:
        message=str(e)

    if len(theatres)==0:
        message = "No theatres available for the given date and time slot."
    else:
        message = None
    connection.commit()
    return render_template('director/theatres.html', theatres=theatres, message=message)

@director_bp.route('/movies', methods=['GET'])
def list_movies():
    movies_with_predecessors=[]
    movies=[]
    cursor = connection.cursor()

    username = session.get('username')
    message=""
    try:
        cursor.execute("""SELECT Movies.movie_id, Movies.movie_name, theatre_id, time_slot, session_date, former_id
                        FROM MovieSessions
                        JOIN Movies ON Movies.movie_id= MovieSessions.movie_id
                        LEFT JOIN Precedes ON Precedes.later_id= Movies.movie_id
                        WHERE Movies.username = %s """, (username,))
        movies = cursor.fetchall()
        print(movies)
    except Exception as e:
        message=str(e)
        print(str(e))
        return render_template('director/movies.html', movies=movies, message=message)
    
    if(movies):
        last_element = movies[-1]
        range = last_element[0]
        print(range)
        movies_with_predecessors = []
        for movie in movies:
            movie_id = movie[0]
            movie_name = movie[1]
            theatre_id = movie[2]
            time_slot = movie[3]
            date= movie[4]
            predecessors = set()
            predecessors.add(movie[5]) #add the predecessor
            for other in movies:
                other_id = other[0]
                if movie_id == other_id:
                    predecessors.add(other[5]) #trace the movies again for each movie and if there is a predecessor, add it
            separator = ', '
            str_precedes = separator.join(str(pre) for pre in predecessors)
            # Append the movie with its attributes and predecessor list to the list
            movies_with_predecessors.append((movie_id, movie_name, theatre_id, date, time_slot, str_precedes))
            movies_with_predecessors = list(dict.fromkeys(movies_with_predecessors)) #to remove the duplicates
            print(movies_with_predecessors)
    connection.commit()
    return render_template('director/movies.html', movies=movies_with_predecessors, message=message)


@director_bp.route('/tickets', methods=['GET'])
def list_tickets():
    tickets=[]
    cursor = connection.cursor()
    username = session.get('username')
    movie_id = request.args.get('movie_id')
    print(username, movie_id)
    message=""
    try:
        cursor.execute("""SELECT a.username, u.name, u.surname
                        FROM AudienceBuy as a
                        JOIN Users as u ON a.username=u.username
                        JOIN MovieSessions as m ON m.session_id  = a.session_id 
                        JOIN Movies ON Movies.movie_id= m.movie_id 
                        where  Movies.username=%s and m.movie_id  =%s
                        """, (username, movie_id))
        tickets= cursor.fetchall()
        print( "tickets are: ",tickets)
        
    except Exception as e:
        message=str(e)
        print(str(e))
        return render_template('director/tickets.html', tickets=tickets, message=message)

    connection.commit()
    if len(tickets)==0:
        message= "You either entered a movie that is not directed by you or no one bought your ticket :("
        return render_template('director/director.html', tickets=tickets, message=message)
    return render_template('director/tickets.html', tickets=tickets, message=message)

@director_bp.route('/add_movie_session', methods=['POST'])
def add_movie_session():
    cursor = connection.cursor()
    
    #retrieve the form data
    movie_id = request.form.get('movie_id')
    movie_name = request.form.get('movie_name')
    theatre_id = request.form.get('theatre_id')
    time_slot = request.form.get('time_slot')
    date = request.form.get('date')
    duration = request.form.get('duration')
    left_capacity=0
    username = session.get('username')
    actual_movie_name=""
    actual_duration=""
    print(username)
    try:
        cursor.execute("""SELECT theatre_capacity 
                        FROM Theatres
                        WHERE theatre_id=%s""", (theatre_id,))
        result= cursor.fetchone()
        print(result)
        if result is None:
            print("Could not find the capacity for theatre")
        else:
            left_capacity= result[0]
            print("the number of tickets",left_capacity)
           
    except Exception as e: 
        message=str(e)
        return render_template('director/director.html', message=message)
   
    try:
        cursor.execute("""SELECT movie_id,movie_name, duration, username 
                        FROM Movies
                        WHERE movie_id=%s""", (movie_id,))
       
        result= cursor.fetchone()
        print("result",result)
        #if the movie does not exist
        if result is None:
            print("No rows found, this movie_id does not exists on the database")
            try:
                cursor.execute("""INSERT INTO Movies
                (movie_id, movie_name, username, duration)
                VALUES (%s, %s, %s, %s)
                """, (movie_id, movie_name, username, duration))
            except Exception as e:
                message=str(e)+"\n"
                message += "\nPlease make sure that you are logged in!"
                return render_template('director/director.html', message=message)
        else:
            #if the movie id exist, we need to check if the movie attributes match
            id= result[0]
            actual_movie_name= result[1]
            actual_duration= str(result[2])
            actual_username= result[3] 
            print("this is the name of that movie",actual_movie_name)
            print("this is the actual duration",actual_duration)
            if(actual_movie_name!= movie_name or actual_duration != duration or actual_username != username):
                print("are you the problem")
                message = "There is a movie named: " + actual_movie_name+ " with duration:" + actual_duration +" already exists on database, \nMovie ID: "+str(id) + ",\nDirector: " + actual_username 
                return render_template('director/director.html', message=message)    
    except Exception as e: 
        message=str(e)
        return render_template('director/director.html', message=message)
    try:
        cursor.execute("""INSERT INTO MovieSessions 
        ( time_slot, session_date, movie_id, theatre_id, left_capacity)
        VALUES ( %s, %s, %s, %s, %s)
        """, ( time_slot, date, movie_id, theatre_id, left_capacity))
        message = "Movie session successfully added."
    except Exception as e: 
        message=str(e)

    cursor.execute("""SELECT *
                    FROM Movies""")
    print("bre susak",cursor.fetchall())
    connection.commit()
    return render_template('director/director.html', message=message)

@director_bp.route('/add_predecessor', methods=['POST'])
def add_predecessor():
    # Retrieve the form data
    # We assumed that movie id should belong to logged in director, but predecesor might belong to some other director
    cursor = connection.cursor()
    movie_id_pred = request.form.get('movie_id_pred')
    movie_id = request.form.get('movie_id')
    username = session.get('username')
    try:
        cursor.execute("""SELECT username 
                        FROM Movies WHERE movie_id=%s""", (movie_id,))
        director= cursor.fetchone()
        if director is None:
            message="There are no movie with this id"
            return render_template('director/director.html', message=message)
        else:
            if director[0]!= username:
                message= "This is not your movie"
                return render_template('director/director.html', message=message) 
    except Exception as e:
        message=str(e)
        return render_template('director/director.html', message=message)
    
    try:
        cursor.execute("""INSERT INTO Precedes
        (former_id, later_id)
        VALUES (%s, %s)
        """, (movie_id_pred, movie_id))
        message = "Predecessor is successfully added"
    except Exception as e: 
        message=str(e)+"\n"
        message+= "Check if the movie id's exists"
    connection.commit()
    return render_template('director/director.html', message=message)

@director_bp.route('/update_name', methods=['POST'])
def update_name():
    # Retrieve the form data
    cursor = connection.cursor()
    movie_id = request.form.get('movie_id')
    movie_name = request.form.get('movie_name')
    username = session.get('username')

    try:
        cursor.execute("""SELECT username
                    FROM Movies WHERE movie_id=%s""",(movie_id,))
    except Exception as e: 
        message=str(e)
        return render_template('director/director.html', message=message)

    director= cursor.fetchone()
    if director is None:
        message="No movie exists with this movie id: "+ movie_id 
    else:
        print(director)
        if director[0]!= username:
            message= "This is not your movie"
            return render_template('director/director.html', message=message)

        try:
            cursor.execute("""UPDATE Movies
                SET movie_name = %s
                WHERE movie_id = %s AND username = %s;
            """, (movie_name, movie_id, username))
            message = "Movie name is changed"
        except Exception as e: 
            message=str(e)
   
    connection.commit()
    return render_template('director/director.html', message=message)