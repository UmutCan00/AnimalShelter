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
    return render_template("auth/home.html")


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
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
        and "confirm_password" in request.form
        and "name" in request.form
        and "surname" in request.form
        and "phone" in request.form
        and "role" in request.form
    ):
        email = str(request.form["email"])
        password = str(request.form["password"])
        confirm_password = str(request.form["confirm_password"])
        name = str(request.form["name"])
        surname = str(request.form["surname"])
        phone = str(request.form["phone"])
        role = str(request.form["role"])

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
            cursor.execute(
                "INSERT INTO user (User_ID, Password, First_Middle_Name, Last_Name, Email, Phone_Number) VALUES (%s, %s, %s, %s, %s, %s)",
                (email, password, name, surname, email, phone),
            )
            mysql.connection.commit()
            message = "User successfully registered!"
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


@app.route("/user-pets")
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
    cursor.execute(
        "SELECT u.User_ID, CONCAT(u.First_Middle_Name, ' ', u.Last_Name) AS Full_Name FROM user u, Veterinarian v WHERE u.User_ID = v.User_ID;"
    )
    veterinarians = cursor.fetchall()
    veterinarians_array = []
    for vet in veterinarians:
        vet_array = list(vet)
        veterinarians_array.append(vet_array)

    if request.method == "POST":
        email = request.form["email"]
        fullname = request.form["fullname"]
        problems = request.form["problems"]
        appointment_time = request.form["appointment-time"]
        selected_vet = request.form["veterinarian"]

        print(f"Email: {email}")
        print(f"Full Name: {fullname}")
        print(f"Problems: {problems}")
        print(f"Appointment Time: {appointment_time}")
        # print(f"Selected Veterinarian: {veterinarians.get(selected_vet)}")

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
        message=veterinarians,
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


@app.route("/adoption-application/<int:id>", methods=["GET", "POST"])
def adoption_application(id):
    pet = pets_data.get(id)
    application = applications_data.get(id)

    if not pet or not application:
        return "Pet or application not found", 404

    status = (
        "Approved"
        if application["Admin_Approved"] and application["Shelter_Approved"]
        else "Pending"
    )

    if request.method == "POST":
        if "schedule_meet" in request.form:
            date = request.form.get("date")
            phone_number = request.form.get("phone_number")

            return redirect(url_for("home", id=id))

        elif "cancel_application" in request.form:
            del applications_data[id]
            return redirect(url_for("home"))

    return render_template(
        "adoption_application.html", pet=pet, application=application, status=status
    )


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
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            """
                SELECT P.*
                FROM Pet P 
                JOIN Pet_Adoption PA ON P.Pet_ID = PA.Pet_ID
                JOIN AdoptionApplication AA ON PA.Application_ID = AA.Application_ID
                WHERE AA.Application_Status <> 'Approved';

            """
        )

        pet_data = cursor.fetchall() 
        
        cursor.execute("""SELECT Pet.*
            FROM Pet
            LEFT JOIN Pet_Adoption ON Pet.Pet_ID = Pet_Adoption.Pet_ID
            WHERE Pet_Adoption.Pet_ID IS NULL;
        """)
        
        pet_data2 = cursor.fetchall()


        cursor.execute("""SELECT V.User_ID, U.First_Middle_Name, U.Last_Name, COUNT(A.Appointment_ID) AS NumAppointments
            FROM Veterinarian V
            LEFT JOIN vet_appoint VA ON V.User_ID = VA.User_ID
            LEFT JOIN Appointment A ON VA.Appointment_ID = A.Appointment_ID
            LEFT JOIN user U ON V.User_ID = U.User_ID
            GROUP BY V.User_ID, U.First_Middle_Name, U.Last_Name
            ORDER BY NumAppointments DESC
            LIMIT 3;
        """)    
        
        vet_data = cursor.fetchall()

        cursor.execute("""SELECT U.User_ID, U.First_Middle_Name, U.Last_Name, COUNT(PA.Pet_ID) AS NumAdoptedPets
            FROM user U
            LEFT JOIN AdoptionApplication AA ON U.User_ID = AA.User_ID
            LEFT JOIN Pet_Adoption PA ON AA.Application_ID = PA.Application_ID
            GROUP BY U.User_ID
            ORDER BY NumAdoptedPets DESC
            LIMIT 3;
        """)
        
        adopt_data = cursor.fetchall()

        cursor.execute("""SELECT P.Breed, COUNT(PA.Pet_ID) AS NumAdoptions
            FROM Pet P
            LEFT JOIN Pet_Adoption PA ON P.Pet_ID = PA.Pet_ID
            GROUP BY P.Breed
            ORDER BY NumAdoptions DESC
            LIMIT 3;
        """)
                
        breed_data = cursor.fetchall()
        
        return render_template("admin_panel.html", pet_data = pet_data, 
                               pet_data2 = pet_data2, vet_data = vet_data, 
                               adopt_data = adopt_data, breed_data = breed_data)

@app.route('/pet_search_page', methods=['GET', 'POST'])
def pet_search():
    sql_query = """
            SELECT *
            FROM Pet P
            NATURAL JOIN AnimalShelter
            NATURAL JOIN lists
            WHERE P.Adoption_Status = 'Unapproved'
        """
            
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        # Get the search input and filter values from the form
        search_query = request.form.get('search-input')
        pet_type = request.form.get('pet_type')
        min_age = request.form.get('min_age')
        max_age = request.form.get('max_age')
        gender = request.form.get('gender')

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

        if gender:
            sql_query += f" AND P.Gender = '{gender}'"

        cursor.execute(sql_query)
        pets = cursor.fetchall()
        
        return render_template('pet_search_page.html', pets=pets)

    cursor.execute(sql_query)
    pets = cursor.fetchall()
    return render_template('pet_search_page.html', pets=pets)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
