from flask import Flask, render_template, session, url_for,request, redirect, flash, send_file
from dbOpr import send_comp, insert_user, get_password, insert_stu, get_dob, insert_comp
import os
from werkzeug.utils import secure_filename
import random
import datetime
import sqlite3


def execute_query(sql_query):
    with sqlite3.connect('quiz.db') as db:
        csr = db.cursor()
        result = csr.execute(sql_query)
        db.commit()
    return result


app = Flask(__name__)
app.secret_key = "123@abc"
AdminLog = False
sel_option = []
score = 0
l = 0
upload_folder = "uploads"
app.config['UPLOAD_FOLDER'] = upload_folder


def set_session(email, name):
    session.permanent = True
    session["logged_in"] = True
    session["email"] = email
    session["name"] = name


def reset_session():
    if "logged_in" in session:
        del session["logged_in"]
        del session["email"]
        del session["name"]


def verify_login(email, password, type):
    global AdminLog
    if type == "Admin":
        stored_password = get_password(email)
        if len(stored_password):
            if password == stored_password[0][0]:
                AdminLog = True
            else:
                flash("Wrong Password")
        else:
            flash("No Email Found")

    elif type == "Student":
        stored_password, name = get_dob(email)
        if len(stored_password):
            if password == stored_password[0][0]:
                set_session(email, name[0][0])
            else:
                flash("Wrong Password")
        else:
            flash("No Email Found")


@app.route("/")
def home():
    return render_template("home1.html")


@app.route("/adminpage", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    else:
        name = request.form['email']
        pwd = request.form['pwd']
        verify_login(name, pwd, "Admin")
        return redirect("adminportal")


@app.route("/adminportal", methods=["GET", "POST"])
def adminportal():
    global AdminLog
    if AdminLog:
        return render_template("admin portal.html")
    else:
        return redirect("adminpage")


@app.route("/adminstu", methods=["GET", "POST"])
def adminstu():
    if request.method == "GET":
        print("a")
        return render_template("student register.html")
    else:
        name = request.form['name']
        dob = request.form['dob']
        cls = request.form['class']
        sec = request.form['sec']
        date = request.form["date"]
        gen = request.form["gen"]
        roll = request.form["roll"]
        insert_stu(name, gen, cls, dob, sec, date, roll)
        print(name, gen, cls, dob, sec, date, roll)

        return render_template("student register.html")


@app.route("/competition page", methods=["GET", "POST"])
def comppage():
    if request.method == "GET":
        return render_template('competition page.html')
    else:
        title = request.form['title']
        des = request.form['description']
        try:
            f = request.files['file']
            name = f.filename
            val = name.split(".")
            a = str(random.randrange(1000, 5000))
            name = a + "_" + val[0] + "." + val[1]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(name)))
        except IndexError:
            name = "None"

        insert_comp(title, name, a, des)
        return render_template('competition page.html')


@app.route("/stucomp", methods=["POST", "GET"])
def stu_comp():
    if request.method == "GET":
        title, id, decp, file = send_comp()
        length = len(id)
        return render_template('StuComp.html', title=title, no=id, decp=decp, file=file, length=length)
    else:
        text = request.form["id"]
        return send_file("uploads/" + text, as_attachment=True)


@app.route("/staff", methods=["POST", "GET"])
def staff():
    if request.method == "GET":
        print("c")
        return render_template("login.html", utc_dt=datetime.datetime.utcnow())
    else:
        print("b")

        global regno
        regno = request.form['regno']
        password = request.form['psw']
        print(regno)
        query = "select * from login where regno='" + regno + "' and password = '" + password + "'"
        l = execute_query(query)
        l = l.fetchall()
        if len(l) == 0:
            print("sorry,Incorrect details")
        else:
            print("a")
            return render_template("gen details.html")

        return render_template("login.html", utc_dt=datetime.datetime.utcnow())


