#CS353-1 Homework 4
#Cenker Akan
#22102295
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__) 

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'AnimalShelter'
  
mysql = MySQL(app)

#Home Page Function
@app.route('/', methods =['GET'])
def home():
    return render_template('auth/home.html')


#Login Page Function
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(email);
        print(password);
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE Email = % s AND Password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            print("entered")
            session['loggedin'] = True
            session['userid'] = user['User_ID']
            message = 'Logged in successfully!'
            return redirect(url_for('suite'))
        else:
            message = 'Please enter correct password !'
    return render_template('auth/login.html', message = message)

@app.route('/suite', methods =['GET'])
def suite():
    return render_template('auth/suite.html')

#Signup Page Function
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'date' in request.form and 'dept' in request.form and 'year' in request.form and 'gpa' in request.form:
        username = request.form['username']
        password = request.form['password']
        bdate = request.form['date']
        dept = request.form['dept']
        year = request.form['year']
        gpa = request.form['gpa']
        if not username or not password or not bdate or not dept or not year or not gpa:
            message = 'Please fill out the form!'
            return render_template('register.html', message = message)
        elif not gpa.replace(".", "", 1).isdigit() or float(gpa)>4 or float(gpa)<0:
            message = 'Wrong GPA value!'
            return render_template('register.html', message = message)
        elif (len(dept) > 2):
            message = 'Please enter Department code using two characters!'
            return render_template('register.html', message = message)
        elif len(password)>6 or len(year) >15 or len(username) >50:
            message = 'Form values are too long!'
            return render_template('register.html', message = message)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE sname = %s', (username,))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'
            return render_template('register.html', message = message)
        else:
            cursor.execute('INSERT INTO student (sid, sname, bdate, dept, year, gpa) VALUES (%s, %s, %s, %s, %s, %s)', (username, password, bdate, dept, year, gpa))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'
    
    return render_template('register.html', message = message)

@app.route('/registerPet', methods =['GET', 'POST'])
def registerPet():
    message = ''
    if request.method == 'POST' and 'type' in request.form and 'breed' in request.form and 'dateOfBirth' in request.form and 'vacCard' in request.form and 'petImage' in request.form and 'adoptionFee' in request.form and 'description' in request.form:
        userid = session["userid"]
        
        animalType = request.form['type']
        animalBreed = request.form['breed']
        dateOfBirth = request.form['dateOfBirth']
        vacCard = request.form['vacCard']
        petImage = request.form['petImage']
        adoptionFee = request.form['adoptionFee']
        description = request.form['description']
        
        if not animalType or not animalBreed or not dateOfBirth or not vacCard or not description:
            message = 'Please fill out the form!'
            return render_template('shelter/registerPet.html', message = message)
    elif request.method == 'POST':
        message = 'Please fill all the fields!'
    
    return render_template('shelter/registerPet.html', message = message)

