INSERT INTO Theatres (theatre_id, theatre_capacity, theatre_name, district)
VALUES (1, 100, 'ABC Theater', 'District X');

INSERT INTO Users (username, name, password, surname)
VALUES ('director1', 'John', 'passwor123', 'Doe');

INSERT INTO RatingPlatforms (platform_id, platform_name)
VALUES (1, 'Platform A');

INSERT INTO Directors (username, nationality, platform_id)
VALUES ('director1', 'Country X', 1);



INSERT INTO Movies (movie_id, movie_name, average_rating, username, duration)
VALUES (1, 'Minions', 4.5, 'director1', 2),
       (2, 'Minions: The Rise of Gru', 4.2, 'director1', 2),
       (3, 'Despicable Me', 4.8, 'director1', 2);

INSERT INTO MovieSessions (session_id, time_slot, session_date, movie_id, theatre_id)
VALUES (1, 1, '2023-05-15', 1, 1);

INSERT INTO MovieSessions (session_id, time_slot, session_date, movie_id, theatre_id)
VALUES (2, 2, '2023-05-15', 2, 1);


-- Inserting sample data into Precedes table
INSERT INTO Precedes (former_id, later_id)
VALUES (1, 2);

-- Inserting sample data into Users table
INSERT INTO Users (username, name, password, surname)
VALUES ('user1', 'John', 'pass123', 'Doe'),
       ('user2', 'Jane', 'pass456', 'Smith');
       
INSERT INTO AudienceBuy (username, session_id)
VALUES ('user1', 2);


