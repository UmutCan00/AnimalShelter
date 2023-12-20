# CS353-1 Homework 4
# Cenker Akan
# 22102295
import re
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

app.secret_key = "abcdefgh"

app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "AnimalShelter"

mysql = MySQL(app)


# Home Page Function
@app.route("/", methods=["GET"])
def home():
    userid = session["userid"]
    message = ""
    if userid:
        message = "Logged in with userid= " + userid
    return render_template("auth/home.html", message=message)


# Login Page Function
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
    ):
        email = request.form["email"]
        password = request.form["password"]
        print(email)
        print(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM user WHERE Email = % s AND Password = % s",
            (
                email,
                password,
            ),
        )
        user = cursor.fetchone()
        if user:
            print("entered")
            session["loggedin"] = True
            session["userid"] = user["User_ID"]
            message = "Logged in successfully!"
            return redirect(url_for("suite"))
        else:
            message = "Please enter correct password !"
    return render_template("auth/login.html", message=message)


@app.route("/suite", methods=["GET"])
def suite():
    return render_template("auth/suite.html")


# Signup Page Function
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        name = request.form["name"]
        surname = request.form["surname"]
        phone = request.form["phone"]
        role = request.form["role"]

        # Additional fields for Veterinarian
        if role == "vet":
            specialization = request.form["specialization"]
            clinic_name = request.form["clinic_name"]
            clinic_id = request.form["clinic_id"]
            status = request.form["status"]

        # Validation checks
        if any(
            value == ""
            for value in (email, password, confirm_password, name, surname, phone, role)
        ):
            message = "Please fill out all the fields!"
            return render_template("auth/register.html", message=message)

        if password != confirm_password:
            message = "Passwords do not match!"
            return render_template("auth/register.html", message=message)

        if (
            len(password) > 40
            or len(name) > 60
            or len(surname) > 60
            or len(email) > 100
            or len(phone) > 20
        ):
            message = "Field length exceeds the limit!"
            return render_template("auth/register.html", message=message)

        try:
            # Generate a random 6-digit User_ID
            new_user_id = "U" + str("123342")
            hashed_email = sum(ord(char) for char in email) % (10**9)
            new_user_id = "U" + str(hashed_email)
            # Insert user into 'user' table with generated User_ID
            cursor.execute(
                "INSERT INTO user (User_ID, Password, First_Middle_Name, Last_Name, Email, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s)",
                (new_user_id, password, name, surname, email, phone),
            )
            mysql.connection.commit()

            # Insert user into respective table based on role
            if role == "vet":
                cursor.execute(
                    "INSERT INTO Veterinarian (User_ID, Specialization, Clinic_Name, Clinic_ID, Status) VALUES (%s, %s, %s, %s, %s)",
                    (new_user_id, specialization, clinic_name, clinic_id, status),
                )
            elif role == "adopter":
                cursor.execute(
                    "INSERT INTO Adopter (User_ID, Number_of_Adoptions) VALUES (%s, %s)",
                    (new_user_id, 0),  # You may adjust the initial value here
                )
            elif role == "shelter":
                cursor.execute(
                    "INSERT INTO AnimalShelter (User_ID, Number_of_Animals) VALUES (%s, %s)",
                    (new_user_id, 0),  # You may adjust the initial value here
                )

            mysql.connection.commit()
            message = "User successfully registered!" + new_user_id
        except Exception as e:
            message = f"Error: {str(e)}"

    else:
        message = "Please fill out all the fields!"

    return render_template("auth/register.html", message=message)


pets_data1 = [
    {
        "Pet_ID": "1",
        "Name": "Buddy",
        "Breed": "Labrador Retriever",
        "Date_of_Birth": "2020-01-15",
        "Age": 3,
        "Gender": "Male",
        "Description": "Friendly and active",
        "Adoption_Status": "Available",
        "Medical_History": "Vaccinated and dewormed",
    },
    {
        "Pet_ID": "2",
        "Name": "Buddy",
        "Breed": "Labrador Retriever",
        "Date_of_Birth": "2020-01-15",
        "Age": 3,
        "Gender": "Male",
        "Description": "Friendly and active",
        "Adoption_Status": "Available",
        "Medical_History": "Vaccinated and dewormed",
    },
    {
        "Pet_ID": "3",
        "Name": "Buddy",
        "Breed": "Labrador Retriever",
        "Date_of_Birth": "2020-01-15",
        "Age": 3,
        "Gender": "Male",
        "Description": "Friendly and active",
        "Adoption_Status": "Available",
        "Medical_History": "Vaccinated and dewormed",
    },
]


