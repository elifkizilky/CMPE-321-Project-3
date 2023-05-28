import sys
sys.path.append("..")
import mysql.connector
import sys
sys.path.append("..")
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
    databasemanagercheck_trigger= """CREATE TRIGGER DatabaseManagerCheck
        BEFORE INSERT ON DatabaseManagers
        FOR EACH ROW
        BEGIN
            DECLARE count INT;
            SELECT COUNT(*) 
            INTO count
            FROM DatabaseManagers;
            IF count >= 4 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Maximum limit of 4 database managers reached.';
            END IF;
        END;"""
    cursor.execute(databasemanagercheck_trigger)
    #this trigger checks if a newly added movie session overlaps with an existing one, it also checks slot duration constraints
    movie_session_overlap_trigger="""CREATE TRIGGER movie_session_overlap
        BEFORE INSERT 
        ON MovieSessions FOR EACH ROW
        BEGIN
            DECLARE session_start INT;
            DECLARE session_end INT;
            SET session_start = NEW.time_slot;
            SET session_end = NEW.time_slot + (
                SELECT duration
                FROM Movies
                WHERE movie_id = NEW.movie_id
            );
            IF session_end<=5 THEN
                IF EXISTS (
                    SELECT * FROM MovieSessions ms
                    JOIN Movies m ON ms.movie_id = m.movie_id
                    WHERE ms.theatre_id = NEW.theatre_id
                    AND ms.session_date = NEW.session_date
                    AND (
                        (ms.time_slot < session_end AND ms.time_slot >= session_start)
                        OR (ms.time_slot + m.duration <= session_end AND ms.time_slot + m.duration > session_start)
                    )
                ) THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Overlap in movie sessions, please change the time slot';
                END IF;
            ELSE
                SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = 'You cant put a movie on this slot, we also need to go home and have some sleep!';
            END IF;

        END;"""
    cursor.execute(movie_session_overlap_trigger)

    predecessor_trigger="""CREATE TRIGGER predecessor_movies_watched
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
                    FROM AudienceBuy as ab
                    JOIN MovieSessions as ms ON ab.session_id = ms.session_id
                    JOIN Precedes as p ON p.former_id = ms.movie_id
                    WHERE ab.username = NEW.username
                    AND p.later_id = (
                        SELECT movie_id
                        FROM MovieSessions
                        WHERE session_id = NEW.session_id
                    )
                ) THEN
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Watch the predecessors first';
                END IF;
            END IF;
        END;"""

    cursor.execute(predecessor_trigger)

    rating_insert_trigger="""CREATE TRIGGER RatingInsert
        BEFORE INSERT ON Rates
        FOR EACH ROW
        BEGIN
            DECLARE subscribed INT;
            DECLARE bought_ticket INT;
            SELECT COUNT(*) INTO subscribed
            FROM AudienceSubscribe
            WHERE username = NEW.username
            AND platform_id = (SELECT platform_id FROM Directors JOIN Movies ON Movies.username= Directors.username WHERE Movies.movie_id  = NEW.movie_id);
            
            SELECT COUNT(*) INTO bought_ticket
            FROM AudienceBuy
            WHERE username = NEW.username
            AND session_id = (SELECT session_id FROM MovieSessions WHERE movie_id = NEW.movie_id LIMIT 1);

            IF subscribed = 0 OR bought_ticket = 0
            THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'User is not eligible to rate this movie.';
            END IF;
        END;"""
    cursor.execute(rating_insert_trigger)

    average_rating_trigger="""CREATE TRIGGER update_average_rating
        AFTER INSERT ON Rates
        FOR EACH ROW
        BEGIN
            UPDATE Movies
            SET average_rating = (
                SELECT AVG(rating)
                FROM Rates
                WHERE movie_id = NEW.movie_id
            )
            WHERE movie_id = NEW.movie_id;
        END;""" 
    cursor.execute(average_rating_trigger)
    
    #updates the left capacity for a movie session
    capacity_trigger="""CREATE TRIGGER capacity_trigger
        BEFORE INSERT ON AudienceBuy
        FOR EACH ROW
        BEGIN
            DECLARE session_capacity INT;
            SET session_capacity =(SELECT left_capacity
            FROM MovieSessions 
            WHERE session_id = NEW.session_id);
            IF session_capacity > 0 THEN
                UPDATE MovieSessions 
                SET MovieSessions.left_capacity = MovieSessions.left_capacity - 1
                WHERE session_id = NEW.session_id;
            ELSE
                SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = 'Session is full. Cannot insert into AudienceBuy.';
            END IF;        
        END;"""
    cursor.execute(capacity_trigger)
    connection.commit()
    return "Triggers are executed"
 

    

def execute_sql_line(line):
    cursor.execute(line)
    for x in cursor:
        print(x)
    return "SQL lines executed successfully"



if __name__ == '__main__':
    print("-"*40)
    #initially drop tables 
    print("Drop tables:")
    print(execute_sql_file("../CreateDatabase/dropTables.sql"))
    print("-"*40)
    #then create tables
    print("Create Tables:")
    print(execute_sql_file("../CreateDatabase/create_db_notrigger.sql"))
    print("-"*40)
    #execute triggers
    print(execute_triggers())
    print("-"*40)
    #execute the sql file for creating database managers, genre, rating platforms
    print("Insert initial rows:")
    print(execute_sql_file("../CreateDatabase/insert_for_demo.sql"))
    print("-"*40)
    #this sql file has additional inserts that can be helpful for demo
    execute_sql_file("../CreateDatabase/insert.sql")

  


    
