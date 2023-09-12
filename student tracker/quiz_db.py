import sqlite3

from click import option

db=sqlite3.connect("quiz.db")
cursor= db.cursor()

def execute_query(sql_query):
    with sqlite3.connect('quiz.db') as db:
        csr=db.cursor()
        result=csr.execute(sql_query)
        db.commit()
    return result


'''query="select * from questions where class=07"
execute_query(query)'''

'''query="""drop table score"""
execute_query(query)'''


sql_query="""create table score(regno text,score text,academics text,sports text,co_curricular text,programming text,status text,interest text)"""
execute_query(sql_query)



'''query="""DELETE FROM quiz_table WHERE crtop='option 1' or crtop='option 2'"""
execute_query(query)'''


'''sql_query="""create table questions(class text,sub_topic text,question text,op1 text,op2 text,op3 text,crtop text)"""
execute_query(sql_query)'''

'''
sql_query="""create table login(regno text primary key,password text)"""
execute_query(sql_query)
sql_query="""INSERT INTO login VALUES('2207B01','1234')"""
execute_query(sql_query)
sql_query="""INSERT INTO login VALUES('2207B02','1234')"""
execute_query(sql_query)
sql_query="""INSERT INTO login VALUES('2208C01','1234')"""
execute_query(sql_query)
'''

'''
sql_query="""create table quiz_table(question text unique,sub_topic text,op1 text,op2 text,op3 text,crtop text)"""
execute_query(sql_query)
sql_query="""INSERT INTO quiz_table VALUES('this is which question','Academics','1st','2nd','3rd','3')"""
execute_query(sql_query)
'''

'''sql_query="""select * from quiz_table"""
RESULT=execute_query(sql_query)
l=RESULT.fetchall()
questions_list=[]
option1_list=[]
option2_list=[]
option3_list=[]
crt_option=[]

for i in l:   
    questions_list.append(i[0])
    option1_list.append(i[1])
    option2_list.append(i[2])
    option3_list.append(i[3])
    crt_option.append(i[4])

print(questions_list)
print(option1_list)
print(option2_list)
print(option3_list)'''




sql_query="select * from score"
RESULT=execute_query(sql_query)
print(RESULT.fetchall())