@app.route("/vet-appointment")
def user_pets():
    message = ""
    user_id = session["userid"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT p.* FROM Pet p INNER JOIN Has_Pet hp ON p.Pet_ID = hp.Pet_ID WHERE hp.User_ID = %s",
        (user_id,),
    )
    user_pets = cursor.fetchall()
    return render_template("mypetlist.html", pets=user_pets)


@app.route("/petcare")
def petcare():
    message = ""
    user_id = session["userid"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT p.* FROM Pet p INNER JOIN Has_Pet hp ON p.Pet_ID = hp.Pet_ID WHERE hp.User_ID = %s",
        (user_id,),
    )
    user_pets = cursor.fetchall()
    return render_template("petcareinfo.html", pets=user_pets)


@app.route("/petcare/<pet_type>")
def pet_care_info(pet_type):
    return render_template("typepetcare.html", pet_type=pet_type)


pet_details = {
    "Pet_ID": "1",
    "Name": "Buddy",
    "Breed": "Labrador Retriever",
    "Date_of_Birth": "2020-01-15",
    "Age": 3,
    "Gender": "Male",
    "Description": "Friendly and active",
    "Adoption_Status": "Available",
    "Medical_History": "Vaccinated and dewormed",
}


@app.route("/schedule_online_meeting/<pet_id>", methods=["GET", "POST"])
def schedule_online_meeting(pet_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM Pet WHERE Pet_ID = %s", (pet_id,))
    pet_details = cursor.fetchone()

    cursor.execute(
        "SELECT u.User_ID, CONCAT(u.First_Middle_Name, ' ', u.Last_Name) AS Full_Name FROM user u, Veterinarian v WHERE u.User_ID = v.User_ID;"
    )
    veterinarians = cursor.fetchall()

    if request.method == "POST":
        email = request.form["email"]
        fullname = request.form["fullname"]
        problems = request.form["problems"]
        appointment_time = request.form["appointment-time"]
        selected_vet = request.form["veterinarian"]
        random_number = "1234"
        # Check if email and full name match the user in the session

        user_id = session["userid"]
        cursor.execute(
            "SELECT Email, CONCAT(First_Middle_Name, ' ', Last_Name) AS Full_Name FROM user WHERE User_ID = %s",
            (user_id,),
        )
        user_info = cursor.fetchone()

        if (
            str(user_info["Email"]).lower().strip() == str(email).lower().strip()
            and str(user_info["Full_Name"]).lower().strip()
            == str(fullname).lower().strip()
        ):
            cursor.execute(
                "INSERT INTO Appointment (Appointment_ID, Date, Time, Purpose) VALUES (%s, %s, %s, %s)",
                (
                    random_number,
                    appointment_time.split("T")[0],
                    appointment_time.split("T")[1],
                    problems,
                ),
            )
            mysql.connection.commit()
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (random_number, user_id),
            )

            # Fetch the newly inserted Appointment_ID
            cursor.execute(
                "SELECT Appointment_ID FROM Appointment ORDER BY Appointment_ID DESC LIMIT 1"
            )
            appointment_id = cursor.fetchone()["Appointment_ID"]

            # Insert data into vet_appoint table
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (appointment_id, user_id),
            )
            mysql.connection.commit()

            form_success = True
            return render_template(
                "online_meeting.html",
                pet=pet_details,
                veterinarians=veterinarians,
                form_success=form_success,
            )

        return render_template(
            "online_meeting.html",
            pet=pet_details,
            veterinarians=veterinarians,
            message="invalid fields"
            + email
            + fullname
            + user_info["Email"]
            + user_info["Full_Name"],
        )

    user_id = session["userid"]
    cursor.execute(
        "SELECT Email, CONCAT(First_Middle_Name, ' ', Last_Name) AS Full_Name FROM user WHERE User_ID = %s",
        (user_id,),
    )
    user_info = cursor.fetchone()
    return render_template(
        "online_meeting.html",
        pet=pet_details,
        veterinarians=veterinarians,
    )


