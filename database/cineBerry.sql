DROP TABLE Users;
DROP TABLE Admins;
DROP TABLE Movie;
DROP TABLE Seats;
DROP TABLE Showtimes;
DROP TABLE Bookings;
DROP TABLE Booking_Seat;
DROP TABLE Payments;
DROP DATABASE Cinema;
CREATE DATABASE Cinema;
USE Cinema;

CREATE TABLE Users(
User_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
First_Name_u VARCHAR(60) NOT NULL,
Last_Name_u VARCHAR(60) NOT NULL,
Email_u VARCHAR(20)  NULL UNIQUE,
Phone_Number_u CHAR(10) NULL UNIQUE,
Pass_u VARCHAR(20) NOT NULL
);

CREATE TABLE Admins(
Admin_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
First_Name_a VARCHAR(60) NOT NULL,
Last_Name_a VARCHAR(60) NOT NULL,
Email_a VARCHAR(20)  NULL UNIQUE,
Phone_Number_a CHAR(10) NULL UNIQUE,
Pass_a VARCHAR(20) NOT NULL
);

CREATE TABLE Movie(
Movie_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Title VARCHAR(60) NOT NULL,
Description_ VARCHAR(500),
Duration INT NOT NULL,
Genre VARCHAR(60) NOT NULL,
age_rating ENUM('G', 'PG', 'PG-13', '14+', '17+', '18+','R'),
Poster VARCHAR(255) NULL
);

CREATE TABLE Seats(
Seat_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Hall_Number VARCHAR(60) NOT NULL,
Seat_Row  VARCHAR(60) NOT NULL,
Seat_Column VARCHAR(60) NOT NULL
);

CREATE TABLE Showtimes(
Showtime_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Movie_Id INT NOT NULL,
Hall_Number VARCHAR(60) NOT NULL,
Show_Date DATE NOT NULL,
Show_Time  TIME NOT NULL,
FOREIGN KEY (Movie_Id) REFERENCES Movie (Movie_Id)
);

CREATE TABLE Bookings(
Booking_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
User_Id INT NOT NULL,
Showtime_Id INT NOT NULL,
Booking_Date DATE NOT NULL,
Total_Price FLOAT NOT NULL,
Payment_Status ENUM ('Confirmed', 'Cancelled', 'Completed') NOT NULL,
FOREIGN KEY (User_Id) REFERENCES Users (User_Id),
FOREIGN KEY (Showtime_Id) REFERENCES Showtimes (Showtime_Id)
);

CREATE TABLE Booking_Seat(
Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Booking_Id INT NOT NULL,
Seat_Id INT NOT NULL,
FOREIGN KEY (Booking_Id) REFERENCES Bookings (Booking_Id),
FOREIGN KEY (Seat_Id) REFERENCES Seats (Seat_Id)
);

CREATE TABLE Payments (
    Payment_Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Booking_Id INT NOT NULL,
    Payment_Method ENUM('Credit Card', 'Cash', 'Apple Pay') NOT NULL,
    Amount FLOAT NOT NULL,
    Payment_Status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    Payment_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Booking_Id) REFERENCES Bookings(Booking_Id)
);

INSERT INTO Users ( First_Name_u ,Last_Name_u , Email_u ,Phone_Number_u,pass_u) VALUES
('zahra', 'almohammedsalem', 'zahra@gmail.com', '0533474737', 'zahra@44'),
('Nematallah', 'Megdad', 'Nematallah@gmail.com', '0523587634', 'Nematallah@60'),
('Hawra', 'Almadeh', 'Hawra@gmail.com', '0534756321', 'Hawra_48'),
('jude', 'aldous', 'jude@gmail.com', '0543330202', 'jude33_');

INSERT INTO Admins (First_Name_a ,Last_Name_a , Email_a ,Phone_Number_a,pass_a) VALUES
('sahar', 'alaswad', 'sahar@gmail.com', '0548838583', 'sahar33@'),
('reema', 'aldossari', 'reema@gmail.com', '0585302453', 'reema@12'),
('Ghala', 'Alsalem', 'Ghala@gmail.com', '0593828456', 'Ghala_19'),
('Nourah', 'Alharkan', 'Nourah@gmail.com', '0547583833', 'Nourah_234');

