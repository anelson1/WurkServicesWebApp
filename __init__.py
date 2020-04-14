
from flask import Flask, render_template, request
from waitress import serve
import psycopg2
import random
import string
import os
import config as cfg


app = Flask(__name__, instance_relative_config=True)
conn = psycopg2.connect(user =cfg.info["user"],password = cfg.info["passwd"],host = cfg.info["host"],port = "5432",database = cfg.info["db"])
cursor = conn.cursor()
@app.route("/")
def hello():
    return render_template('index.html')
@app.route("/meeting", methods = ['post'])
def meet():
    print(request.form['MID'])
    selecting = "SELECT * FROM bookings natural join bookingtimes WHERE bid = " + "'"+str(request.form['MID'])+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    for i in records:
        print(i)
    if len(records) != 0:
        meetingIDSQL = records[0][0]
        student = records[0][1]
        teacherSQL = records[0][2]
        monthSQL = records[0][4]
        daySQL = records[0][5]
        startSQL = records[0][6]
        endSQL = records[0][7]
        tob = records[0][3]
        return render_template('meeting.html',meetingID = meetingIDSQL, teacher = teacherSQL,month = monthSQL, start = startSQL, end = endSQL, day = daySQL, TOB = tob)
    else:
        return render_template('error.html',error = 'Error: Meeting ID not found',lastpage = '')
@app.route("/registered", methods = ['post'])
def registered():
    username = request.form['uname'].lower()
    password = request.form['pass']
    confpass = request.form['confpass']
    email = request.form['email']
    phonenumber = request.form['pnum']
    address = request.form['addr']
    city = request.form['city']
    state = request.form['state']
    fname = request.form['fname']
    lname = request.form['lname']
    selecting = "SELECT * FROM users WHERE username = '" + str(username)+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    if len(records) != 0:
        return render_template('error.html',error = 'Error: User with this username already exists, try logging in',lastpage = 'register')
    elif password != confpass:
        return render_template('error.html',error = 'Error: Passwords do not match',lastpage = 'register')
    elif '@' not in email:
        return render_template('error.html',error = 'Error: Invalid Email Address',lastpage = 'register')
    else:
        insert = "INSERT INTO users VALUES ('"+str(username)+"','"+str(password)+"','"+str(email)+"','"+str(phonenumber)+"','"+str(address)+"','"+str(city)+"','"+str(state)+ "','"+str(fname)+"','"+str(lname)+"')"
        cursor.execute(insert)
        conn.commit()
        return render_template('registered.html')

@app.route("/useraccount", methods = ['post'])
def useraccount():
    username = request.form['uname'].lower()
    password = request.form['password']
    if username == '':
        return render_template('error.html', error = 'Error: Invalid Username or Password', lastpage = '')
    selecting = "SELECT * FROM users WHERE username = " + "'"+str(username)+"' AND password = '"+str(password)+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    if username == 'admin' and len(records) != 0:
        selecting12 = "select * from bookings natural join bookingtimes"
        cursor.execute(selecting12)
        records12 = cursor.fetchall()
        return render_template('adminpage.html', uname = records[0][7], records = records12, len = len(records12), len2 = len(records12[0]))
    elif len(records) != 0:
        return render_template('useraccount.html', uname = records[0][7])
    else:
        return render_template('error.html', error = 'Error: Invalid Username or Password', lastpage = '')
@app.route("/created", methods = ['post'])
def create():
    tid = request.form['tid']
    month = request.form['month']
    day = request.form['day']
    st = request.form['st']
    et = request.form['et']
    name = "SELECT * FROM teacher WHERE tid = '"+str(tid)+"'"
    cursor.execute(name)
    records = cursor.fetchall()
    timeelapsed = 0
    if(len(records) == 0):
        return render_template('error.html', error = 'Error: you entered an invalid Teacher ID, please try again', lastpage = 'SuperSecretTeacherPage')
    else:
         intst = int(st)
         intet = int(et)
         print("start: " + str(intst) + "end: " + str(intet))
         if intst > intet:
            while intst < 24:
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst+=1
                conn.commit()
            intst = 1;
            for i in range(intet - 1):
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst+=1
                conn.commit()
         else:
            timeelapsed = intet - intst
            for i in range(timeelapsed):
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst+=1
                conn.commit()
         return render_template('created.html', lastpage = 'SuperSecretTeacherPage')