@app.route("/schedule_vet_appointment/<pet_id>", methods=["GET", "POST"])
def schedule_vet_appointment(pet_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM Pet WHERE Pet_ID = %s", (pet_id,))
    pet_details = cursor.fetchone()
    veterinarians = {}
    # Fetch all distinct clinic names
    cursor.execute("SELECT DISTINCT Clinic_Name FROM Veterinarian")
    clinics = cursor.fetchall()

    if request.method == "POST":
        selected_clinic = request.form.get("clinic")

        # Fetch veterinarians based on the selected clinic
        cursor.execute(
            "SELECT u.User_ID, CONCAT(u.First_Middle_Name, ' ', u.Last_Name) AS Full_Name FROM user u "
            "JOIN Veterinarian v ON u.User_ID = v.User_ID WHERE v.Clinic_Name = %s",
            (selected_clinic,),
        )
        veterinarians = cursor.fetchall()
        email = request.form["email"]
        fullname = request.form["fullname"]
        problems = request.form["problems"]
        appointment_time = request.form["appointment-time"]
        selected_vet = request.form["veterinarian"]
        random_number = "1234"
        # Check if email and full name match the user in the session

        user_id = session["userid"]
        cursor.execute(
            "SELECT Email, CONCAT(First_Middle_Name, ' ', Last_Name) AS Full_Name FROM user WHERE User_ID = %s",
            (user_id,),
        )
        user_info = cursor.fetchone()

        if (
            str(user_info["Email"]).lower().strip() == str(email).lower().strip()
            and str(user_info["Full_Name"]).lower().strip()
            == str(fullname).lower().strip()
        ):
            cursor.execute(
                "INSERT INTO Appointment (Appointment_ID, Date, Time, Purpose) VALUES (%s, %s, %s, %s)",
                (
                    random_number,
                    appointment_time.split("T")[0],
                    appointment_time.split("T")[1],
                    problems,
                ),
            )
            mysql.connection.commit()
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (random_number, user_id),
            )

            # Fetch the newly inserted Appointment_ID
            cursor.execute(
                "SELECT Appointment_ID FROM Appointment ORDER BY Appointment_ID DESC LIMIT 1"
            )
            appointment_id = cursor.fetchone()["Appointment_ID"]

            # Insert data into vet_appoint table
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (appointment_id, user_id),
            )
            mysql.connection.commit()
            return render_template(
                "vet_meeting.html",
                pet=pet_details,
                clinics=clinics,
                veterinarians=veterinarians,
            )
        # Handle the rest of the form submission for requesting a meeting
        # ...

        return render_template(
            "vet_meeting.html",
            pet=pet_details,
            clinics=clinics,
            veterinarians=veterinarians,
        )

    return render_template(
        "vet_meeting.html",
        pet=pet_details,
        clinics=clinics,
        veterinarians=veterinarians,
    )

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM Pet WHERE Pet_ID = %s", (pet_id,))
    pet_details = cursor.fetchone()

    cursor.execute(
        "SELECT u.User_ID, CONCAT(u.First_Middle_Name, ' ', u.Last_Name) AS Full_Name FROM user u, Veterinarian v WHERE u.User_ID = v.User_ID;"
    )
    veterinarians = cursor.fetchall()

    if request.method == "POST":
        email = request.form["email"]
        fullname = request.form["fullname"]
        problems = request.form["problems"]
        appointment_time = request.form["appointment-time"]
        selected_vet = request.form["veterinarian"]
        random_number = "1234"
        # Check if email and full name match the user in the session

        user_id = session["userid"]
        cursor.execute(
            "SELECT Email, CONCAT(First_Middle_Name, ' ', Last_Name) AS Full_Name FROM user WHERE User_ID = %s",
            (user_id,),
        )
        user_info = cursor.fetchone()

        if (
            str(user_info["Email"]).lower().strip() == str(email).lower().strip()
            and str(user_info["Full_Name"]).lower().strip()
            == str(fullname).lower().strip()
        ):
            cursor.execute(
                "INSERT INTO Appointment (Appointment_ID, Date, Time, Purpose) VALUES (%s, %s, %s, %s)",
                (
                    random_number,
                    appointment_time.split("T")[0],
                    appointment_time.split("T")[1],
                    problems,
                ),
            )
            mysql.connection.commit()
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (random_number, user_id),
            )

            # Fetch the newly inserted Appointment_ID
            cursor.execute(
                "SELECT Appointment_ID FROM Appointment ORDER BY Appointment_ID DESC LIMIT 1"
            )
            appointment_id = cursor.fetchone()["Appointment_ID"]

            # Insert data into vet_appoint table
            cursor.execute(
                "INSERT INTO vet_appoint (Appointment_ID, User_ID) VALUES (%s, %s)",
                (appointment_id, user_id),
            )
            mysql.connection.commit()

            form_success = True
            return render_template(
                "online_meeting.html",
                pet=pet_details,
                veterinarians=veterinarians,
                form_success=form_success,
                message=user_info,
            )

        return render_template(
            "online_meeting.html",
            pet=pet_details,
            veterinarians=veterinarians,
            message="invalid fields"
            + email
            + fullname
            + user_info["Email"]
            + user_info["Full_Name"],
        )

    user_id = session["userid"]
    cursor.execute(
        "SELECT Email, CONCAT(First_Middle_Name, ' ', Last_Name) AS Full_Name FROM user WHERE User_ID = %s",
        (user_id,),
    )
    user_info = cursor.fetchone()
    return render_template(
        "online_meeting.html",
        pet=pet_details,
        veterinarians=veterinarians,
        message=user_info,
    )


