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
    ('Mickey', 'Chen', 200000, STR_TO_DATE('29/02/2000', '%d/%m/%Y'), '0888888888', 'mickey2902@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Poom', 'Wang', 280000, STR_TO_DATE('04/04/1999', '%d/%m/%Y'), '0844444444', 'poomwang@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Sofia', 'the First', 49000, STR_TO_DATE('09/11/2000', '%d/%m/%Y'), '0811111111', 'sofia1st@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('James', 'Bond', 200000, STR_TO_DATE('07/07/2001', '%d/%m/%Y'), '0877777777', 'jamesbond@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Kong', 'Godzilla', 160000, STR_TO_DATE('03/03/2000', '%d/%m/%Y'), '0833333333', 'konggozzy@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y'));

INSERT INTO Room(TypeID, StaffID)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 1),
    (4, 2),
    (4, 3),
    (5, 4),
    (5, 5),
    (6, 1),
    (7, 2);

INSERT INTO Caterer(TeamName, Salary, Phone, Email, HireDate)
VALUES
    ('Panda', 100000, '0911111111', 'pandacaterer@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Koala', 150000, '0922222222', 'koalacaterer@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Sloth', 50000, '0933333333', 'slothcaterer@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y')),
    ('Capybara', 200000, '0944444444', 'capybaracaterer@gmail.com', STR_TO_DATE('04/05/2000', '%d/%m/%Y'));

INSERT INTO Guest(FirstName, LastName, Phone, Email, Username, GuestPassword)
VALUES
    ('Charles', 'Lin', '0898989898', 'charleslin@gmail.com', 'CharlesL', 'sussyguest1234'),
    ('Elizabeth', 'Wen', '0989898989', 'bethywen@gmail.com', 'ElizabethW', 'yayyay2468'),
    ('Colin', 'Yang', '0878787878', 'colinyang@gmail.com', 'ColinY', 'mrcolin1379+');
