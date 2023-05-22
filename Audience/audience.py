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