pets_data = {
    1: {
        "Pet_ID": 1,
        "Name": "Fluffy",
        "Breed": "Golden Retriever",
    }
}

applications_data = {
    1: {
        "Application_ID": 1,
        "Pet_ID": 1,
        "Donation_Fee": 50,
        "Admin_Approved": True,
        "Shelter_Approved": True,
    }
}


@app.route("/adoption-application/<id>", methods=["GET", "POST"])
def adoption_application(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "GET":
        # Fetch pet data related to the provided ID and user from the session
        user_id = session["userid"]
        if not user_id:
            return "User not logged in", 403

        cursor.execute(
            "SELECT p.*, aa.* "
            "FROM Pet p "
            "JOIN Pet_Adoption pa ON p.Pet_ID = pa.Pet_ID "
            "JOIN AdoptionApplication aa ON aa.Application_ID = pa.Application_ID "
            "WHERE aa.Application_ID = %s AND aa.User_ID = %s",
            (id, user_id),
        )
        pet_application = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM Meet_And_Greet WHERE Pet_ID = %s AND User_ID = %s",
            (id, user_id),
        )
        meet_and_greet = cursor.fetchall()

        if not pet_application:
            return "Pet or application not found", 404

        return render_template(
            "adoption_application.html",
            pet=pet_application,
            application=pet_application,
            meet_and_greet=meet_and_greet,
        )

    elif request.method == "POST":
        if "schedule_meet" in request.form:
            date = request.form.get("date")
            phone_number = request.form.get("phone_number")

            # Insert meet and greet details into the database
            cursor.execute(
                "INSERT INTO Meet_And_Greet (Date, Time, Pet_ID, User_ID) VALUES (%s, %s, %s, %s)",
                (date.split("T")[0], date.split("T")[1], id, session["userid"]),
            )
            mysql.connection.commit()

            return redirect(url_for("home", id=id))

        elif "cancel_application" in request.form:
            # Cancel the application by updating the status to 'Canceled'
            cursor.execute(
                "UPDATE AdoptionApplication SET Application_Status = 'Canceled' "
                "WHERE Application_ID = %s AND User_ID = %s",
                (id, session["userid"]),
            )
            mysql.connection.commit()

            return redirect(url_for("home"))

        elif "delete_meet" in request.form:
            meet_date = request.form.get("meet_date")
            meet_time = request.form.get("meet_time")

            cursor.execute(
                "DELETE FROM Meet_And_Greet WHERE Date = %s AND Time = %s AND User_ID = %s",
                (meet_date, meet_time, session["userid"]),
            )
            mysql.connection.commit()
            return redirect(url_for("adoption_application", id=id))

        user_id = session["userid"]
        if not user_id:
            return "User not logged in", 403

        cursor.execute(
            "SELECT p.*, aa.* "
            "FROM Pet p "
            "JOIN Pet_Adoption pa ON p.Pet_ID = pa.Pet_ID "
            "JOIN AdoptionApplication aa ON aa.Application_ID = pa.Application_ID "
            "WHERE aa.Application_ID = %s",
            (id),
        )
        pet_application = cursor.fetchone()

        if not pet_application:
            return "Pet or application not found", 404

        return render_template(
            "adoption_application.html",
            pet=pet_application,
            application=pet_application,
        )

    return "Invalid Request", 400


