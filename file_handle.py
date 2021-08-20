import pymysql
import datetime

#database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="hospital" )
cursor = connection.cursor()
if connection :
    print("DATABASE CONNECT SUCESSFULLY")

f = open("file.txt",'r')
print(f)
# queries for inserting values

sql = "INSERT INTO `test` (`Customer Name`, `Customer ID`, `Customer Open Date`) VALUES ('Viresh','12' , '2020-08-16');"
#executing the quires
cursor.execute(sql)


# Print database table values

sql = "select * from test;"
p = cursor.execute(sql)

rows = cursor.fetchall()
for row in rows :
    print(row)

#commiting the connection then closing it.
connection.commit()
connection.close()
