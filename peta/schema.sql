CREATE TABLE user (
    User_ID CHAR(11) PRIMARY KEY,
    Password VARCHAR(40) NOT NULL,
    First_Middle_Name VARCHAR(60),
    Last_Name VARCHAR(60),
    Email VARCHAR(100),
    Phone_Number VARCHAR(20)
);

CREATE TABLE Veterinarian (
    User_ID CHAR(11) PRIMARY KEY,
    Specialization VARCHAR(50),
    Clinic_Name VARCHAR(50),
    Clinic_ID CHAR(11),
    Status VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES user(User_ID)
);

INSERT INTO user (User_ID, Password, First_Middle_Name, Last_Name, Email, Phone_Number)
VALUES
    ('U001', '123456', 'a', 'b', 'cenkerakan@email.com', '987897987'),
    ('U002', '123', 'a', 'c', 'cenkerakan@asdmail.com', '46545');

INSERT INTO Veterinarian (User_ID, Specialization, Clinic_Name, Clinic_ID, Status)
VALUES
    ('U001', 'General Medicine', '123', 'C001', 'Active'),
    ('U002', 'Dermatology', '123', 'C002', 'Active');
