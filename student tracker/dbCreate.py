import sqlite3

sql1 = """
    CREATE TABLE IF NOT EXISTS Login(
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
"""

sql2 = """
    CREATE TABLE IF NOT EXISTS Student(
        name TEXT,
        dob TEXT,
        id TEXT PRIMARY KEY,
        class INTEGER,
        sec TEXT,
        date TEXT,
        gender INTEGER,
    )"""


sql3 = """
    CREATE TABLE IF NOT EXISTS Comp(
        Title TEXT,
        id TEXT PRIMARY KEY,
        Decrp TEXT,
        file TEXT
    )"""


def execute_query(sql):
    with sqlite3.connect("Comp.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
    return result


if __name__ == '__main__':
    execute_query(sql3)