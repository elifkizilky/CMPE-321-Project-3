CREATE TABLE IF NOT EXISTS DatabaseManagers(
	username CHAR(30) NOT NULL,
	password char(30) NOT NULL,
	PRIMARY KEY (username));

CREATE TABLE IF NOT EXISTS RatingPlatforms(
platform_id INTEGER NOT NULL,
platform_name CHAR(30) NOT NULL,
PRIMARY KEY(platform_id),
UNIQUE(platform_name)
);  
    
CREATE TABLE IF NOT EXISTS Users (
	username CHAR(30) NOT NULL, #As design choice we decided these should not be null
	name CHAR(30) NOT NULL, 
	password CHAR(30) NOT NULL, 
	surname CHAR(30)NOT NULL,
PRIMARY KEY (username)); 

CREATE TABLE IF NOT EXISTS Directors (
username CHAR(30) NOT NULL,
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
movie_id INTEGER NOT NULL, 
movie_name CHAR(100) NOT NULL, #movie name
average_rating FLOAT, #overall_rating
username CHAR(30) NOT NULL, #since director_name is  an attribute and not null, it is "direct" relation
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
	theatre_name CHAR(30) NOT NULL, 
	district CHAR(30) NOT NULL, 
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
former_id INTEGER NOT NULL,
later_id INTEGER NOT NULL,
PRIMARY KEY(former_id, later_id),
Foreign key (former_id) REFERENCES Movies(movie_id)
	ON DELETE CASCADE,
Foreign key (later_id) REFERENCES Movies(movie_id)
	ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MovieSessions(
	session_id INTEGER AUTO_INCREMENT NOT NULL,
	time_slot INTEGER NOT NULL,
    session_date DATE NOT NULL,
    movie_id INTEGER NOT NULL,
    theatre_id INTEGER NOT NULL, #this is "on" relation in ER diagram
	left_capacity INTEGER NOT NULL,
	PRIMARY KEY (session_id),
    UNIQUE(theatre_id, session_date, time_slot),
	FOREIGN KEY(movie_id)	#this comes from "movieof" relation in ER diagram
		REFERENCES Movies(movie_id)
        ON DELETE CASCADE,
	FOREIGN KEY(theatre_id)
		REFERENCES Theatres(theatre_id),
	CHECK( time_slot <= 4))AUTO_INCREMENT = 50001; #client should delete the movie sessions before deleting the theare 



#AudienceBuy corresponds to "buy" relation and "Audience" entity in ER diagram.
#it represents bought ticket list.
CREATE TABLE IF NOT EXISTS AudienceBuy (
	username CHAR(30) NOT NULL, 
	session_id INTEGER NOT NULL,
	PRIMARY KEY (username, session_id),
	FOREIGN KEY(username) #it comes from "Audience" entity in ER diagram.
		REFERENCES Users(username)
		ON DELETE CASCADE, #when a user is deleted, users ticket also should be deleted. 
	FOREIGN KEY(session_id) #it comes from "buy" relation in ER diagram.
		REFERENCES MovieSessions(session_id)); 
 
#AudienceSubscribe corresponds to "Audience" entity and "subscribe" relation in ER diagram.
CREATE TABLE IF NOT EXISTS AudienceSubscribe (
	username CHAR(30) NOT NULL, 
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
	username CHAR(30) NOT NULL,  #the audience who rates
	movie_id INTEGER NOT NULL,  #the movie
	rating FLOAT NOT NULL,
	FOREIGN KEY(username) #audience can rate if they bought a ticket to the movie.
		REFERENCES AudienceBuy(username),
	FOREIGN KEY(movie_id)	#platform of the movie
		REFERENCES Movies(movie_id),
	PRIMARY KEY (username,movie_id),
    CHECK (rating >= 0 AND rating <= 5) );
    




    


