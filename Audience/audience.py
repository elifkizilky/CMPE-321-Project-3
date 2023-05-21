from flask import Blueprint, render_template
from ..App.db_config import connection

audience_bp = Blueprint('audience', __name__)

@audience_bp.route('/')
def audience():
    movies = get_all_movies_with_predecessors()
    return render_template('audience/audience.html', movies=movies)

#buralar düzeltilecek

def get_all_movies_with_predecessors():
    cursor = connection.cursor()

    # Retrieve all movies with their predecessor lists
    query = "SELECT m.movie_id, m.movie_name, d.director_surname, p.platform_name, s.theatre_id, s.time_slot, GROUP_CONCAT(preceding_id) AS predecessors \
             FROM Movies AS m \
             INNER JOIN Directors AS d ON m.director_id = d.director_id \
             INNER JOIN Platforms AS p ON m.platform_id = p.platform_id \
             INNER JOIN MovieSessions AS s ON m.movie_id = s.movie_id \
             LEFT JOIN Precedes AS pc ON m.movie_id = pc.later_id \
             GROUP BY m.movie_id"

    cursor.execute(query)
    movies = cursor.fetchall()

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

    return movies_with_predecessors