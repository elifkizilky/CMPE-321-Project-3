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
        ('kamisama', 'Tengen', '123456789', 'Uzui'),
        ('peterJackson', 'Peter', '1234567', 'Jackson');

INSERT INTO Directors (username, nationality, platform_id)
VALUES ('kamisama', 'Japan', 10130),
        ('michanek', 'German', 10131),
        ('chrisnolan', 'English', 10131),
	('boss', 'Japan', 10131),
        ('peterJackson', 'New Zealander', 10130);


INSERT INTO Movies (movie_id, movie_name, average_rating, username, duration)
VALUES (1, 'Funny Games', 0, 'michanek', 1),
       (2, 'Love', 0, 'michanek', 2),
       (3, 'Cache', 0, 'michanek', 3),
       (4, 'Memento', 0, 'chrisnolan', 1),
       (5, 'Inception', 0, 'chrisnolan', 2),
       (6, 'The Dark Knight', 0, 'chrisnolan', 2),
       (7, 'Interstellar', 0, 'chrisnolan', 1),
       (8, 'Tenet', 0, 'chrisnolan', 2),
       (9, 'The Lord of the Rings: The Fellowship of the Ring', 0, 'peterJackson', 2),
       (10, 'The Lord of the Rings: The Two Towers', 0, 'peterJackson', 2),
       (11, 'The Lord of the Rings: The Return of the King', 0, 'peterJackson', 3);


INSERT INTO Theatres (theatre_id, theatre_capacity, theatre_name, district)
VALUES (1, 10, 'Theatre A', 'District 1'),
       (2, 15, 'Theatre B', 'District 2'),
       (3, 5, 'Theatre C', 'District 1'),
       (4, 20, 'Theatre D', 'District 3'),
       (5, 4, 'Theatre E', 'District 2');



INSERT INTO MovieSessions (time_slot, session_date, movie_id, theatre_id, left_capacity)
VALUES  (1, '2023-05-22', 1, 1, 10),
        (2, '2023-05-22', 2, 2, 15),
        (3, '2023-05-23', 1, 1, 10),
        (4, '2023-05-24', 3, 3, 5),
        (1, '2023-05-25', 4, 1, 10),
        (2, '2023-05-26', 5, 2, 15),
        (3, '2023-05-27', 6, 1, 10),
        (4, '2023-05-28', 7, 3, 5),
        (1, '2023-05-29', 8, 1, 10 ),
        (2, '2023-05-30', 9, 2, 15),
        (3, '2023-05-31', 10, 1, 10),
        (4, '2023-06-01', 11, 3, 5);
       




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


INSERT INTO Precedes (former_id, later_id)
VALUES (10,11),
        (9,11),
        (9,10);


       