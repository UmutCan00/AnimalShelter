--first i am creating schemans, later we ll add examples of them

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

CREATE TABLE Administrator (
    User_ID CHAR(11) PRIMARY KEY,
    Num_of_Adoption_Overseen INT,
    Num_of_Donation_Overseen INT,
    Num_of_Control_Overseen INT,
);


CREATE TABLE AdoptionApplication (
    Application_ID CHAR(11) PRIMARY KEY,
    Application_Date DATE,
    Application_Status VARCHAR(20),
);


CREATE TABLE Meet_And_Greet (
    Date DATE,
    Time TIME,
    Pet_ID INT,
    User_ID INT,
    PRIMARY KEY (Date, Time)
);




CREATE TABLE ControlForm (
    Form_ID CHAR(11) PRIMARY KEY,
    Form_Name VARCHAR(50),
    Description TEXT,
    Adoption_Fee_Status VARCHAR(20)
);



CREATE TABLE Appointment (
    Appointment_ID CHAR(11) PRIMARY KEY,
    Date DATE,
    Time TIME,
    Purpose VARCHAR(255)
);


CREATE TABLE PetHealthReport (
Report_ID CHAR(11) PRIMARY KEY,
Diagnosis TEXT,
Medications TEXT,
Treatment_Date DATE
);
CREATE TABLE ExpertAdvice (
Advice_ID CHAR(11) PRIMARY KEY,
Title VARCHAR(100),
Description TEXT
);
CREATE TABLE DonationApplication (
Donation_Application_ID CHAR(11) PRIMARY KEY,
Application_Date DATE,
Application_Status VARCHAR(20)
);CREATE TABLE PetCareInfo (
Info_ID CHAR(11) PRIMARY KEY,
Title VARCHAR(100),
Description TEXT,
Category VARCHAR(50)
);
CREATE TABLE donates (
User_ID CHAR(11),
Donation_Application_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES Donor (User_ID) ON
DELETE CASCADE,
FOREIGN KEY (Donation_Application_ID) REFERENCES
DonationApplication (Donation_Application_ID) ON DELETE CASCADE
);
CREATE TABLE oversees_donation (
User_ID CHAR(11),
Donation_Application_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES Administrator (User_ID) ON
DELETE CASCADE,
FOREIGN KEY (Donation_Application_ID) REFERENCES
DonationApplication (Donation_Application_ID) ON DELETE CASCADE,
);
CREATE TABLE oversees_control (
User_ID CHAR(11),
Form_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES Administrator (User_ID) ON
DELETE CASCADE,
FOREIGN KEY (Form_ID) REFERENCES ControlForm (Form_ID) ON
DELETE CASCADE,
);
CREATE TABLE oversees_adoption (
User_ID CHAR(11),
Application_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES Administrator (User_ID) ON
DELETE CASCADE,
FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication
(Application_ID) ON DELETE CASCADE,
);
CREATE TABLE Adopter_Controlled (
User_ID CHAR(11),
Form_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES Adopter (User_ID) ON
DELETE CASCADE,
FOREIGN KEY (Form_ID) REFERENCES ControlForm (Form_ID) ON
DELETE CASCADE,
);CREATE TABLE schedules (
Adopter_ID CHAR(11),
Date DATE,
Time TIME,
FOREIGN KEY (Adopter_ID) REFERENCES Adopter (Adopter_ID)
ON DELETE CASCADE,
FOREIGN KEY (Date, Time) REFERENCES Meet_And_Greet (Date,
Time) ON DELETE CASCADE,
);
CREATE TABLE met (
Pet_ID CHAR(11),
Date DATE,
Time TIME,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
FOREIGN KEY (Date, Time) REFERENCES Meet_And_Greet (Date,
Time) ON DELETE CASCADE,
);CREATE TABLE Pet_Adoption(

Application_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
FOREIGN KEY (Application_ID) REFERENCES
AdoptionApplication (Application_ID) ON DELETE CASCADE,
);
CREATE TABLE applies_to_adopt (
Application_ID CHAR(11),
User_ID CHAR(11),
FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication
(Application_ID) ON DELETE CASCADE,
FOREIGN KEY (User_ID) REFERENCES Adopter (User_ID) ON
DELETE CASCADE,
);CREATE TABLE express_interest (
User_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES PotentialAdopter (User_ID)
ON DELETE CASCADE,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
);CREATE TABLE lists (
User_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (User_ID) REFERENCES AnimalShelter (User_ID)
ON DELETE CASCADE,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
);CREATE TABLE pet_appoint (
Appointment_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (Appointment_ID) REFERENCES Appointment
(Appointment_ID) ON DELETE CASCADE,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
);
CREATE TABLE pet_donation_appl (
Donation_Application_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (Donation_Application_ID) REFERENCES
DonationApplication (Donation_Application_ID) ON DELETE CASCADE,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
);CREATE TABLE informs (
Info_ID CHAR(11),
Pet_ID CHAR(11),
FOREIGN KEY (Info_ID) REFERENCES PetCareInfo (Info_ID) ON
DELETE CASCADE,
FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
CASCADE,
);

CREATE TABLE vet_appoint (
    Appointment_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Appointment_ID) REFERENCES Appointment
    (Appointment_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Veterinarian (User_ID) ON
    DELETE CASCADE,
);

CREATE TABLE advises (
    Advice_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Advice_ID) REFERENCES ExpertAdvice (Advice_ID)
    ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Veterinarian (User_ID) ON
    DELETE CASCADE,
);

CREATE TABLE advised_pet (
    Advice_ID CHAR(11),
    Pet_ID CHAR(11),
    22
    FOREIGN KEY (Advice_ID) REFERENCES ExpertAdvice (Advice_ID)
    ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
    CASCADE,
);

CREATE TABLE write_health_report (
    Vet_ID CHAR(11),
    Report_ID CHAR(11),
    FOREIGN KEY (Vet_ID) REFERENCES Veterinarian (Vet_ID) ON
    DELETE CASCADE,
    FOREIGN KEY (Report_ID) REFERENCES PetHealthReport
    (Report_ID) ON DELETE CASCADE,
);

CREATE TABLE pet_health_report (
    Pet_ID CHAR(11),
    Report_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE
    CASCADE,
    FOREIGN KEY (Report_ID) REFERENCES PetHealthReport
    (Report_ID) ON DELETE CASCADE,
);