def get_table_details(options, query='', table=""):
    if table == 'questions':
        sql_query = query
    elif table == 'score':
        sql_query = query
    else:
        sql_query = "select * from " + table
    RESULT = execute_query(sql_query)
    l = RESULT.fetchall()
    if table == 'score':
        register_number = []
        final_score = []
        academic_score = []
        sports_score = []
        co_curricular_score = []
        programming_score = []
        status = []
        interest = []

    else:
        class_list = []
        questions_list = []
        sub_topic_list = []
        option1_list = []
        option2_list = []
        option3_list = []
        crt_option = []
    if table == 'questions':
        for i in l:
            class_list.append(i[0])
            questions_list.append(i[1])
            sub_topic_list.append(i[2])
            option1_list.append(i[3])
            option2_list.append(i[4])
            option3_list.append(i[5])
            crt_option.append(i[6])
    if table == 'score':
        for i in l:
            register_number.append(i[0])
            final_score.append(i[1])
            academic_score.append(i[2])
            sports_score.append(i[3])
            co_curricular_score.append(i[4])
            programming_score.append(i[5])
            status.append(i[6])
            interest.append(i[7])
    else:

        for i in l:
            questions_list.append(i[0])
            sub_topic_list.append(i[1])
            option1_list.append(i[2])
            option2_list.append(i[3])
            option3_list.append(i[4])
            crt_option.append(i[5])
    length = len(l)
    if options == 'get_length':
        return length
    if options == 'get_questions':
        return questions_list
    elif options == 'get_details':
        if table == 'score':
            return register_number, final_score, academic_score, sports_score, co_curricular_score, programming_score, status, interest
        else:
            return questions_list, sub_topic_list, option1_list, option2_list, option3_list, crt_option, length


@app.route('/student register')
def student_register():
    return render_template("student register.html")


@app.route("/teacher register")
def teacher_register():
    return render_template('teacher register.html')



@app.route("/general")
def gen_details():
    return render_template("gen details.html")


@app.route("/student")
def student():
    cls = regno[2:4]
    query = "select * from questions where class='" + cls + "'"
    l = execute_query(query)
    l = l.fetchall()
    return render_template("student.html", regno=regno, questions=len(l))


@app.route("/start")
def start():
    query = 'select regno from score'
    l = execute_query(query)
    l = l.fetchall()

    cls = regno[2:4]
    query = "select * from questions where class='" + cls + "'"
    result = execute_query(query)
    result = result.fetchall()

    if len(result) == 0:
        return render_template("student.html", regno=regno, questions=0)
    for i in range(len(l)):
        if regno == l[i][0]:
            return render_template("student.html", regno=regno, questions=0)

    return render_template("start.html")


@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


@app.route("/result")
def result():
    query = "select * from score where regno='" + regno + "'"
    reg, score, ac, sc, cc, pc, status, interest = get_table_details('get_details', query, 'score')
    return render_template("result.html", score=score, regno=reg, academic_score=ac, sport_score=sc,
                           co_curricular_score=cc, programming_score=pc, status=status)


@app.route("/statistics")
def statistics():
    query = "select interest from score"
    l = execute_query(query)
    l = l.fetchall()
    ac, sp, co, pr, ot = 0, 0, 0, 0, 0
    for i in l:
        print(i, ":")
        if i[0] == 'Academic ':
            ac += 1
        elif i[0] == 'Sports ':
            sp += 1
        elif i[0] == 'Co_Curricular ':
            co += 1
        elif i[0] == 'Programming ':
            pr += 1
        else:
            ot += 1

    return render_template("statistics.html", academic=ac, sport=sp, co_curricular=co, programming=pr, other=ot)


@app.route("/question", methods=["POST", "GET"])
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        question = request.form['Add question']
        sub_topic = request.form['sub topic']
        op1 = request.form['Type option 1']
        op2 = request.form['Type option 2']
        op3 = request.form['Type option 3']
        crt_op = request.form['Answer']
        print(sub_topic)
        sql_query = "insert into quiz_table values('" + question + "','" + sub_topic + "','" + op1 + "','" + op2 + "','" + op3 + "','" + crt_op + "')"
        execute_query(sql_query)
        return render_template("question.html")


@app.route("/comp", methods=["POST", "GET"])
def comp():
    if request.method == "GET":
        return render_template("Comp.html")


@app.route("/report")
def report():
    query = "select * from score"
    reg, sor, aca, sport, co_curr, prog, status, interest = get_table_details('get_details', query, 'score')
    length = len(reg)
    print(reg)
    print(sor)
    return render_template("report.html", register_number=reg,
                           score=sor,
                           academic=aca,
                           sport=sport,
                           co_curricular=co_curr,
                           programming=prog,
                           status=status,
                           length=length,
                           interest=interest
                           )


