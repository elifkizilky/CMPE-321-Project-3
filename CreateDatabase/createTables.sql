CREATE TABLE IF NOT EXISTS DatabaseManagers(
	username CHAR(20) NOT NULL,
	password char(20) NOT NULL,
	PRIMARY KEY (username));
DELIMITER $$
CREATE TRIGGER CheckDatabaseManagerLimit
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
END;
DELIMITER ;
    
CREATE TABLE IF NOT EXISTS RatingPlatforms(
platform_id INTEGER,
platform_name CHAR(20) NOT NULL,
PRIMARY KEY(platform_id),
UNIQUE(platform_name)
);  
    
CREATE TABLE IF NOT EXISTS Users (
	username CHAR(20) NOT NULL, #As design choice we decided these should not be null
	name CHAR(20) NOT NULL, 
	password CHAR(10) NOT NULL, 
	surname CHAR(20)NOT NULL,
PRIMARY KEY (username)); 

CREATE TABLE IF NOT EXISTS Directors (
username CHAR(20) NOT NULL,
nationality CHAR(100) NOT NULL,
platform_id INTEGER,   #it shows agreement relation, at most one platform constraint
PRIMARY KEY (username),
UNIQUE(username, platform_id),
FOREIGN KEY(username)	
	REFERENCES Users(username)
    ON DELETE CASCADE,
 FOREIGN KEY(platform_id)	
	REFERENCES RatingPlatforms(platform_id)   
    ON DELETE SET NULL #a director does not have to be part of a platform
);

CREATE TABLE IF NOT EXISTS Movies (
movie_id INTEGER, 
movie_name CHAR(100) NOT NULL, #movie name
average_rating FLOAT, #overall_rating
username CHAR(20) NOT NULL, #since director_name is  an attribute and not null, it is "direct" relation
duration INTEGER NOT NULL,
UNIQUE(movie_id, duration), # since movie_id primary key, it is referenced in "MovieSessions" table this way
FOREIGN KEY(username)	
	REFERENCES Directors(username) 
    ON DELETE CASCADE
	ON UPDATE CASCADE, #if a platform is deleted, this tuple will be updated to username NULL, it should be updated here as well 
 #since a movie does not have to have a platform, it can be null
PRIMARY KEY (movie_id));

CREATE TABLE IF NOT EXISTS Theatres (
	theatre_id INTEGER NOT NULL, 
	theatre_capacity INTEGER NOT NULL, 
	theatre_name CHAR(20) NOT NULL, 
	district CHAR(20) NOT NULL, 
	PRIMARY KEY (theatre_id));
    
CREATE TABLE IF NOT EXISTS Genres (
	genre_id INTEGER NOT NULL, 
    genre_name CHAR(30) NOT NULL, 
	PRIMARY KEY (genre_id),
    UNIQUE(genre_name));
    
#"type" relation and "MovieGenre" entity in ER model is created as this table
CREATE TABLE IF NOT EXISTS MovieGenres (
	movie_id INTEGER NOT NULL, #comes from "type" relation in ER
	genre_id INTEGER NOT NULL, 
	FOREIGN KEY(movie_id)	
			REFERENCES Movies(movie_id)
			ON DELETE CASCADE,
	FOREIGN KEY(genre_id)	
			REFERENCES Genres(genre_id),
	PRIMARY KEY (genre_id, movie_id));



CREATE TABLE IF NOT EXISTS Precedes( #comes from "precedes" relation in ER diagram
former_id INTEGER,
later_id INTEGER,
PRIMARY KEY(former_id, later_id),
Foreign key (former_id) REFERENCES Movies(movie_id)
	ON DELETE CASCADE,
Foreign key (later_id) REFERENCES Movies(movie_id)
	ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovieSessions(
	session_id INTEGER NOT NULL,
	time_slot INTEGER NOT NULL,
    session_date DATE NOT NULL,
    movie_id INTEGER NOT NULL,
    theatre_id INTEGER, #this is "on" relation in ER diagram
	PRIMARY KEY (session_id),
    UNIQUE(theatre_id, session_date, time_slot),
	FOREIGN KEY(movie_id)	#this comes from "movieof" relation in ER diagram
		REFERENCES Movies(movie_id)
        ON DELETE CASCADE,
	FOREIGN KEY(theatre_id)
		REFERENCES Theatres(theatre_id),
	CHECK( time_slot <= 4)); #client should delete the movie sessions before deleting the theare 

DELIMITER $$
CREATE TRIGGER check_movie_session_overlap
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
END$$
DELIMITER ;


#AudienceBuy corresponds to "buy" relation and "Audience" entity in ER diagram.
#it represents bought ticket list.
CREATE TABLE IF NOT EXISTS AudienceBuy (
	username CHAR(20) NOT NULL, 
	session_id INTEGER NOT NULL,
	PRIMARY KEY (username, session_id),
	FOREIGN KEY(username) #it comes from "Audience" entity in ER diagram.
		REFERENCES Users(username)
		ON DELETE CASCADE, #when a user is deleted, user's ticket also should be deleted. 
	FOREIGN KEY(session_id) #it comes from "buy" relation in ER diagram.
		REFERENCES MovieSessions(session_id)); 
        
DELIMITER $$
CREATE TRIGGER check_predecessor_movies
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
END$$
DELIMITER ;

#AudienceSubscribe corresponds to "Audience" entity and "subscribe" relation in ER diagram.
CREATE TABLE IF NOT EXISTS AudienceSubscribe (
	username CHAR(20) NOT NULL, 
	platform_id INTEGER NOT NULL,
	PRIMARY KEY (username, platform_id),
	FOREIGN KEY(username) #it comes from Audience entity in ER diagram
		REFERENCES Users(username)
		ON DELETE CASCADE, #we dont need the subscription data without the user
	FOREIGN KEY(platform_id) #it comes from subscribe relation in ER diagram
		REFERENCES RatingPlatforms(platform_id)
		ON DELETE CASCADE); #when a platform is deleted, subscription will be deleted.

#Rates corresponds to "rates" relation in ER diagram.
CREATE TABLE IF NOT EXISTS Rates (
	username CHAR(20) NOT NULL,  #the audience who rates
	movie_id INTEGER NOT NULL,  #the movie
	rating FLOAT NOT NULL,
	FOREIGN KEY(username) #audience can rate if they bought a ticket to the movie.
		REFERENCES AudienceBuy(username),
	FOREIGN KEY(movie_id)	#platform of the movie
		REFERENCES Movies(movie_id),
	PRIMARY KEY (username,movie_id),
    CHECK (rating >= 0 AND rating <= 5) );
    
DELIMITER $$
CREATE TRIGGER CheckRatingInsert
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
END //
DELIMITER ;

