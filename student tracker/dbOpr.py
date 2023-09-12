import sqlite3


def insert_user(email, password):
    sql = """
    INSERT INTO Login(email, password) VALUES('%s', '%s')""" % (email, password)
    execute_query1(sql)


def get_password(email):
    sql_query = """
    SELECT password FROM Login WHERE email='%s'""" % email
    password = execute_query1(sql_query).fetchall()
    return password


def insert_stu(name, gen, cls, dob, sec, date, id):
    sql = """
    INSERT INTO Student(name, gender, cls, dob, sec, date, id) VALUES('%s', '%s', '%s', '%s','%s','%s', '%s')""" % (name, gen, cls, dob, sec, date, id)
    execute_query2(sql)


def get_dob(roll):
    sql_query1 = """
        SELECT dob FROM Student WHERE id='%s'""" % roll
    password = execute_query2(sql_query1).fetchall()
    sql_query2 = """
            SELECT name FROM Student WHERE id='%s'""" % roll
    name = execute_query2(sql_query2).fetchall()
    return password, name


def insert_comp(title, file, number, decrp):
    sql = """
        INSERT INTO Comp(Title, Id, Decrp, file) VALUES('%s', '%s', '%s', '%s')"""% (
        title, number, decrp, file)
    execute_query3(sql)


def send_comp():
    sql_query1 = """
            SELECT Title FROM Comp"""
    title = execute_query3(sql_query1).fetchall()
    sql_query2 = """
                SELECT id FROM Comp"""
    id = execute_query3(sql_query2).fetchall()
    sql_query3 = """
                SELECT Decrp FROM Comp"""
    Decrp = execute_query3(sql_query3).fetchall()
    sql_query4 = """
                    SELECT file FROM Comp"""
    file = execute_query3(sql_query4).fetchall()

    return title, id, Decrp, file


def execute_query1(sql_query):
    with sqlite3.connect("login.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def execute_query2(sql_query):
    with sqlite3.connect("Student.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


def execute_query3(sql_query):
    with sqlite3.connect("Comp.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql_query)
        conn.commit()
    return result


if __name__ == '__main__':
    """get_password("karthik@gmail.com")
    insert_user("aamil@kcgpc.com", "123")"""