@app.route("/current-applications")
def current_applications():
    user_id = session["userid"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT Application_ID, Application_Date, Application_Status FROM AdoptionApplication WHERE User_ID = %s",
        (user_id,),
    )
    applications = cursor.fetchall()

    return render_template("current_applications.html", applications=applications)


@app.route("/registerPet", methods=["GET", "POST"])
def registerPet():
    message = ""
    if (
        request.method == "POST"
        and "type" in request.form
        and "breed" in request.form
        and "dateOfBirth" in request.form
        and "vacCard" in request.form
        and "gender" in request.form
        and "description" in request.form
    ):
        # real
        # userid = session["userid"]

        # for dev purposes must be changed when in Use
        userid = "AS001"

        # get form info
        animalType = request.form["type"]
        animalBreed = request.form["breed"]
        dateOfBirth = request.form["dateOfBirth"]
        vacCard = request.form["vacCard"]
        gender = request.form["gender"]
        description = request.form["description"]
        # for test
        printer = (
            "animalType: ",
            animalType,
            "animalBreed: ",
            animalBreed,
            "dateOfBirth: ",
            dateOfBirth,
            "vacCard: ",
            vacCard,
            "gender: ",
            gender,
            "description: ",
            description,
        )
        message = printer
        # control missing info
        if (
            not animalType
            or not animalBreed
            or not dateOfBirth
            or not vacCard
            or not gender
            or not description
        ):
            message = "Please fill out the form!"
            return render_template("shelter/registerPet.html", message=message)
        # control for db
        elif (
            len(animalType) > 50
            or len(animalBreed) > 50
            or len(gender) > 10
            or len(description) > 250
            or len(vacCard) > 250
        ):
            message = "Too long texts!"
            return render_template("register.html", message=message)

        today = datetime.now().date()
        birth_date = datetime.strptime(dateOfBirth, "%Y-%m-%d").date()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        # control birth date
        if birth_date > today:
            message = "Invalid date of birth. Please enter a date in the past."
            return render_template("shelter/registerPet.html", message=message)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM AnimalShelter WHERE User_ID = %s", (userid,))
        account = cursor.fetchone()

        # checks if this is a shelter account
        if account:
            cursor.execute("SELECT * FROM Pet")
            pets = cursor.fetchall()
            lastId = 354
            # Manuel primary key increment
            for pet in pets:
                lastId = int(pet["Pet_ID"][1:])
            nextId = "P" + str(lastId + 1)
            # insert new Pet
            cursor.execute(
                "INSERT INTO Pet (Pet_ID, Name, Breed, Date_of_Birth, Age, Gender, Description, Adoption_Status, Medical_History) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    nextId,
                    animalType,
                    animalBreed,
                    dateOfBirth,
                    age,
                    gender,
                    description,
                    "notAdopted",
                    vacCard,
                ),
            )
            mysql.connection.commit()
            # increment animal count of animal shelter
            current_number_of_animals = account["Number_of_Animals"]
            updated_number_of_animals = current_number_of_animals + 1
            cursor.execute(
                "UPDATE AnimalShelter SET Number_of_Animals = %s WHERE User_ID = %s",
                (updated_number_of_animals, userid),
            )
            mysql.connection.commit()
            cursor.execute(
                "INSERT INTO lists (User_ID, Pet_ID) VALUES ( %s, %s)", (userid, nextId)
            )
            mysql.connection.commit()

        cursor.execute("SELECT * FROM lists")
        allPets = cursor.fetchall()
        # must be changed in the prod
        message = allPets
        # message = 'Pet successfully created!'
    elif request.method == "POST":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        message = "Please fill all the fields!"

    return render_template("shelter/registerPet.html", message=message)


@app.route("/current_adopted_pets", methods=["GET", "POST"])
def current_adopted_pets():
    if request.method == "GET":
        userid = session["userid"]
        message = userid
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("SELECT * FROM Pet_Adoption")
        if userid:
            cursor.execute(
                """
                    SELECT P.*
                    FROM Pet P 
                    NATURAL JOIN Pet_Adoption PA 
                    NATURAL JOIN AdoptionApplication AA 
                    WHERE AA.User_ID = %s AND AA.Application_Status = 'Approved';
                """,
                (userid,),
            )

            pets = cursor.fetchall()
            message = pets
            return render_template(
                "adoptedPets.html", message=message
            )  # , userid=userid, username=username, dept=dept, bdate=bdate, year=year, gpa=gpa)
        else:
            return redirect(url_for("login"))


