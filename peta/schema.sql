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

CREATE TABLE Meet_And_Greet (
    Date DATE,
    Time TIME,
    Pet_ID INT,
    User_ID INT,
    PRIMARY KEY (Date, Time)
);

CREATE TABLE Appointment (
    Appointment_ID CHAR(11) PRIMARY KEY,
    Date DATE,
    Time TIME,
    Purpose VARCHAR(255)
);

CREATE TABLE Has_Pet (
    Pet_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE
);

CREATE TABLE met (
    Pet_ID CHAR(11),
    Date DATE,
    Time TIME,
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (Date, Time) REFERENCES Meet_And_Greet (Date, Time) ON DELETE CASCADE
);


INSERT INTO user (User_ID, Password, First_Middle_Name, Last_Name, Email, Phone_Number)
VALUES
    ('U001', '123456', 'a', 'b', 'cenkerakan@email.com', '987897987'),
    ('U002', '123', 'a', 'c', 'cenkerakan@asdmail.com', '46545'),
    ('V001', '123456', 'umut', 'can1', 'cenkerakan@asdmail.com', '46545'),
    ('V002', '123456', 'umut', 'can2', 'cenkerakan@asdmail.com', '46545');

INSERT INTO Veterinarian (User_ID, Specialization, Clinic_Name, Clinic_ID, Status)
VALUES
    ('V001', 'General Medicine', '123', 'C001', 'Active'),
    ('V002', 'Dermatology', '123', 'C002', 'Active');

INSERT INTO Pet (Pet_ID, Name, Breed, Date_of_Birth, Age, Gender, Description, Adoption_Status, Medical_History)
VALUES
    ('P001', 'Buddy', 'Golden Retriever', '2019-05-15', 3, 'Male', 'Friendly dog', 'Available', 'Up to date on vaccinations'),
    ('P002', 'Fluffy', 'Persian', '2020-08-20', 2, 'Female', 'Fluffy cat', 'Adopted', 'Healthy and playful');

INSERT INTO Has_Pet (Pet_ID, User_ID)
VALUES
    ('P001', 'U001'), 
    ('P002', 'U002');  