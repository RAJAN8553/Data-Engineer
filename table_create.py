import pymysql
from datetime import datetime

# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="hospital")
cursor = connection.cursor()
if connection:
    print("DATABASE CONNECT SUCCESSFULLY ")

# open file in read mode
f = open("data_20210819.txt", 'r')
row = f.readlines()


# create function for insert D type of Data
def insert_record(split_data):
    s = "INSERT INTO `" + split_data[9] + "`(`Customer Name`, `Customer ID`, " \
                                    "`Customer Open Date`, `Last Consulted Date`," \
                                    " `Vaccination Type`, `Doctor Consulted`," \
                                    " `State`, `Country`," \
                                    " `Date of Birth`, `Active Customer`)" \
                                    " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    v = split_data[2::1]
    cursor.execute(s, v)
    print("Record Your Data Successfully. \n Name Of customer ", split_data[2])


# main program

for i in range(0, len(row)):
    split = row[i].split("|")  # Split file data to list
    flag = 0  # This variable for check country table

    if split[1].lower() == 'h':  # this condition check H type of data and insert record
        # Header record will store in test table
        sql = "INSERT INTO `test` (`Customer Name`, `Customer Open Date`, `Customer ID`) " \
                                  "VALUES (%s,%s,%s);"  # sql query
        val = split[2:(len(split[i]) - 1)]  # use indexing for store data
        # executing the query
        cursor.execute(sql, val)

    elif split[1].lower() == 'd':  # condition for store Detail Data
        sql = "SHOW TABLES"  # sql query
        cursor.execute(sql)  # execute query

        for tb in cursor:  # store all table of hospital database
            if split[9].lower() in tb:  # checks if same country is in table
                flag = 1
        split[10] = datetime.strptime(split[10], '%m%d%Y')  # format our given date of birth

        if flag:
            insert_record(split)  # call the function

        else:
            # else it create new country table and store data into new country table
            sql = "CREATE TABLE `hospital`.`" + split[9] + "`( `Customer Name` VARCHAR(255) NOT NULL ," \
                                                          " `Customer ID` VARCHAR(18) NOT NULL , " \
                                                          "`Customer Open Date` DATE NOT NULL , " \
                                                          "`Last Consulted Date` DATE NULL ," \
                                                          " `Vaccination Type` CHAR(5) NULL , " \
                                                          "`Doctor Consulted` CHAR(255) NULL , `State` CHAR(5) NULL ," \
                                                          "`Country` CHAR(5) NULL , `Post Code` INT(5) NULL , " \
                                                          "`Date of Birth` DATE NULL , " \
                                                          "`Active Customer` CHAR(1) NULL , " \
                                                          "PRIMARY KEY (`Customer Name`)) ;"
            cursor.execute(sql)
            insert_record(split)  # call the function

    elif split[1].lower() == 't':  # store T type of data
        sql = "INSERT INTO `test` (`Customer ID`)" \
              " VALUES (%s);"

        val = split[2::2]
        cursor.execute(sql, val)

    else:
        print("Please give valid mode of record ")
connection.commit()  # committing the current transaction
connection.close()  # close the connection
