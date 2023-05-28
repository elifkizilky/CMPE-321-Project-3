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
VALUES ('steven.jobs', 'Steven', 'apple123', 'Jobs'),
	('minion.lover', 'Felonius', 'bello387', 'Gru'),
        ('steve.wozniak', 'Ryan', 'pass4321', 'Andrews'),
        ('he.gongmin', 'He', 'passwordpass', 'Gongmin'),
        ('carm.galian', 'Carmelita', 'madrid9897', 'Galiano'),
        ('kron.helene', 'Helene', 'helenepass', 'Kron'),
        ('arzucan.ozgur', 'Arzucan', 'deneme123', 'Ozgur'),
        ('egemen.isguder', 'Egemen', 'deneme124', 'Isguder'),
        ('busra.oguzoglu', 'Busra', 'deneme125', 'Oguzoglu'),
        ('peter.weir', 'Peter', 'peter_weir879', 'Weir'),
        ('kyle.balda', 'Kyle', 'mynameiskyle9', 'Balda');

INSERT INTO Directors (username, nationality, platform_id)
VALUES 
    ('he.gongmin', 'Turkish', 10130),
    ('carm.galian', 'Turkish', 10131),
    ('kron.helene', 'French', 10130),
    ('peter.weir', 'Spanish', 10131),
    ('kyle.balda', 'German', 10132);





INSERT INTO Movies (movie_id, movie_name, average_rating, username, duration)
VALUES 
    (20001, 'Despicable Me', 0, 'kyle.balda', 2),
    (20002, 'Catch Me If You Can', 0, 'he.gongmin', 2),
    (20003, 'The Bone Collector', 0, 'carm.galian', 2),
    (20004, 'Eagle Eye', 0, 'kron.helene', 2),
    (20005, 'Minions: The Rise Of Gru', 0, 'kyle.balda', 1),
    (20006, 'The Minions', 0, 'kyle.balda', 1),
    (20007, 'The Truman Show', 0, 'peter.weir', 3);

INSERT INTO Theatres (theatre_id, theatre_capacity, theatre_name, district)
VALUES 
    (40001, 300, 'Sisli_1', 'Sisli'),
    (40002, 200, 'Sisli_2', 'Sisli'),
    (40003, 100, 'Besiktas1', 'Besiktas'),
    (40004, 100, 'Besiktas2', 'Besiktas'),
    (40005, 500, 'Besiktas3', 'Besiktas');


INSERT INTO MovieGenres (movie_id, genre_id)
VALUES
        (20001, 80001),
        (20001, 80002),
        (20002, 80003),
        (20002, 80004),
        (20003, 80005),
        (20004, 80003),
        (20005, 80001),
        (20005, 80002),
        (20006, 80001),
        (20006, 80002),
        (20007, 80002),
        (20007, 80006);

INSERT INTO Precedes (former_id, later_id)
VALUES 
    (20001, 20005),
    (20001, 20006),
    (20006, 20005);




INSERT INTO MovieSessions (time_slot, session_date, movie_id, theatre_id, left_capacity)
VALUES  
    (1, '2023-03-15', 20001, 40001, 300),
    (3, '2023-03-15', 20001, 40001, 300),
    (1, '2023-03-15', 20001, 40002, 200),
    (3, '2023-03-15', 20002, 40002, 200),
    (1, '2023-03-16', 20003, 40003, 100),
    (3, '2023-03-16', 20004, 40003, 100),
    (1, '2023-03-16', 20005, 40004, 100),
    (3, '2023-03-16', 20006, 40004, 100),
    (1, '2023-03-16', 20007, 40005, 500);

INSERT INTO AudienceBuy (username, session_id)
VALUES 
    ('steven.jobs', 50001),
    ('steve.wozniak', 50004),
    ('steve.wozniak', 50005),
    ('arzucan.ozgur', 50006),
    ('egemen.isguder', 50001),
    ('egemen.isguder', 50004),
    ('egemen.isguder', 50007),
    ('egemen.isguder', 50008),
    ('busra.oguzoglu', 50009);
INSERT INTO AudienceSubscribe (username, platform_id)
VALUES 
    ('steven.jobs', 10130),
    ('steven.jobs', 10131),
    ('steve.wozniak', 10131),
    ('arzucan.ozgur', 10130),
    ('egemen.isguder', 10132),
    ('busra.oguzoglu', 10131);

INSERT INTO Rates (username, movie_id, rating)
VALUES ('egemen.isguder', 20001, 5),
       ('egemen.isguder', 20005, 5),
       ('egemen.isguder', 20006, 5),
       ('arzucan.ozgur', 20004, 5),
       ('busra.oguzoglu', 20007, 5);