@app.route("/shelterAnimalList", methods=["GET", "POST"])
def shelterAnimalList():
    if request.method == "GET":
        # assuming shelterid is stored in session
        # shelterId = session["shelterId"]
        shelterId = "AS001"
        # ^for dev purposes

        userid = session["userid"]
        if shelterId:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                """
                SELECT P.*
                FROM Pet P
                NATURAL JOIN lists L
                WHERE L.User_ID = %s
            """,
                (shelterId,),
            )

            message = cursor.fetchall()
            cursor.execute(
                "SELECT * FROM AnimalShelter WHERE User_ID = %s", (shelterId,)
            )
            AnimalS = cursor.fetchall()
            return render_template(
                "shelter/shelterAnimalList.html", message=message, animalNumber=AnimalS
            )
        else:
            return redirect(url_for("login"))


# Main Page Function
@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        userid = session["userid"]
        if userid:
            username = session["username"]
            year = session["year"]
            gpa = session["gpa"]
            dept = session["dept"]
            bdate = session["bdate"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                """
                SELECT *
                FROM apply
                NATURAL JOIN company
                WHERE sid = %s
            """,
                (userid,),
            )
            message = cursor.fetchall()
            return render_template(
                "tasks.html",
                message=message,
                userid=userid,
                username=username,
                dept=dept,
                bdate=bdate,
                year=year,
                gpa=gpa,
            )
        else:
            return redirect(url_for("login"))


# Cancel Application Function
@app.route("/cancelApplication", methods=["GET", "POST"])
def cancelApplication():
    if request.method == "POST":
        userid = session["userid"]
        if userid:
            companyId = request.form.get("cid")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute(
                    "DELETE FROM apply WHERE sid = %s AND cid = %s", (userid, companyId)
                )
                mysql.connection.commit()
                return render_template("cancelSuccessMessage.html")
            except MySQLError as e:
                return render_template("cancelFailMessage.html")
        else:
            return redirect(url_for("login"))
    return render_template("cancelFailMessage.html")


# Application Page Function
@app.route("/companies", methods=["GET", "POST"])
def companies():
    if request.method == "GET":
        userid = session["userid"]
        if userid:
            gpa = session["gpa"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT COUNT(*) AS applicationNumber FROM apply WHERE sid = %s",
                [userid],
            )
            applicationNumber = cursor.fetchone()
            if applicationNumber:
                applicationNumberVal = applicationNumber["applicationNumber"]
                if applicationNumberVal < 3:
                    cursor.execute(
                        """
                        SELECT *
                        FROM company remain
                        WHERE remain.cid NOT IN (
                            SELECT comp.cid
                            FROM company comp
                            WHERE quota = (
                                SELECT COUNT(*)
                                FROM apply
                                WHERE cid = comp.cid
                            )
                            UNION
                            SELECT app.cid
                            FROM apply app
                            WHERE app.sid = %s
                            UNION
                            SELECT DISTINCT c.cid
                            FROM company c
                            WHERE %s < c.gpaThreshold
                        )
                    """,
                        (
                            userid,
                            gpa,
                        ),
                    )
                    results = cursor.fetchall()

                    return render_template(
                        "companies.html", message=results, userid=userid
                    )
                else:
                    return render_template("quotaFullMessage.html")
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    if request.method == "POST":
        gpa = session["gpa"]
        userid = session["userid"]
        if userid:
            companyId = request.form.get("cid")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                """
                            SELECT * 
                            FROM (
                                    SELECT *
                                    FROM company remain
                                    WHERE remain.cid NOT IN (
                                        SELECT comp.cid
                                        FROM company comp
                                        WHERE quota = (
                                            SELECT COUNT(*)
                                            FROM apply
                                            WHERE cid = comp.cid
                                        )
                                        UNION
                                        SELECT app.cid
                                        FROM apply app
                                        WHERE app.sid = %s
                                        UNION
                                        SELECT DISTINCT c.cid
                                        FROM company c
                                        WHERE %s < c.gpaThreshold
                                    )
                                ) AS result
                            WHERE result.cid = %s
                        """,
                (userid, gpa, companyId),
            )
            applyresults = cursor.fetchall()
            if not applyresults:
                return render_template("applyFailMessage.html")
            else:
                cursor.execute(
                    "INSERT INTO apply (sid, cid) VALUES (%s, %s)", (userid, companyId)
                )
                mysql.connection.commit()
                return render_template("applySuccessMessage.html")
        else:
            return render_template("login.html")
    return render_template("companies.html")


