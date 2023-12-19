CREATE TABLE user (
    User_ID CHAR(11) PRIMARY KEY,
    Password VARCHAR(40) NOT NULL,
    First_Middle_Name VARCHAR(60),
    Last_Name VARCHAR(60),
    Email VARCHAR(100),
    Phone_Number VARCHAR(20)
);


INSERT INTO user
VALUES
    ('U001', '123456', 'a', 'b', 'cenkerakan@email.com', "987897987"),
    ('U002', '123', 'a', 'c', 'cenkerakan@asdmail.com', "46545");

CREATE TABLE Pet (
    Pet_ID VARCHAR(11) PRIMARY KEY,
    Name VARCHAR(50),
    Breed VARCHAR(50),
    Date_of_Birth DATE,
    Age INT,
    Gender VARCHAR(10),
    Description TEXT,
    Adoption_Status VARCHAR(20),
    Medical_History TEXT
);

INSERT INTO Pet
VALUES
    ('P001', 'pet name 1', 'Tekir', '1800-01-01', 12, 'email', 'des1', 'Approved', 'grip'),
    ('P002', 'pet name 2', 'Sarman', '1800-01-02', 21, 'male', 'des2', 'Approved', 'flu');



CREATE TABLE AnimalShelter (
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Animals INT
);

INSERT INTO AnimalShelter
VALUES
    ('AS001', 0),
    ('AS002', 0);

CREATE TABLE lists (
    User_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES AnimalShelter (User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE CASCADE
);

CREATE TABLE AdoptionApplication (
    Application_ID CHAR(11) PRIMARY KEY,
    User_ID CHAR(11),
    Application_Date DATE,
    Application_Status VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE
);

CREATE TABLE Pet_Adoption(
    Application_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication(Application_ID) ON DELETE CASCADE
);