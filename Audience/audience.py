from flask import Blueprint, render_template
from ..App.db_config import connection

audience_bp = Blueprint('audience', __name__)

@audience_bp.route('/')
def audience():
    return render_template('audience/audience.html')

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
    print(movies)
    # Convert the predecessors list to a string
    movies_with_predecessors = []
    for movie in movies:
        movie_id = movie[0]
        movie_name = movie[1]
        director_surname = movie[2]
        platform = movie[3]
        theatre_id = movie[4]
        time_slot = movie[5]
        predecessors = movie[6] if movie[6] else ""  # Convert None to empty string

        # Append the movie with its attributes and predecessor list to the list
        movies_with_predecessors.append((movie_id, movie_name, director_surname, platform, theatre_id, time_slot, predecessors))

    return render_template('audience/listMovies.html', movies = movies)