INSERT INTO Movie ( Title, Description_ ,Duration , Genre, age_rating, Poster ) VALUES
('The One Piece' , 'One Piece is an epic saga of adventure on the high seas, following the adventures of Monkey D. Luffy and his crew, the Straw Hat Pirates, as they seek the mythical treasure known as the "One Piece" to become the next King of the Pirates. ', 90 ,'adventure', '14+', 'movie1.jpg'),
('Iron lung', 'In a post-apocalyptic future after "The Quiet Rapture" event, a convict explores a blood ocean on a desolate moon using a submarine called the "Iron Lung" to search for missing stars/planets.', 127 ,'Horror','PG-13', 'movie2.jpg'),
('Fantastic Mr.Fox', 'A stop motion animated adventure comedy film. An urbane fox cannot resist returning to his farm raiding ways and then must help his community survive the farmers retaliation.',87 ,'adventure','PG', 'movie3.jpg'),
('Avengers Endgame', 'After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos actions and restore balance to the universe.',181,'Sci-Fi','PG-13', 'movie4.jpg'),
('The amazing world of GUMBALL', 'Gumballs biggest fan finds the lost episode of the show and accidentally opens a portal that connects his world to Gumballs cartoon world.', 132,'Comedy','PG', 'movie5.jpg'),
('The wild Robot', 'After a shipwreck, an intelligent robot called Roz is stranded on an uninhabited island. To survive the harsh environment, Roz bonds with the islands animals and cares for an orphaned baby goose.',102 ,'Family','PG', 'movie6.jpg'),
('Whisper of the Heart', 'The story follows Shizuku Tsukishima, a 14-year-old girl with a love for books and a knack for writing. The story begins with a curious coincidence: Shizuku notices that all her favorite library books have been previously checked out by someone named Seiji Amasawa. Intrigued, she sets out to uncover who this mystery person is, only to find herself intertwined in a journey of self-discovery, young love, and artistic ambition.',111 ,'Drama','PG', 'movie7.jpg'),
('Song of the sea', 'Ben, a young Irish boy, and his little sister Saoirse, a girl who can turn into a seal, go on an adventure to free the fairies and save the spirit world.',93 ,'Fantasy','PG', 'movie8.jpg'),
('The Kings speech', 'a historical drama that tells the inspiring story of King George VIs struggle to overcome his speech impediment with the help of an unconventional speech therapist, Lionel Logue.', 118,'History','R', 'movie9.jpg'),
('Zootopia 2', 'Brave rabbit cop Judy Hopps and her friend, the fox Nick Wilde, team up again to crack a new case, the most perilous and intricate of their careers.', 108,'adventure','PG', 'movie10.jpg');

INSERT INTO Seats (Hall_Number, Seat_Row, Seat_Column) VALUES
-- Hall 1
('Hall1','A','1'),('Hall1','A','2'),('Hall1','A','3'),('Hall1','A','4'),('Hall1','A','5'),
('Hall1','B','1'),('Hall1','B','2'),('Hall1','B','3'),('Hall1','B','4'),('Hall1','B','5'),
('Hall1','C','1'),('Hall1','C','2'),('Hall1','C','3'),('Hall1','C','4'),('Hall1','C','5'),

-- Hall 2
('Hall2','A','1'),('Hall2','A','2'),('Hall2','A','3'),('Hall2','A','4'),('Hall2','A','5'),
('Hall2','B','1'),('Hall2','B','2'),('Hall2','B','3'),('Hall2','B','4'),('Hall2','B','5'),
('Hall2','C','1'),('Hall2','C','2'),('Hall2','C','3'),('Hall2','C','4'),('Hall2','C','5'),

-- Hall 3
('Hall3','A','1'),('Hall3','A','2'),('Hall3','A','3'),('Hall3','A','4'),('Hall3','A','5'),
('Hall3','B','1'),('Hall3','B','2'),('Hall3','B','3'),('Hall3','B','4'),('Hall3','B','5'),
('Hall3','C','1'),('Hall3','C','2'),('Hall3','C','3'),('Hall3','C','4'),('Hall3','C','5'),

-- Hall 4
('Hall4','A','1'),('Hall4','A','2'),('Hall4','A','3'),('Hall4','A','4'),('Hall4','A','5'),
('Hall4','B','1'),('Hall4','B','2'),('Hall4','B','3'),('Hall4','B','4'),('Hall4','B','5'),
('Hall4','C','1'),('Hall4','C','2'),('Hall4','C','3'),('Hall4','C','4'),('Hall4','C','5'),

-- Hall 5
('Hall5','A','1'),('Hall5','A','2'),('Hall5','A','3'),('Hall5','A','4'),('Hall5','A','5'),
('Hall5','B','1'),('Hall5','B','2'),('Hall5','B','3'),('Hall5','B','4'),('Hall5','B','5'),
('Hall5','C','1'),('Hall5','C','2'),('Hall5','C','3'),('Hall5','C','4'),('Hall5','C','5'),

-- Hall 6
('Hall6','A','1'),('Hall6','A','2'),('Hall6','A','3'),('Hall6','A','4'),('Hall6','A','5'),
('Hall6','B','1'),('Hall6','B','2'),('Hall6','B','3'),('Hall6','B','4'),('Hall6','B','5'),
('Hall6','C','1'),('Hall6','C','2'),('Hall6','C','3'),('Hall6','C','4'),('Hall6','C','5'),

-- Hall 7
('Hall7','A','1'),('Hall7','A','2'),('Hall7','A','3'),('Hall7','A','4'),('Hall7','A','5'),
('Hall7','B','1'),('Hall7','B','2'),('Hall7','B','3'),('Hall7','B','4'),('Hall7','B','5'),
('Hall7','C','1'),('Hall7','C','2'),('Hall7','C','3'),('Hall7','C','4'),('Hall7','C','5'),