@app.route("/register")
def register():
    return render_template('register.html')
@app.route("/createbooking", methods = ['post'])
def CB2():
    name = request.form['name']
    month = request.form['month']
    day = request.form['day']
    typeofbooking = request.form['TOB']
    if typeofbooking == 'Acedemic Tutoring' or typeofbooking == 'Music Lessons' or typeofbooking == 'ACT and SAT Prep' or typeofbooking == 'Sports Coaching':
        select = "SELECT stuname from bookings where stuname = '" + str(name) +"'"
        cursor.execute(select)
        behiminey = cursor.fetchall()
        teachSelect = " SELECT firstname,lastname from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE day = '" +str(day)+"' AND month = '"+ str(month)+"' AND typeofteacher = '" + str(typeofbooking)+"'"
        cursor.execute(teachSelect)
        teacherList = cursor.fetchall()
        if len(teacherList) == 0:
            return render_template('error.html', error = 'Error: No teachers are avaliable on that day, please try again or contact us for custom avalibility', lastpage = '')
        newTeacherList = list(dict.fromkeys(teacherList))
        return render_template('CB2.html', nameList = newTeacherList, name = name, month = month, day = day,TOB = typeofbooking)
    else:
        return render_template('CB2-nonacedemic.html', name = name, month = month, day = day, TOB = typeofbooking)
@app.route("/createbooking2", methods = ['post'])
def CB3():
    name = request.form['name']
    month = request.form['month']
    day = request.form['day']
    teacher = request.form['teachers']
    typeofbooking = request.form['TOB']
    if typeofbooking == 'Acedemic Tutoring' or typeofbooking == 'Music Lessons' or typeofbooking == 'ACT and SAT Prep' or typeofbooking == 'Sports Coaching':
        timeSelect = " SELECT starttime,endtime from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE firstname = '"+str(teacher)+"'"
        cursor.execute(timeSelect)
        times = cursor.fetchall()
        teachSelect = " SELECT firstname,lastname from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE day = '" +str(day)+"' AND month = '"+ str(month)+"' AND typeofteacher = '" + str(typeofbooking)+"'"
        cursor.execute(teachSelect)
        teacherList = cursor.fetchall()
        newTeacherList = list(dict.fromkeys(teacherList))
        for i in range(len(times)):
            for j in range(len(times[i])):
                if(times[i][j] == '1'):
                    tempList = list(times[i])
                    tempList[j] = "1am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '2'):
                    tempList = list(times[i])
                    tempList[j] = "2am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '3'):
                    tempList = list(times[i])
                    tempList[j] = "3am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '4'):
                    tempList = list(times[i])
                    tempList[j] = "4am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '5'):
                    tempList = list(times[i])
                    tempList[j] = "5am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '6'):
                    tempList = list(times[i])
                    tempList[j] = "6am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '7'):
                    tempList = list(times[i])
                    tempList[j] = "7am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '8'):
                    tempList = list(times[i])
                    tempList[j] = "8am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '9'):
                    tempList = list(times[i])
                    tempList[j] = "9am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '10'):
                    tempList = list(times[i])
                    tempList[j] = "10am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '11'):
                    tempList = list(times[i])
                    tempList[j] = "11am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '12'):
                    tempList = list(times[i])
                    tempList[j] = "12am"
                    times[i] = tuple(tempList)
                if(times[i][j] == '13'):
                    tempList = list(times[i])
                    tempList[j] = "1pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '14'):
                    tempList = list(times[i])
                    tempList[j] = "2pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '15'):
                    tempList = list(times[i])
                    tempList[j] = "3pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '16'):
                    tempList = list(times[i])
                    tempList[j] = "4pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '17'):
                    tempList = list(times[i])
                    tempList[j] = "5pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '18'):
                    tempList = list(times[i])
                    tempList[j] = "6pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '19'):
                    tempList = list(times[i])
                    tempList[j] = "7pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '20'):
                    tempList = list(times[i])
                    tempList[j] = "8pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '21'):
                    tempList = list(times[i])
                    tempList[j] = "9pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '22'):
                    tempList = list(times[i])
                    tempList[j] = "10pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '23'):
                    tempList = list(times[i])
                    tempList[j] = "11pm"
                    times[i] = tuple(tempList)
                if(times[i][j] == '24'):
                    tempList = list(times[i])
                    tempList[j] = "12am"
                    times[i] = tuple(tempList)
        return render_template('CB3.html', timesList = times, nameList = newTeacherList, teacherName = teacher, name = name, month = month, day = day, TOB = typeofbooking)
