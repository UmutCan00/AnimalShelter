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
    ('U002', '123', 'a', 'c', 'cenkerakan@asdmail.com', "46545"),
    ('V001', '123456', 'umut', 'can1', 'cenkerakan@asdmail.com', '46545'),
    ('V002', '123456', 'umut', 'can2', 'cenkerakan@asdmail.com', '46545');

CREATE TABLE Pet (
    Pet_ID VARCHAR(11) PRIMARY KEY,
    Type VARCHAR(11),
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
    ('P001', 'Cat','pet name 1', 'Tekir', '1800-01-01', 12, 'email', 'des1', 'Approved', 'grip'),
    ('P002', 'Cat','pet name 2', 'Sarman', '1800-01-02', 21, 'male', 'des2', 'Approved', 'flu'),
    ('P003', 'Cat','pet name 3', 'Siyam', '1800-01-03', 123, 'female', 'des3', 'Unapproved', 'fever'),
    ('P004', 'Cat','pet name 4', 'British', '1800-01-04', 1234, 'male', 'des4', 'Unapproved', 'none'),
    ('P005', 'Cat','pet name 5', 'Scottish', '1800-01-05', 12345, 'female', 'des5', 'Unapproved', 'chickenpox');

CREATE TABLE AnimalShelter (
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Animals INT
);

INSERT INTO AnimalShelter
VALUES
    ('AS001', 2),
    ('AS002', 0);

CREATE TABLE lists (
    User_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES AnimalShelter (User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE CASCADE
);

INSERT INTO lists
VALUES
    ('AS001', 'P003'),
    ('AS001', 'P004'),
    ('AS002', 'P005');

CREATE TABLE AdoptionApplication (
    Application_ID CHAR(11) PRIMARY KEY,
    User_ID CHAR(11),
    Application_Date DATE,
    Application_Status VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE
);

INSERT INTO AdoptionApplication
VALUES
    ('AA001', 'U001', '1800-01-01', 'Approved'),
    ('AA002', 'U001', '1800-01-01', 'Approved'),
    ('AA003', 'U001', '1800-01-01', 'Unapproved');

CREATE TABLE Pet_Adoption(
    Application_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication(Application_ID) ON DELETE CASCADE
);

INSERT INTO Pet_Adoption
VALUES
    ('AA001', 'P001'),
    ('AA002', 'P002'),
    ('AA003', 'P003');

CREATE TABLE Has_Pet (
    Pet_ID VARCHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet (Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE
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

CREATE TABLE vet_appoint(
    Appointment_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE
);

CREATE TABLE met (
    Pet_ID CHAR(11),
    Date DATE,
    Time TIME,
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (Date, Time) REFERENCES Meet_And_Greet(Date, Time) ON DELETE CASCADE
);

CREATE TABLE Veterinarian (
    User_ID CHAR(11) PRIMARY KEY,
    Specialization VARCHAR(50),
    Clinic_Name VARCHAR(50),
    Clinic_ID CHAR(11),
    Status VARCHAR(20),
    FOREIGN KEY (User_ID) REFERENCES user(User_ID)
);

INSERT INTO Veterinarian (User_ID, Specialization, Clinic_Name, Clinic_ID, Status)
VALUES
    ('V001', 'General Medicine', '123', 'C001', 'Active'),
    ('V002', 'Dermatology', '123', 'C002', 'Active');

INSERT INTO Has_Pet (Pet_ID, User_ID)
VALUES
    ('P001', 'U001'), 
    ('P002', 'U002');


CREATE TABLE Adopter(
    User_ID CHAR(11) PRIMARY KEY,
    Number_of_Adoptions INT
);


CREATE TABLE Administrator (
    User_ID CHAR(11) PRIMARY KEY,
    Num_of_Adoption_Overseen INT,
    Num_of_Donation_Overseen INT,
    Num_of_Control_Overseen INT
);

CREATE TABLE ControlForm (
    Form_ID CHAR(11) PRIMARY KEY,
    Form_Name VARCHAR(50),
    Description TEXT,
    Adoption_Fee_Status VARCHAR(20)
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
);

CREATE TABLE PetCareInfo (
    Info_ID CHAR(11) PRIMARY KEY,
    Title VARCHAR(100),
    Description TEXT,
    Category VARCHAR(50)
);

CREATE TABLE donates (
    User_ID CHAR(11),
    Donation_Application_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES user(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Donation_Application_ID) REFERENCES DonationApplication(Donation_Application_ID) ON DELETE CASCADE
);

CREATE TABLE oversees_donation (
    User_ID CHAR(11),
    Donation_Application_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES Administrator(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Donation_Application_ID) REFERENCES DonationApplication(Donation_Application_ID) ON DELETE CASCADE
);

CREATE TABLE oversees_control (
    User_ID CHAR(11),
    Form_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES Administrator(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Form_ID) REFERENCES ControlForm(Form_ID) ON DELETE CASCADE
);

CREATE TABLE oversees_adoption (
    User_ID CHAR(11),
    Application_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES Administrator(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication(Application_ID) ON DELETE CASCADE
);

CREATE TABLE Adopter_Controlled (
    User_ID CHAR(11),
    Form_ID CHAR(11),
    FOREIGN KEY (User_ID) REFERENCES Adopter(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Form_ID) REFERENCES ControlForm(Form_ID) ON DELETE CASCADE
);

CREATE TABLE applies_to_adopt (
    Application_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Application_ID) REFERENCES AdoptionApplication(Application_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Adopter(User_ID) ON DELETE CASCADE
);

CREATE TABLE schedules (
    Adopter_ID CHAR(11),
    Date DATE,
    Time TIME,
    FOREIGN KEY (Adopter_ID) REFERENCES Adopter(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Date, Time) REFERENCES Meet_And_Greet(Date, Time) ON DELETE CASCADE
);

CREATE TABLE pet_appoint (
    Appointment_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE
);

CREATE TABLE pet_donation_appl (
    Donation_Application_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Donation_Application_ID) REFERENCES DonationApplication(Donation_Application_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE
);

CREATE TABLE informs (
    Info_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Info_ID) REFERENCES PetCareInfo(Info_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE
);


CREATE TABLE advises (
    Advice_ID CHAR(11),
    User_ID CHAR(11),
    FOREIGN KEY (Advice_ID) REFERENCES ExpertAdvice(Advice_ID) ON DELETE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Veterinarian(User_ID) ON DELETE CASCADE
);

CREATE TABLE advised_pet (
    Advice_ID CHAR(11),
    Pet_ID CHAR(11),
    FOREIGN KEY (Advice_ID) REFERENCES ExpertAdvice(Advice_ID) ON DELETE CASCADE,
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE
);

CREATE TABLE write_health_report (
    Vet_ID CHAR(11),
    Report_ID CHAR(11),
    FOREIGN KEY (Vet_ID) REFERENCES Veterinarian(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Report_ID) REFERENCES PetHealthReport(Report_ID) ON DELETE CASCADE
);

CREATE TABLE pet_health_report (
    Pet_ID CHAR(11),
    Report_ID CHAR(11),
    FOREIGN KEY (Pet_ID) REFERENCES Pet(Pet_ID) ON DELETE CASCADE,
    FOREIGN KEY (Report_ID) REFERENCES PetHealthReport(Report_ID) ON DELETE CASCADE
);