#Main Page Function
@app.route('/tasks', methods =['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        userid = session["userid"]
        if userid:
            username = session["username"]
            year = session["year"]
            gpa = session["gpa"]
            dept = session["dept"]
            bdate = session["bdate"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
                SELECT *
                FROM apply
                NATURAL JOIN company
                WHERE sid = %s
            ''', (userid,))
            message = cursor.fetchall()
            return render_template('tasks.html', message=message, userid=userid, username=username, dept=dept, bdate=bdate, year=year, gpa=gpa)
        else:
            return redirect(url_for('login'))

#Cancel Application Function
@app.route('/cancelApplication', methods =['GET', 'POST'])
def cancelApplication():
    if request.method == 'POST':
        userid = session["userid"]
        if userid:
            companyId = request.form.get('cid')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute('DELETE FROM apply WHERE sid = %s AND cid = %s', (userid, companyId))
                mysql.connection.commit()
                return render_template('cancelSuccessMessage.html')
            except MySQLError as e:
                return render_template('cancelFailMessage.html')
        else:
            return redirect(url_for('login'))
    return render_template('cancelFailMessage.html')

#Application Page Function
@app.route('/companies', methods =['GET', 'POST'])
def companies():
    if request.method == 'GET':
        userid = session["userid"]
        if userid:
            gpa = session["gpa"]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) AS applicationNumber FROM apply WHERE sid = %s", [userid])
            applicationNumber = cursor.fetchone()
            if applicationNumber: 
                applicationNumberVal = applicationNumber['applicationNumber']
                if applicationNumberVal<3 :
                    cursor.execute('''
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
                    ''', (userid,gpa,))
                    results = cursor.fetchall()
                    
                    return render_template('companies.html', message=results, userid=userid)
                else:
                    return render_template('quotaFullMessage.html')
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    if request.method == 'POST':
        gpa = session["gpa"]
        userid = session["userid"]
        if userid:
            companyId = request.form.get('cid')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
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
                        ''', (userid,gpa,companyId))
            applyresults = cursor.fetchall()
            if not applyresults:
                return render_template('applyFailMessage.html')
            else:
                cursor.execute('INSERT INTO apply (sid, cid) VALUES (%s, %s)', (userid, companyId))
                mysql.connection.commit()
                return render_template('applySuccessMessage.html')    
        else:
            return render_template('login.html')
    return render_template('companies.html')

#Application Summary Page Function
@app.route('/appSum', methods =['GET', 'POST'])
def appSum():
    if request.method == 'GET':
        userid = session["userid"]
        if userid:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
                SELECT c.cid, c.cname, c.quota, c.gpaThreshold
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
                ORDER BY c.quota DESC
            ''', (userid,))
            msg1 = cursor.fetchall()
            if not msg1:
                return render_template('noDataMessage.html')
            cursor.execute('''
            SELECT MAX(c.gpaThreshold) AS maxGpaThreshold, MIN(c.gpaThreshold) AS minGpaThreshold
            FROM apply a
            NATURAL JOIN company c
            WHERE a.sid = %s AND a.cid = c.cid
            ''', (userid,))
            msg2 = cursor.fetchall()
            
            cursor.execute('''
            SELECT c.city, COUNT(*) AS applicationCount
            FROM apply a
            NATURAL JOIN company c
            WHERE a.sid = %s AND a.cid = c.cid
            GROUP BY c.city
            ''', (userid,))
            msg3 = cursor.fetchall()
            
            cursor.execute('''
            SELECT comp.cname, temp.companyWithMaxQuota
            FROM
            (    
                SELECT MAX(c.quota) AS companyWithMaxQuota
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
            ) temp, company comp
            WHERE comp.quota= temp.companyWithMaxQuota
            ''', (userid,))
            msg4 = cursor.fetchall()
            
            cursor.execute('''
            SELECT comp.cname, temp.companyWithMinQuota
            FROM
            (    
                SELECT MIN(c.quota) AS companyWithMinQuota
                FROM apply a
                NATURAL JOIN company c
                WHERE a.sid = %s AND a.cid = c.cid
            ) temp, company comp
            WHERE comp.quota= temp.companyWithMinQuota
            ''', (userid,))
            msg5 = cursor.fetchall()
            
            return render_template('stats.html', msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, userid=userid)
        else:
            return redirect(url_for('login'))
    return "stats.html"

#Logout Function
@app.route('/logout', methods =['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session['loggedin'] = False
        session['userid'] = None
        session['username'] = None
        session['gpa'] = None
        session['bdate'] = None
        session['year'] = None
        session['dept'] = None
        return render_template('login.html')
    if request.method == 'GET':
        session['loggedin'] = False
        session['userid'] = None
        session['username'] = None
        session['gpa'] = None
        session['bdate'] = None
        session['year'] = None
        session['dept'] = None
        return render_template('login.html')
    return render_template('login.html')

#I did not use analysis. I used appSum() function as Application Summary Page Function
@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    return "Analysis page"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