# Application Summary Page Function
@app.route("/appSum", methods=["GET", "POST"])
def appSum():
    if request.method == "GET":
        userid = session["userid"]
        if userid:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                """
                SELECT c.cid, c.cname, c.quota, c.gpaThreshold
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
                ORDER BY c.quota DESC
            """,
                (userid,),
            )
            msg1 = cursor.fetchall()
            if not msg1:
                return render_template("noDataMessage.html")
            cursor.execute(
                """
            SELECT MAX(c.gpaThreshold) AS maxGpaThreshold, MIN(c.gpaThreshold) AS minGpaThreshold
            FROM apply a
            NATURAL JOIN company c
            WHERE a.sid = %s AND a.cid = c.cid
            """,
                (userid,),
            )
            msg2 = cursor.fetchall()

            cursor.execute(
                """
            SELECT c.city, COUNT(*) AS applicationCount
            FROM apply a
            NATURAL JOIN company c
            WHERE a.sid = %s AND a.cid = c.cid
            GROUP BY c.city
            """,
                (userid,),
            )
            msg3 = cursor.fetchall()

            cursor.execute(
                """
            SELECT comp.cname, temp.companyWithMaxQuota
            FROM
            (    
                SELECT MAX(c.quota) AS companyWithMaxQuota
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
            ) temp, company comp
            WHERE comp.quota= temp.companyWithMaxQuota
            """,
                (userid,),
            )
            msg4 = cursor.fetchall()

            cursor.execute(
                """
            SELECT comp.cname, temp.companyWithMinQuota
            FROM
            (    
                SELECT MIN(c.quota) AS companyWithMinQuota
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
            ) temp, company comp
            WHERE comp.quota= temp.companyWithMinQuota
            """,
                (userid,),
            )
            msg5 = cursor.fetchall()

            return render_template(
                "stats.html",
                msg1=msg1,
                msg2=msg2,
                msg3=msg3,
                msg4=msg4,
                msg5=msg5,
                userid=userid,
            )
        else:
            return redirect(url_for("login"))
    return "stats.html"


# Logout Function
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session["loggedin"] = False
        session["userid"] = None
        session["username"] = None
        session["gpa"] = None
        session["bdate"] = None
        session["year"] = None
        session["dept"] = None
        return render_template("login.html")
    if request.method == "GET":
        session["loggedin"] = False
        session["userid"] = None
        session["username"] = None
        session["gpa"] = None
        session["bdate"] = None
        session["year"] = None
        session["dept"] = None
        return render_template("login.html")
    return render_template("login.html")


# I did not use analysis. I used appSum() function as Application Summary Page Function
@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    return "Analysis page"


