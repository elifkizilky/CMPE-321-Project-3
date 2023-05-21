INSERT INTO DatabaseManagers (username, password)
VALUES ('manager1', 'managerpass1'),
       ('manager2', 'managerpass2'),
       ('manager35', 'managerpass35');

INSERT INTO Genres (genre_id, genre_name)
VALUES (80001, 'Animation'),
       (80002, 'Comedy'),
       (80003, 'Adventure'),
       (80004, 'Real Story'),
       (80005, 'Thriller'),
       (80006, 'Drama');

INSERT INTO RatingPlatforms (platform_id, platform_name)
VALUES (10130, 'IMDB'),
	(10131, 'Letterboxd'),
        (10132, 'FilmIzle'),
        (10133, 'Filmora'),
        (10134, 'BollywoodMDB');

INSERT INTO Users (username, name, password, surname)
VALUES ('demonslayer', 'tanjiro', '1234', 'kamado'),
	('kingOfForest', 'Inosuke', '123478', 'Hashibira'),
        ('blonde', 'zenitsu', '123478', 'Agatsuma'),
        ('boss', 'muzan', '1234567', 'Kibutsuji'),
        ('michanek', 'Michael', '098765', 'Haneke'),
        ('chrisnolan', 'Christopher', '568979', 'Nolan'),
        ('kamisama', 'Tengen', '123456789', 'Uzui');

INSERT INTO Directors (username, nationality, platform_id)
VALUES ('kamisama', 'Japan', 10130),
        ('michanek', 'German', 10131),
        ('chrisnolan', 'English', 10131),
	('boss', 'Japan', 10131);


INSERT INTO Movies (movie_id, movie_name, average_rating, username, duration)
VALUES (1, 'Funny Games', 4.5, 'michanek', 108),
       (2, 'Love', 4.8, 'michanek', 127),
       (3, 'Cache', 4.2, 'michanek', 117),
       (4, 'Memento', 4.5, 'chrisnolan', 113),
       (5, 'Inception', 4.8, 'chrisnolan', 148),
       (6, 'The Dark Knight', 4.2, 'chrisnolan', 152),
       (7, 'Interstellar', 4.7, 'chrisnolan', 169),
       (8, 'Tenet', 4.6, 'chrisnolan', 150);

INSERT INTO Theatres (theatre_id, theatre_capacity, theatre_name, district)
VALUES (1, 200, 'Theatre A', 'District 1'),
       (2, 150, 'Theatre B', 'District 2'),
       (3, 180, 'Theatre C', 'District 1'),
       (4, 120, 'Theatre D', 'District 3'),
       (5, 250, 'Theatre E', 'District 2');


INSERT INTO MovieSessions (session_id, time_slot, session_date, movie_id, theatre_id)
VALUES (1, 1, '2023-05-22', 1, 1),
       (2, 2, '2023-05-22', 2, 2),
       (3, 3, '2023-05-23', 1, 1),
       (4, 4, '2023-05-24', 3, 3),
       (5, 1, '2023-05-25', 4, 1),
       (6, 2, '2023-05-26', 5, 2),
       (7, 3, '2023-05-27', 6, 1);


INSERT INTO AudienceBuy (username, session_id)
VALUES  ('kingOfForest', 1),
        ('kingOfForest', 2),
        ('kingOfForest', 4),
        ('kingOfForest', 5),
        ('kingOfForest', 6),
        ('blonde', 2);

INSERT INTO AudienceSubscribe (username, platform_id)
VALUES  ('kingOfForest', 10131),
        ('blonde', 10131);



INSERT INTO Rates (username, movie_id, rating)
VALUES ('kingOfForest', 1, 3.8),
       ('kingOfForest', 2, 3.8),
       ('kingOfForest', 3, 4.8),
       ('kingOfForest', 4, 2.7),
       ('kingOfForest', 5, 3.5);