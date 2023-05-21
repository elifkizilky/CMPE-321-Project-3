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
        ('kamisama', 'Tengen', '123456789', 'Uzui');

INSERT INTO Directors (username, nationality, platform_id)
VALUES ('kamisama', 'Japan', 10130),
		('boss', 'Japan', 10131);