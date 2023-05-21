import mysql.connector
from config import Config


connection = mysql.connector.connect(
    host=Config.HOST,
    user=Config.USER,
    password=Config.PASSWORD,
    database=Config.DATABASE
)
cursor= connection.cursor()


def execute_sql_file(file_path):
    with open(file_path, 'r') as sql_file:
        statements = sql_file.read().split(';')

        for statement in statements:
            if statement.strip():
                cursor.execute(statement)

    connection.commit()
    return "SQL file executed successfully"
    
    
       
def execute_triggers():
 
    databasemanagerlimit_trigger= """CREATE TRIGGER CheckDatabaseManagerLimit
        BEFORE INSERT ON DatabaseManagers
        FOR EACH ROW
        BEGIN
            DECLARE manager_count INT;
            
            SELECT COUNT(*) INTO manager_count
            FROM DatabaseManagers;
            
            IF manager_count >= 4 THEN
                SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Maximum limit of 4 database managers reached.';
            END IF;
        END;"""

    cursor.execute(databasemanagerlimit_trigger)

    movie_session_overlap_trigger="""CREATE TRIGGER check_movie_session_overlap
        BEFORE INSERT ON MovieSessions
        FOR EACH ROW
        BEGIN
            DECLARE new_start_time INT;
            DECLARE new_end_time INT;
            SET new_start_time = NEW.time_slot;
            SET new_end_time = NEW.time_slot + (
                SELECT duration
                FROM Movies
                WHERE movie_id = NEW.movie_id
            );
            
            IF EXISTS (
                SELECT 1 FROM MovieSessions
                JOIN Movies ON MovieSessions.movie_id = Movies.movie_id
                WHERE MovieSessions.theatre_id = NEW.theatre_id
                AND MovieSessions.session_date = NEW.session_date
                AND (
                    (MovieSessions.time_slot >= new_start_time AND MovieSessions.time_slot < new_end_time)
                    OR (MovieSessions.time_slot + Movies.duration > new_start_time AND MovieSessions.time_slot + Movies.duration <= new_end_time)
                )
            ) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Overlap in movie sessions';
            END IF;
        END;"""
    cursor.execute(movie_session_overlap_trigger)

    check_predecessor_trigger="""CREATE TRIGGER check_predecessor_movies
        BEFORE INSERT ON AudienceBuy
        FOR EACH ROW
        BEGIN
            DECLARE predecessor_movies INT;
            SET predecessor_movies = (
                SELECT COUNT(*)
                FROM Precedes
                WHERE later_id = (
                    SELECT movie_id
                    FROM MovieSessions
                    WHERE session_id = NEW.session_id
                )
            );
            IF predecessor_movies > 0 THEN
                IF NOT EXISTS (
                    SELECT 1
                    FROM AudienceBuy ab
                    JOIN MovieSessions ms ON ab.session_id = ms.session_id
                    JOIN Precedes p ON p.former_id = ms.movie_id
                    WHERE ab.username = NEW.username
                    AND p.later_id = (
                        SELECT movie_id
                        FROM MovieSessions
                        WHERE session_id = NEW.session_id
                    )
                ) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Predecessor movies need to be watched first';
                END IF;
            END IF;
        END;"""

    cursor.execute(check_predecessor_trigger)
    rating_insert_trigger="""CREATE TRIGGER CheckRatingInsert
        BEFORE INSERT ON Rates
        FOR EACH ROW
        BEGIN
            DECLARE subscribed INT;
            DECLARE bought_ticket INT;
            
            -- Check if the user is subscribed to the platform
            SELECT COUNT(*) INTO subscribed
            FROM AudienceSubscribe
            WHERE username = NEW.username
            AND platform_id = (SELECT platform_id FROM Directors JOIN Movies ON Movies.username= Directors.username WHERE Movies.movie_id  = NEW.movie_id LIMIT 1);
            
            -- Check if the user has bought a ticket to the movie
            SELECT COUNT(*) INTO bought_ticket
            FROM AudienceBuy
            WHERE username = NEW.username
            AND session_id = (SELECT session_id FROM MovieSessions WHERE movie_id = NEW.movie_id LIMIT 1);
            -- If the user is not subscribed or hasn't bought a ticket, raise an error
            IF subscribed = 0 OR bought_ticket = 0
            THEN
                SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'User is not eligible to rate this movie.';
            END IF;
        END;"""


    cursor.execute(rating_insert_trigger)
    return "Triggers are executed"
 

    

def execute_sql_line(line):
    cursor.execute(line)
    for x in cursor:
        print(x)
    return "SQL file executed successfully"



if __name__ == '__main__':
    execute_sql_file("../CreateDatabase/dropTables.sql")
    execute_sql_file("../CreateDatabase/create_db_notrigger.sql")
    print(execute_triggers())
    execute_sql_file("../CreateDatabase/insert_for_demo.sql")
  


    
