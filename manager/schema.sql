DROP TABLE IF EXISTS RoomType;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Guest;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Caterer;

CREATE TABLE RoomType(
    TypeID INT PRIMARY KEY AUTO_INCREMENT,
    RoomName varchar(50) NOT NULL,
    Details TEXT,
    PricePerNight decimal(10,2) NOT NULL,
    Capacity INT NOT NULL
);
CREATE TABLE Staff(
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    Salary decimal(10,2) NOT NULL,
    DateOfBirth date NOT NULL,
    Phone varchar(15) NOT NULL,
    Email varchar(255) NOT NULL, 
    HireDate date NOT NULL
);
CREATE TABLE Room(
    RoomNumber INT PRIMARY KEY AUTO_INCREMENT,
    TypeID INT NOT NULL,
    StaffID INT NOT NULL,
    RoomStatus varchar(20) NOT NULL,
    foreign key(TypeID) references RoomType(TypeID),
    foreign key(StaffID) references Staff(StaffID)
);
CREATE TABLE Guest(
    GuestID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    Phone varchar(15) NOT NULL,
    Email varchar(255) NOT NULL,
    Username varchar(255) NOT NULL,
    GuestPassword varchar(255) NOT NULL,
    UNIQUE(Username)
);
CREATE TABLE Booking(
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    GuestID INT NOT NULL,
    RoomNumber INT NOT NULL,
    CatererID INT,
    CheckInDate date NOT NULL,
    CheckOutDate date NOT NULL,
    TotalPrice decimal(10,2) NOT NULL,
    foreign key(GuestID) references Guest(GuestID),
    foreign key(RoomNumber) references Room(RoomNumber),
    foreign key(CatererID) references Caterer(CatererID)
);
CREATE TABLE Caterer(
    CatererID INT PRIMARY KEY AUTO_INCREMENT,
    TeamName varchar(50) NOT NULL,
    Salary decimal(10,2) NOT NULL,
    Phone varchar(15) NOT NULL,
    Email varchar(255) NOT NULL,
    HireDate date NOT NULL
);
CREATE TABLE RoomBooking(
    RoomNumber INT NOT NULL,
    BookingID INT NOT NULL,
    foreign key(RoomNumber) references Room(RoomNumber),
    foreign key(BookingID) references Booking(BookingID)
)

INSERT INTO RoomType(RoomName, Details, PricePerNight, Capacity)
VALUES
    ('Single Room', 'A room perfectly for one person.', 4999, 1),
    ('Double Room', 'A room most fit for two people.', 8999, 2),
    ('Standard Room', 'A room with one full king-size bed.', 12999, 3),
    ('Suite', 'More luxurious than a standard room.', 25999, 3),
    ('Deluxe Room', 'A room with a view.', 34999, 3),
    ('Presidential Suites', 'Second most luxurious room in the hotel.', 59999, 5),
    ('Penthouse suites', 'You take a whole floor, basically.', 199999, 8);

INSERT INTO Staff(FirstName, LastName, Salary, DateOfBirth, Phone, Email, HireDate)
VALUES
    ('Mickey', 'Chen', 200000, STR_TO_DATE('29/02/2000', '%d/%m/%Y'), 0888888888, 'mickey2902@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Poom', 'Wang', 280000, STR_TO_DATE('04/04/1999', '%d/%m/%Y'), 0844444444, 'poomwang@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Sofia', 'the First', 49000, STR_TO_DATE('09/11/2000', '%d/%m/%Y'), 0811111111, 'sofia1st@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('James', 'Bond', 200000, STR_TO_DATE('07/07/2001', '%d/%m/%Y'), 0877777777, 'jamesbond@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Kong', 'Godzilla', 160000, STR_TO_DATE('03/03/2000', '%d/%m/%Y'), 0833333333, 'konggozzy@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y'));

INSERT INTO Room(TypeID, StaffID, RoomStatus)
VALUES
    (1, 1, 'Available'),
    (1, 2, 'Available'),
    (2, 3, 'Available'),
    (2, 4, 'Available'),
    (3, 5, 'Available'),
    (3, 1, 'Available'),
    (4, 2, 'Available'),
    (4, 3, 'Available'),
    (5, 4, 'Available'),
    (5, 5, 'Available'),
    (6, 1, 'Available'),
    (7, 2, 'Available');
