--first i am creating schemans, later we ll add examples of them

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


CREATE TABLE Veterinarian (
    User_ID CHAR(11) PRIMARY KEY,
    Specialization VARCHAR(50),
    Clinic_Name VARCHAR(50),
    Clinic_ID CHAR(11),
    Status VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);


CREATE TABLE PotentialAdopter (
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Interested INT,
);


CREATE TABLE AnimalShelter (
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Animals INT,
);

CREATE TABLE Adopter(
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Adoptions INT,
);


CREATE TABLE Donor (
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Donated INT,
);





