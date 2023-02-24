from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3

app=Flask(__name__)
app.secret_key='1234'

@app.route('/')
def index():
    return render_template('1home.html')

@app.route('/Admin_loginpage')
def adminlogin():
    return render_template('2adminlogin.html')


@app.route('/Ad_login',methods=['GET','POST'])
def adminpage():
    if request.method=='POST':
        Uname=request.form['name']
        Upwd=request.form['password']


        global Adminname
        Adminname = Uname

        import sqlite3
        con=sqlite3.connect('schooladmins.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute('SELECT * from admins where name=? and pwd=?',(Uname,Upwd))
        AdminDATA=cur.fetchone()




        if AdminDATA:
            Uname == AdminDATA['name']
            Upwd == AdminDATA['pwd']

            global adminname
            adminname=Uname

            return render_template('3adminpage.html', Username=Uname)

        else:
            flash('username and password mismatch','danger')
            return render_template('2adminlogin.html')
    return render_template('2adminlogin.html')

@app.route('/Adminactivities')
def admin_activities():
    user='Siva'
    return render_template('3adminpage.html',Username=user)


@app.route('/Add_student')
def add_student():
    return render_template('4addstudent.html')

@app.route('/New_Registration',methods=['POST','GET'])
def Newregistration():
    if request.method=='POST':
        Sname=request.form.get('name')
        Sdob = request.form.get('dob')
        Sfather = request.form.get('fname')
        Smother = request.form.get('mname')
        Saddress = request.form.get('address')
        Smail = request.form.get('mail')
        Scontact = request.form.get('contact')

        con=sqlite3.connect('studentdetail.db')
        cur=con.cursor()
        qry="INSERT INTO students (name,dob,fathername,mothername,address,mail,contact,password) VALUES (?,?,?,?,?,?,?,?)"
        tup_word=(Sname,Sdob,Sfather,Smother,Saddress,Smail,Scontact ,Smail)
        cur.execute(qry,tup_word)
        con.commit()

        con = sqlite3.connect('studentdetail.db')
        cur = con.cursor()
        q="SELECT * FROM students WHERE name=? AND dob=?"
        tup=(Sname,Sdob)
        cur.execute(q,tup)
        ans=cur.fetchone()

        myrollno=ans[0]
        flash('added Successfully','success')
        con.close()
        return render_template('4addstudent.html',Sname=Sname,myrollno=myrollno)


    else:
        flash('Error in Updating',danger)



@app.route('/Add_examDetail')
def add_examdetails():
    return render_template('5addexamdetails.html')

@app.route('/Markregister',methods=['POST','GET'])
def markregister():
    if request.method=='POST':
        Sroll=request.form.get('rollno')
        Stamil = int(request.form.get('tamil'))
        Senglish =int( request.form.get('english'))
        Smaths = int(request.form.get('maths'))
        Sscience = int(request.form.get('science'))
        Ssocial =int( request.form.get('social'))

        Stotal=Stamil+Senglish+Smaths+Sscience+Ssocial
        Savg=Stotal/5

        if((Stamil>=35) & (Senglish>=35) & (Smaths>=35) & (Sscience>=35) & (Ssocial>=35) ):
            Sresult='pass'
        else:
            Sresult='fail'

        con = sqlite3.connect('studentdetail.db')
        cur = con.cursor()
        qry="UPDATE students SET tamil=?,english=?,maths=?,science=?,social=?,total=?,average=?,result=? WHERE rollno=? "
        tup_word = (Stamil,Senglish,Smaths,Sscience,Ssocial,Stotal,Savg,Sresult,Sroll)
        cur.execute(qry, tup_word)
        con.commit()
        flash('added Successfully','success')
        return render_template('5addexamdetails.html',Sroll=Sroll)
        con.close()

    else:
        flash('Error in Updating','danger')
        return render_template('5addexamdetails.html')
        con.close()


#ranklist database
def ranking():
    import sqlite3
    connection = sqlite3.connect('studentdetail.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name,total,result,rank,rollno FROM students order by total DESC ")
    result = cursor.fetchall()

    '''convert tuple to list'''
    mylist1 = []
    for i in result:
        mylist1.append(list(i))

    n = 1
    old = 0
    for i in mylist1:
        if i[2] == 'pass':  # i[2]=result
            if old == i[1]:  # i[1] total
                old = i[1]
                n = n - 1
                i[3] = n  # i[3] rank
            else:
                old = i[1]
                i[3] = n  # i[3] rank
            n = n + 1
            # print("Rank holders",i[3],i[0])
        else:
            continue

    MYLIST2 = []
    for i in mylist1:
        MYLIST2.append(tuple(i))


    connection = sqlite3.connect('studentdetail.db')
    cursor = connection.cursor()
    qry = "UPDATE students SET name=?,total=?,result=?,rank=? WHERE rollno=?"
    for i in MYLIST2:
        cursor.execute(qry, i)
    connection.commit()



@app.route('/Overalldatabase')
def Overall_database():
    ranking()
    con = sqlite3.connect('studentdetail.db')
    con.row_factory=sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM students')
    Result= cur.fetchall()
    con.close()
    return render_template('6overalldatabase.html',Result=Result)

'''step2:create update record route link 182 to 190 & 236'''

@app.route('/Update_record/<string:id>',methods=['POST','GET'])
def Update_myrecord(id):
    con=sqlite3.connect('studentdetail.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute('SELECT * FROM students WHERE rollno=?',(id,))
    MYDATA=cur.fetchone()

    #step4: get detils from update page 192 to 234
    if request.method=='POST':
        try:
            Uname=request.form['name']
            Udob = request.form['dob']
            Ufname = request.form['fname']
            Umname = request.form['mname']

            Uaddress = request.form['address']
            Umail = request.form['mail']
            Ucontact = request.form['contact']
            Upassword = request.form['password']

            Utamil = int(request.form.get('tamil'))
            Uenglish =int(request.form.get('english'))
            Umaths = int(request.form.get('maths'))
            Uscience = int(request.form.get('science'))
            Usocial = int(request.form.get('social'))

            Utotal = Utamil  + Uenglish+ Umaths + Uscience + Usocial
            Uavg = Utotal / 5

            if ((Utamil  >= 35) & ( Uenglish >= 35) & ( Umaths >= 35) & (Uscience  >= 35) & (Usocial >= 35)):
                Uresult = 'pass'
            else:
                Uresult = 'fail'

            con=sqlite3.connect('studentdetail.db')
            cur=con.cursor()
            qry="UPDATE students SET name=?,dob=?,fathername=?,mothername=?,address=?,mail=?,contact=?,password=?,tamil=?,english=?,maths=?,science=?,social=?,total=?,average=?,result=? WHERE rollno=?"
            tup=(Uname,Udob,Ufname,Umname,Uaddress,Umail,Ucontact,Upassword,Utamil,Uenglish,Umaths,Uscience,Usocial,Utotal,Uavg,Uresult,id)
            cur.execute(qry,tup)
            con.commit()

            flash('Record Updated Successfully','success')

        except Exception as E:
            print(E,'error')
            flash("Error in Updating",'danger')
        finally:
            dummy='Sivaraman'
            return render_template('3adminpage.html',Username=dummy)
            con.close()
    # step2:
    return render_template('10update.html',MYDATA=MYDATA)   #step2:

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=sqlite3.connect('studentdetail.db')
        cur=con.cursor()
        cur.execute('DELETE   FROM students WHERE rollno=?',(id,))
        con.commit()
        flash('Record deleted successfully','success')
    except Exception as E:
        print(E)
        flash('Error in deleting Record','danger')
    finally:
        #return redirect(url_for)
        dummy='sivaraman'
        return render_template('3adminpage.html', Username=dummy)
    con.close()


@app.route('/View_ranklist')
def view_ranklist():
    ranking()
    con = sqlite3.connect('studentdetail.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE result='pass' ")
    Mydata = cur.fetchall()
    con.close()
    return render_template('7viewranklist.html',Mydata=Mydata)

@app.route('/View_failures')
def view_failures_list():
    ranking()
    con = sqlite3.connect('studentdetail.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE result='fail' ")
    Mydata = cur.fetchall()
    con.close()
    return render_template('8view_failures_list.html',Mydata=Mydata)




@app.route('/View_coachingclass')
def view_coachingclass():
    ranking()

    con = sqlite3.connect('studentdetail.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT rollno,name,tamil,english,maths,science,social FROM students WHERE result='fail' ")
    Mydata = cur.fetchall()

    Tamil = []
    English = []
    Maths = []
    Science = []
    Social = []
    for i in Mydata:
        if i[2] < 35:
            Tamil.append(i[1])
        if i[3] < 35:
            English.append(i[1])
        if i[4] < 35:
            Maths.append(i[1])
        if i[5] < 35:
            Science.append(i[1])
        if i[6] < 35:
            Social.append(i[1])


    return render_template('9coachingclass.html', Tamil=Tamil, English=English, Maths=Maths, Science=Science,
    Social=Social)


@app.route('/admin_forgotpwd',methods=['POST','GET'])
def admin_forgotpwd():
    if request.method=='POST':
        Fname=request.form.get('name')
        Fdob=request.form.get('dob')
        print('Fname', Fname)
        print(Fdob, Fdob)
        import sqlite3
        con = sqlite3.connect('schooladmins.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * from admins where name=? and dob=?', (Fname,Fdob))
        FDATA = cur.fetchone()

        if FDATA:
            Dname=FDATA['name'].title()
            Ddob= FDATA['dob']
            Fname == Dname
            Fdob  ==Ddob
            return render_template('12admin_conpwd.html',username=Fname)
        else:
            flash('username or DOB mismatch or No USER in this name', 'danger')
            return render_template('11adminforgotpwd.html')
    return render_template('11adminforgotpwd.html')



@app.route('/admin_changepwd',methods=['POST','GET'])
def admin_changepwdF():
    if request.method=='POST':
        Uname = (request.form.get('Uname')).title()
        CHpwd=request.form.get('pwd1')
        Cpwd=request.form.get('pwd2')

        if  (CHpwd==Cpwd):
            con = sqlite3.connect('schooladmins.db')
            cur = con.cursor()
            qry = "UPDATE admins SET pwd=? WHERE name=?"
            tup_word = (CHpwd,Uname)
            cur.execute(qry,tup_word)
            con.commit()
            flash('Pasword changed successfully', 'success')
            return render_template('2adminlogin.html')
        else:
            flash('Password and Confirm password mismatch', 'danger')
            return render_template('12admin_conpwd.html')
    return render_template('12admin_conpwd.html')


@app.route('/new_adminreg',methods=['POST','GET'])
def new_adminreg():
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        pwd = request.form.get('pwd')
        favplace = request.form.get('favplace')
        mail = request.form.get('mail')
        scode = request.form.get('scode')

        if (scode == 'siva1997' or 'SIVA1997'):
            con = sqlite3.connect('schooladmins.db')
            cur = con.cursor()
            qry = "INSERT INTO admins (name,dob,pwd,favplace,mail) VALUES (?,?,?,?,?)"
            tup_word = (name,dob,pwd,favplace,mail)
            cur.execute(qry, tup_word)
            con.commit()
            flash('New Admin registered successfully', 'success')
            return render_template('2adminlogin.html')
        else:
            flash('secret code doesnot match', 'danger')
            return render_template('13new_admin.html')
    return render_template('13new_admin.html')


@app.route('/Student_loginpage')
def studentlogin():
    return render_template('21studentlogin.html')

def Candidatename(abc):
    global Can_data
    Can_data = abc


@app.route('/St_login',methods=['GET','POST'])
def studentpage():
    if request.method=='POST':
        Uname=(request.form['name']).title()
        Upwd=request.form['password']

        import sqlite3
        con=sqlite3.connect('studentdetail.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute('SELECT * from students where name=? and password=?',(Uname,Upwd))
        Stud_Data=cur.fetchone()

        Candidatename(Stud_Data)

        if Stud_Data:
            StName=Stud_Data['name']

            Uname == StName.title()
            Upwd == Stud_Data['password']
            return render_template('22studentpage.html',USERDATA=Stud_Data)

        else:
            flash('username and password mismatch','danger')
            return render_template('21studentlogin.html')
    return render_template('21studentlogin.html')


@app.route('/Studentactivities')
def student_activities():
    return render_template('22studentpage.html',USERDATA=Can_data)

@app.route('/biodata/<string:id>',methods=['POST','GET'])
def View_Biodata(id):
    con=sqlite3.connect('studentdetail.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute('SELECT * FROM students where rollno=? ',(id,))
    BIODATA=cur.fetchone()
    con.close()
    return render_template('23viewbiodata.html',BIODATA=BIODATA)


@app.route('/examresult/<string:id>',methods=['POST','GET'])
def Exam_result(id):
    con=sqlite3.connect('studentdetail.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute('SELECT * FROM students where rollno=? ',(id,))
    MYRESULT=cur.fetchone()
    con.close()
    return render_template('24examresult.html',MYRESULT=MYRESULT)


@app.route('/Student_coachingclass')
def Student_coachingclass():
    ranking()

    con = sqlite3.connect('studentdetail.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT rollno,name,tamil,english,maths,science,social FROM students WHERE result='fail' ")
    Mydata = cur.fetchall()

    Tamil = []
    English = []
    Maths = []
    Science = []
    Social = []
    for i in Mydata:
        if i[2] < 35:
            Tamil.append(i[1])
        if i[3] < 35:
            English.append(i[1])
        if i[4] < 35:
            Maths.append(i[1])
        if i[5] < 35:
            Science.append(i[1])
        if i[6] < 35:
            Social.append(i[1])

    return render_template('25stcoachingclass.html', Tamil=Tamil, English=English, Maths=Maths, Science=Science,
    Social=Social)

@app.route('/stud_forgotpwd',methods=['POST','GET'])
def stud_forgotpwd():
    if request.method=='POST':
        Fname=(request.form.get('name')).title()
        Fdob=request.form.get('dob')

        import sqlite3
        con = sqlite3.connect('studentdetail.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * from students where name=? and dob=?', (Fname,Fdob))
        SDATA = cur.fetchone()

        if SDATA:
            Fname == SDATA['name']
            Fdob == SDATA['dob']
            return render_template('27Stud_conpwd.html',username=Fname)
        else:
            flash('username or DOB mismatch or No USER in this name', 'danger')
            return render_template('26Studentforgotpwd.html')
    return render_template('26Studentforgotpwd.html')

@app.route('/stud_changepwd',methods=['POST','GET'])
def stud_changepwd():
    if request.method=='POST':
        Uname = request.form.get('Uname')
        CHpwd=request.form.get('pwd1')
        Cpwd=request.form.get('pwd2')

        if  (CHpwd==Cpwd):
            con = sqlite3.connect('schooladmins.db')
            cur = con.cursor()
            qry = "UPDATE admins SET pwd=? WHERE name=?"
            tup_word = (CHpwd,Uname)
            cur.execute(qry,tup_word)
            con.commit()
            flash('Pasword changed successfully', 'success')
            return render_template('21studentlogin.html')
        else:
            flash('Password and Confirm password mismatch', 'danger')
            return render_template('27Stud_conpwd.html')
    return render_template('27Stud_conpwd.html')


@app.route('/Aboutus')
def About_us():
    return render_template('31aboutpage.html')


@app.route('/Preprimary')
def Pre_primary():
    return render_template('32pre_primary.html')


@app.route('/primary')
def primary():
    return render_template('33Primary.html')


@app.route('/highschool')
def highschool():
    return render_template('34HighSchool.html')


@app.route('/Skilluplift')
def Skilluplift():
    return render_template('35skillupliftment.html')


@app.route('/Achievemnts')
def Achievement():
    return render_template('36Achievements.html')


@app.route('/gallery')
def gallery():
    return render_template('37gallery.html')


@app.route('/puzzlezone')
def puzzle():
    return render_template('38puzzlezone.html')


@app.route('/onlineform')
def onlineform():
    return render_template('39onlineform.html')

@app.route('/indoorgame')
def indoorgame():
    return render_template('40indoorgames.html')

@app.route('/outdoorgames')
def outergame():
    return render_template('41outergames.html')


@app.route('/culturalmeets')
def culturalmeet():
    return render_template('42culturalmeet.html')






if __name__ == '__main__':
    app.run(debug=True)