@app.route("/BookingComplete",methods = ['post'])
def BC():
    name = request.form['name']
    month = request.form['month']
    day = request.form['day']
    typeofbooking = request.form['TOB']
    BID = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
    print("TOB: " + typeofbooking)
    if typeofbooking == 'Acedemic Tutoring' or typeofbooking == 'Music Lessons' or typeofbooking == 'ACT and SAT Prep' or typeofbooking == 'Sports Coaching':
        print("we innie boys")
        teacher = request.form['teacher']
        times = request.form['times']
        goodtimes = times.split()

        select = "SELECT stuname from bookings where stuname = '" + str(name) +"'"
        cursor.execute(select)
        behiminey = cursor.fetchall()
        if len(behiminey) != 0:
            return render_template('error.html', error = "Error: You already have a booking" ,lastpage = "/")
        insert1 = "INSERT INTO bookings VALUES ('"+str(BID)+"','"+str(name)+"','"+str(teacher)+"','"+str(typeofbooking)+"')"
        cursor.execute(insert1)
        conn.commit()
        insert2 = "INSERT INTO bookingtimes VALUES ('"+str(BID)+"','"+str(month)+"','"+str(day)+"','"+str(goodtimes[0])+"','"+str(goodtimes[1])+"')"
        cursor.execute(insert2)
        conn.commit()
        fixedst = goodtimes[0].replace('am','')
        fixedet = goodtimes[1].replace('am','')
        fixedst = goodtimes[0].replace('pm','')
        fixedet = goodtimes[1].replace('pm','')

        remove = "DELETE FROM teacherbook where starttime = '"+str(fixedst)+"' AND endtime = '"+str(fixedet)+"'"
        cursor.execute(remove)
        conn.commit()

        print(name,month,day,teacher,times,BID,fixedst,fixedet)
        return render_template('BookingComplete.html',BID = BID)
    else:
        starttime = request.form['st']
        insert1 = "INSERT INTO bookings VALUES ('"+str(BID)+"','"+str(name)+"','"+''+"','"+str(typeofbooking)+"')"
        cursor.execute(insert1)
        conn.commit()
        insert2 = "INSERT INTO bookingtimes VALUES ('"+str(BID)+"','"+str(month)+"','"+str(day)+"','"+str(starttime)+"')"
        cursor.execute(insert2)
        conn.commit()
        return render_template('BookingComplete.html',BID = BID)
@app.route("/admino", methods = ['post'])
def admin():
     FN = request.form['FN']
     LN = request.form['LN']
     TOT = request.form['TOT']
     TID = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])
     insert1 = "INSERT INTO teacher VALUES ('"+str(TID)+"','"+str(FN)+"','"+str(LN)+"','"+str(TOT)+"')"
     cursor.execute(insert1)
     conn.commit()
     return render_template('adminpage.html')

@app.route("/BodyOfWork")
def bigbody():
    return render_template('BOW.html')
@app.route("/ContactUs")
def abutus():
    return render_template('contactus.html')
@app.route("/MeetTheTeam")
def dateam():
    return render_template('MTT.html')
@app.route("/SuperSecretTeacherPage")
def SSTP():
    return render_template('supersecretteacherpage.html')
@app.route("/test")
def test():
    return render_template('test.html')
@app.route("/login")
def log():
    return render_template('login.html')
if __name__ == "__main__":
    app.run(debug=True)
    #serve(app, listen = '*:80')