@app.route("/view", methods=['GET', 'POST'])
def view():
    if request.method == 'GET':
        global message
        questions = get_table_details("get_questions", 'noquery', "quiz_table")[::-1]
        length = len(questions)
        return render_template("view question.html", length=length, questions=questions)
    else:
        row = request.form['index']
        standard = request.form['class']
        questions = get_table_details("get_questions", 'noquery', "quiz_table")[::-1]
        length = len(questions)

        '''query="DELETE FROM quiz_table WHERE question='"+questions[int(row)]+"'"
        execute_query(query)'''

        q, st, op1, op2, op3, crtop, l = get_table_details("get_details", 'noquery', "quiz_table")
        for i in range(l):
            sql_query = "insert into questions values('" + standard + "','" + q[i] + "','" + st[i] + "','" + op1[
                i] + "','" + op2[i] + "','" + op3[i] + "','" + crtop[i] + "')"
            execute_query(sql_query)
        sql_query = "delete from quiz_table"
        execute_query(sql_query)

        message = True
        return render_template("view question.html", length=length, questions=questions)


@app.route("/mcq", methods=["POST", "GET"])
def mcq():
    print("g")
    global sel_option, score

    if request.method == "GET":
        print("a_mcq")
        current_class = regno[2:4]
        query = "select * from questions where class='" + current_class + "'"
        q, st, op1, op2, op3, crtop, l = get_table_details('get_details', query, table='questions')

        return render_template("mcq.html",
                               questions_list=q,
                               sub_topic_list=st,
                               option1_list=op1,
                               option2_list=op2,
                               option3_list=op3,
                               length=l
                               )
    else:
        print("b_mcq")
        score = 0
        current_class = regno[2:4]
        query = "select * from questions where class='" + current_class + "'"
        q, st, op1, op2, op3, crtop, l = get_table_details('get_details', query, table='questions')
        for i in range(l):
            selected_option = request.form['' + str(i) + '']
            sel_option.append(selected_option)
            if selected_option == crtop[i]:
                score += 1

        print(sel_option)
        print(crtop)
        print("YOUR SCORE :", score, "/", len(q))
        out_off = get_table_details("get_length", 'noquery', 'quiz_table')
        academics_score, sports_score, co_curricular_score, programming_score = 0, 0, 0, 0
        academics_question, sports_question, co_curricular_question, programming_question = 0, 0, 0, 0

        for i in range(len(sel_option)):
            if st[i] == 'Academics':
                academics_question += 1
                if sel_option[i] == crtop[i]:
                    academics_score += 1
            elif st[i] == 'Sports':
                sports_question += 1
                if sel_option[i] == crtop[i]:
                    sports_score += 1
            elif st[i] == 'Co-Curricular':
                co_curricular_question += 1
                if sel_option[i] == crtop[i]:
                    co_curricular_score += 1
            elif st[i] == 'Programming':
                programming_question += 1
                if sel_option[i] == crtop[i]:
                    programming_score += 1
        if score >= 0.35 * len(sel_option):
            status = 'PASS'
        else:
            status = 'FAIL'

        l = []
        if academics_question == 0:
            l.append(0)
        else:
            l.append(academics_score / academics_question)
        if sports_question == 0:
            l.append(0)
        else:
            l.append(sports_score / sports_question)

        if co_curricular_question == 0:
            l.append(0)
        else:
            l.append(co_curricular_score / co_curricular_question)
        if programming_question == 0:
            l.append(0)
        else:
            l.append(programming_score / programming_question)

        maximum = max(l)
        interest_index = []
        interest = ''
        for i in range(len(l)):
            if l[i] == maximum:
                interest_index.append(i)
        for j in interest_index:
            if len(interest_index) > 0 and len(interest_index) < 4:
                if j == 0:
                    interest += 'Academic '
                if j == 1:
                    interest += 'Sports '
                if j == 2:
                    interest += 'Co_Curricular '
                if j == 3:
                    interest += 'Programming '

            elif len(interest_index) == 4:
                interest = "All Rounder"
                break

        out_off = academics_question + sports_question + co_curricular_question + programming_question
        query = "insert into score values('" + str(regno) + "','" + str(score) + "/" + str(out_off) + "','" + str(
            academics_score) + "/" + str(academics_question) + "','" + str(sports_score) + "/" + str(
            sports_question) + "','" + str(co_curricular_score) + "/" + str(co_curricular_question) + "','" + str(
            programming_score) + "/" + str(programming_question) + "','" + status + "','" + interest + "')"
        execute_query(query)
        sel_option = []
        query = "select * from score where regno='" + regno + "'"
        reg, score, ac, sc, cc, pc, status, interest = get_table_details('get_details', query, 'score')
        return render_template("result.html", score=score, regno=reg, academic_score=ac, sport_score=sc,
                               co_curricular_score=cc, programming_score=pc, status=status)


if __name__ == "__main__":
    app.run(debug=True)

