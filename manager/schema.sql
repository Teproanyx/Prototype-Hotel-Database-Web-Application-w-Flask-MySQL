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