from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..App.db_config import connection
from flask import session

audience_bp = Blueprint('audience', __name__)

@audience_bp.route('/')
def audience():
    username = session.get('username')
    cursor = connection.cursor()

    # Retrieve the existing tickets of the audience
    query_tickets = """
    select ms.movie_id, m.movie_name, a.session_id, r.rating, 
    m.average_rating as overall_rating from audiencebuy a join moviesessions ms on a.session_id  = ms.session_id 
    join movies m  on m.movie_id = ms.movie_id left join rates r on r.movie_id  = m.movie_id and a.username = r.username  where a.username = %s
    """
    cursor.execute(query_tickets, (username,))
    tickets = cursor.fetchall()

    return render_template('audience/audience.html', tickets=tickets)

#buralar düzeltilecek

@audience_bp.route('/listMovies')
def listMovies():
    cursor = connection.cursor()

    # Retrieve all movies with their predecessor lists
    query = "SELECT m.movie_id, m.movie_name, u.surname, r.platform_name, ms.theatre_id, ms.time_slot, p.former_id \
             FROM Movies m \
             JOIN Directors d ON m.username = d.username\
             join Users u on u.username = d.username \
             INNER JOIN ratingplatforms r ON r.platform_id = d.platform_id \
             JOIN MovieSessions ms ON m.movie_id = ms.movie_id \
             LEFT JOIN Precedes p ON m.movie_id = p.later_id order by movie_id ASC"
         

    cursor.execute(query)
    movies = cursor.fetchall()
    #print(movies)
    last_element = movies[-1]
    range = last_element[0]
    print(range)
    # Convert the predecessors list to a string
    movies_with_predecessors = []
    for movie in movies:
        movie_id = movie[0]
        movie_name = movie[1]
        director_surname = movie[2]
        platform = movie[3]
        theatre_id = movie[4]
        time_slot = movie[5]
        predecessors = set()
        predecessors.add(movie[6]) #add the predecessor
        
        for other in movies:
            other_id = other[0]
            if movie_id == other_id:
                predecessors.add(other[6]) #trace the movies again for each movie and if there is a predecessor, add it
                

        separator = ', '
        str_precedes = separator.join(str(pre) for pre in predecessors)

        # Append the movie with its attributes and predecessor list to the list
        movies_with_predecessors.append((movie_id, movie_name, director_surname, platform, theatre_id, time_slot, str_precedes))
        movies_with_predecessors = list(dict.fromkeys(movies_with_predecessors)) #to remove the duplicates
    return render_template('audience/listMovies.html', movies = movies_with_predecessors)



@audience_bp.route('/buyTicket', methods=['POST'])
def buyTicket():
    session_id = request.form['session_id']
    username = session.get('username')
    cursor = connection.cursor()

    try:
        # Check if the session ID is different from the sessions already bought by the audience
        query_existing_sessions = "SELECT * FROM AudienceBuy WHERE username = %s AND session_id = %s"
        cursor.execute(query_existing_sessions, (username, session_id))
        existing_sessions = cursor.fetchall()
        if existing_sessions:
            error_message = 'You have already bought a ticket for this session.'
            tickets = get_tickets(username)
            return render_template('audience/audience.html', tickets=tickets, error_message=error_message)

        # Check if the theatre capacity is full
        query_capacity = """
        select t.theatre_capacity from moviesessions ms join theatres t 
        on t.theatre_id  = ms.theatre_id where ms.session_id = %s
        """
        cursor.execute(query_capacity, (session_id,))
        theatre_capacity = cursor.fetchone()[0]

        if theatre_capacity == 0:
            error_message = 'The theatre capacity is full for this session. Please choose another session.'
            tickets = get_tickets(username)
            return render_template('audience/audience.html', tickets=tickets, error_message=error_message)

        # Buy the ticket
        query_buy_ticket = "INSERT INTO AudienceBuy (username, session_id) VALUES (%s, %s)"
        cursor.execute(query_buy_ticket, (username, session_id))
        connection.commit()

        flash('Ticket is bought.')

        # Retrieve the updated list of tickets
        tickets = get_tickets(username)
        return render_template('audience/audience.html', tickets=tickets)
    except Exception as e:
        error_message = f"An error occurred while buying the ticket: {str(e)}"
        tickets = get_tickets(username)
        return render_template('audience/audience.html', tickets=tickets, error_message=error_message)


def get_tickets(username):
    cursor = connection.cursor()

    query_tickets = """
    SELECT ms.movie_id, m.movie_name, a.session_id, r.rating, m.average_rating as overall_rating
    FROM audiencebuy a
    JOIN moviesessions ms ON a.session_id = ms.session_id
    JOIN movies m ON ms.movie_id = m.movie_id
    LEFT JOIN rates r ON r.movie_id = m.movie_id AND a.username = r.username
    WHERE a.username = %s
    """
    cursor.execute(query_tickets, (username,))
    tickets = cursor.fetchall()
    return tickets