@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT P.*, AA.*
            FROM Pet P 
            JOIN Pet_Adoption PA ON P.Pet_ID = PA.Pet_ID
            JOIN AdoptionApplication AA ON PA.Application_ID = AA.Application_ID
            WHERE AA.Application_Status = 'Unapproved'
        """
    )

    pet_data = cursor.fetchall()

    cursor.execute(
        """
                    SELECT Pet.*
                    FROM Pet
                    LEFT JOIN Pet_Adoption ON Pet.Pet_ID = Pet_Adoption.Pet_ID
                    WHERE Pet_Adoption.Pet_ID IS NULL AND Pet.Adoption_Status = 'Unapproved'
                    """
    )

    pet_data2 = cursor.fetchall()

    cursor.execute(
        """
                    SELECT V.User_ID, U.First_Middle_Name, U.Last_Name, COUNT(A.Appointment_ID) AS NumAppointments
                    FROM Veterinarian V
                    LEFT JOIN vet_appoint VA ON V.User_ID = VA.User_ID
                    LEFT JOIN Appointment A ON VA.Appointment_ID = A.Appointment_ID
                    LEFT JOIN user U ON V.User_ID = U.User_ID
                    GROUP BY V.User_ID, U.First_Middle_Name, U.Last_Name
                    ORDER BY NumAppointments DESC
                    LIMIT 3
                    """
    )

    vet_data = cursor.fetchall()

    cursor.execute(
        """
                    SELECT U.User_ID, U.First_Middle_Name, U.Last_Name, COUNT(HP.Pet_ID) AS NumAdoptedPets
                        FROM user U
                        LEFT JOIN Has_Pet HP ON U.User_ID = HP.User_ID
                        GROUP BY U.User_ID
                        ORDER BY NumAdoptedPets DESC
                        LIMIT 3
                    """
    )

    adopt_data = cursor.fetchall()

    cursor.execute(
        """
                    SELECT P.Breed, COUNT(P.Pet_ID) AS NumAdoptions
                    FROM Pet P
                    WHERE P.Adoption_Status = 'Approved'
                    GROUP BY P.Breed
                    ORDER BY NumAdoptions DESC
                    LIMIT 3
                    """
    )

    breed_data = cursor.fetchall()
    if request.method == "GET":
        return render_template(
            "admin_panel.html",
            pet_data=pet_data,
            pet_data2=pet_data2,
            vet_data=vet_data,
            adopt_data=adopt_data,
            breed_data=breed_data,
        )

    if request.method == "POST":
        pet_id = request.form.get("pet_id")
        cursor.execute(
            "SELECT Application_ID FROM Pet_Adoption WHERE Pet_ID = %s", (pet_id,)
        )

        cursor = mysql.connection.cursor()
        if "pet_id" in request.form and "mark_unavailable" in request.form:
            pet_id = request.form.get("pet_id")

            # Perform a DELETE operation on Pet table to remove the pet
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM Pet WHERE Pet_ID = %s", (pet_id,))
            mysql.connection.commit()

        elif "approve" in request.form:
            status = "Approved"
        elif "reject" in request.form:
            status = "Rejected"
        else:
            # Handle other cases or errors here
            pass

        cursor.execute(
            "SELECT Application_ID FROM Pet_Adoption WHERE Pet_ID = %s", (pet_id,)
        )
        result = cursor.fetchone()
        if result:
            application_id = result
            try:
                cursor.execute(
                    "UPDATE AdoptionApplication SET Application_Status = %s WHERE Application_ID = %s",
                    (status, application_id),
                )
                mysql.connection.commit()
                message = "Status updated successfully!"
            except Exception as e:
                mysql.connection.rollback()
                message = f"Error: {str(e)}"
        else:
            message = "No application found for this pet."
        message += "Button submit"
        return render_template(
            "admin_panel.html",
            pet_data=pet_data,
            pet_data2=pet_data2,
            vet_data=vet_data,
            adopt_data=adopt_data,
            breed_data=breed_data,
            message=message,  # Pass the message for status update
        )


@app.route("/pet_search_page", methods=["GET", "POST"])
def pet_search():
    sql_query = """
            SELECT *
            FROM Pet P
            NATURAL JOIN AnimalShelter
            NATURAL JOIN lists
            WHERE P.Adoption_Status = 'Unapproved'
        """

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        # Get the search input and filter values from the form
        search_query = request.form.get("search-input")
        pet_type = request.form.get("pet_type")
        min_age = request.form.get("min_age")
        max_age = request.form.get("max_age")
        min_fee = request.form.get("min_fee")
        max_fee = request.form.get("max_fee")
        gender = request.form.get("gender")

        # Perform the search and filter in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Build the SQL query based on the provided filters
        sql_query = """
            SELECT *
            FROM Pet P
            NATURAL JOIN AnimalShelter
            NATURAL JOIN lists
            WHERE P.Adoption_Status = 'Unapproved'
        """

        if search_query:
            sql_query += f" AND (P.Breed LIKE '%{search_query}%')"

        if pet_type:
            sql_query += f" AND P.Type = '{pet_type}'"

        if min_age:
            sql_query += f" AND P.Age >= {min_age}"

        if max_age:
            sql_query += f" AND P.Age <= {max_age}"

        if min_fee:
            sql_query += f" AND P.Adoption_Fee >= {min_fee}"

        if max_fee:
            sql_query += f" AND P.Adoption_Fee <= {max_fee}"

        if gender:
            sql_query += f" AND P.Gender = '{gender}'"

        cursor.execute(sql_query)
        pets = cursor.fetchall()

        return render_template("pet_search_page.html", pets=pets)

    cursor.execute(sql_query)
    pets = cursor.fetchall()
    return render_template("pet_search_page.html", pets=pets)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
