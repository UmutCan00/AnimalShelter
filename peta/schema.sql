CREATE TABLE user (
    User_ID CHAR(11) PRIMARY KEY,
    Password VARCHAR(40) NOT NULL,
    First_Middle_Name VARCHAR(60),
    Last_Name VARCHAR(60),
    Email VARCHAR(100),
    Phone_Number VARCHAR(20)
);


CREATE TABLE Pet (
    Pet_ID CHAR(11) PRIMARY KEY,
    Name VARCHAR(50),
    Breed VARCHAR(50),
    Date_of_Birth DATE,
    Age INT,
    Gender VARCHAR(10),
    Description TEXT,
    Adoption_Status VARCHAR(20),
    Medical_History TEXT
);




INSERT INTO student
VALUES
    ('S101', 'Ali',     '1999-07-15', 'CS', 'sophomore', 2.92),
    ('S102', 'Veli',    '2002-01-07', 'EE', 'junior',    3.96),
    ('S103', 'Ayşe',    '2004-02-12', 'IE', 'freshman',  3.30),
    ('S104', 'Mehmet',  '2003-05-23', 'CS', 'junior',    3.07);

CREATE TABLE company (
    cid CHAR(5) PRIMARY KEY,
    cname VARCHAR(20),
    quota INT,
    gpaThreshold FLOAT,
    city VARCHAR(20)
);

INSERT INTO company
VALUES
    ('C101', 'tübitak', 10, 2.50, 'Ankara'),
    ('C102', 'bist',    2,  2.80, 'Istanbul'),
    ('C103', 'aselsan', 3,  3.00, 'Ankara'),
    ('C104', 'thy',     5,  2.40, 'Istanbul'),
    ('C105', 'milsoft', 6,  2.50, 'Ankara'),
    ('C106', 'amazon',  1,  3.80, 'Palo Alto'),
    ('C107', 'tai',     4,  3.00, 'Ankara');

CREATE TABLE apply (
    sid CHAR(6),
    cid CHAR(5),
    PRIMARY KEY (sid, cid),
    FOREIGN KEY (sid) REFERENCES student(sid),
    FOREIGN KEY (cid) REFERENCES company(cid)
);

INSERT INTO apply
VALUES
    ('S101', 'C101'),
    ('S101', 'C102'),
    ('S101', 'C104'),
    ('S102', 'C106'),
    ('S103', 'C104'),
    ('S103', 'C107'),
    ('S104', 'C102'),
    ('S104', 'C107');