-- Hall 8
('Hall8','A','1'),('Hall8','A','2'),('Hall8','A','3'),('Hall8','A','4'),('Hall8','A','5'),
('Hall8','B','1'),('Hall8','B','2'),('Hall8','B','3'),('Hall8','B','4'),('Hall8','B','5'),
('Hall8','C','1'),('Hall8','C','2'),('Hall8','C','3'),('Hall8','C','4'),('Hall8','C','5'),

-- Hall 9
('Hall9','A','1'),('Hall9','A','2'),('Hall9','A','3'),('Hall9','A','4'),('Hall9','A','5'),
('Hall9','B','1'),('Hall9','B','2'),('Hall9','B','3'),('Hall9','B','4'),('Hall9','B','5'),
('Hall9','C','1'),('Hall9','C','2'),('Hall9','C','3'),('Hall9','C','4'),('Hall9','C','5'),

-- Hall 10
('Hall10','A','1'),('Hall10','A','2'),('Hall10','A','3'),('Hall10','A','4'),('Hall10','A','5'),
('Hall10','B','1'),('Hall10','B','2'),('Hall10','B','3'),('Hall10','B','4'),('Hall10','B','5'),
('Hall10','C','1'),('Hall10','C','2'),('Hall10','C','3'),('Hall10','C','4'),('Hall10','C','5');

INSERT INTO Showtimes (Movie_Id, Hall_Number, Show_Date, Show_Time) VALUES
-- The One Piece (Movie_Id = 1)
(1, 'Hall1', '2025-12-10', '12:00:00'),
(1, 'Hall2', '2025-12-10', '15:00:00'),
(1, 'Hall3', '2025-12-10', '18:00:00'),

-- Iron Lung (Movie_Id = 2)
(2, 'Hall1', '2025-12-10', '15:00:00'),
(2, 'Hall2', '2025-12-10', '18:00:00'),

-- Fantastic Mr.Fox (Movie_Id = 3)
(3, 'Hall2', '2025-12-10', '10:00:00'),
(3, 'Hall3', '2025-12-10', '18:00:00'),
(3, 'Hall3', '2025-12-10', '20:00:00'),

-- Avengers Endgame (Movie_Id = 4)
(4, 'Hall4', '2025-12-10', '12:00:00'),
(4, 'Hall4', '2025-12-10', '15:00:00'),
(4, 'Hall4', '2025-12-10', '19:00:00'),

-- The Amazing World of Gumball (Movie_Id = 5)
(5, 'Hall5', '2025-12-10', '11:00:00'),
(5, 'Hall5', '2025-12-10', '14:00:00'),
(5, 'Hall5', '2025-12-10', '17:00:00'),

-- The Wild Robot (Movie_Id = 6)
(6, 'Hall6', '2025-12-10', '12:30:00'),
(6, 'Hall6', '2025-12-10', '18:30:00'),

-- Whisper of the Heart (Movie_Id = 7)
(7, 'Hall7', '2025-12-10', '10:00:00'),

-- Song of the Sea (Movie_Id = 8)
(8, 'Hall8', '2025-12-10', '11:00:00'),
(8, 'Hall8', '2025-12-10', '14:00:00'),
(8, 'Hall8', '2025-12-10', '17:00:00'),

-- The King’s Speech (Movie_Id = 9)
(9, 'Hall9', '2025-12-10', '12:00:00'),
(9, 'Hall9', '2025-12-10', '15:00:00'),

-- Zootopia 2 (Movie_Id = 10)
(10, 'Hall10', '2025-12-10', '10:00:00'),
(10, 'Hall10', '2025-12-10', '16:00:00');

INSERT INTO Bookings (User_Id, Showtime_Id, Booking_Date, Total_Price, Payment_Status) VALUES
(2, 1, '2025-12-09', 20.00, 'Confirmed'),
(4, 3, '2025-12-09', 15.00, 'Completed');

INSERT INTO Booking_Seat (Booking_Id, Seat_Id) VALUES
(1, 1),
(1, 2),
(2,35);

INSERT INTO Payments (Booking_Id, Payment_Method, Amount, Payment_Status) VALUES
(1, 'Credit Card', 20.00, 'Completed'),
(2, 'Cash', 15.00, 'Completed');

ALTER TABLE Movie ADD COLUMN Trailer_URL VARCHAR(255) NULL;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=MCb13lbVGE0'
WHERE Movie_Id = 1;


UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=n2igjYFojUo'
WHERE Movie_Id = 3;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=TcMBFSGVi1c'
WHERE Movie_Id = 4;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=nwithX9cr8M'
WHERE Movie_Id = 5;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=67vbA5ZJdKQ'
WHERE Movie_Id = 6;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=0pVkiod6V0U'
WHERE Movie_Id = 7;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=VrhoOzW8oF8'
WHERE Movie_Id = 8;

UPDATE Movie
SET Trailer_URL = 'https://www.youtube.com/watch?v=BjkIOU5PhyQ'
WHERE Movie_Id = 10;