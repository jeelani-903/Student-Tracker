'''import sqlite3

db=sqlite3.connect('quiz.db')
cursor=db.cursor()

query="select crtop from quiz_table where sno=1"
cursor.execute(query)
result = cursor.fetchall()
crt_op=int(result[0][0])
sel_op=int(input("enter the option :"))

if sel_op==crt_op:
    print("Successful....")
else: 
    print("Fail!!!")

'''
a,b,c=2,0,7
l=[]
if a==0:
    l.append(0)
else:
    l.append(2/a)
if b==0:
    l.append(0)
else:
    l.append(2/b)
if c==0:
    l.append(0)
else:
    l.append(5/c)

print(l)

