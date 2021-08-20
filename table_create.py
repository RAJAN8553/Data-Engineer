import pymysql
from datetime import datetime

# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="hospital")
cursor = connection.cursor()
if connection:
    print("DATABASE CONNECT SUCCESSFULLY ")

# open file
f = open("data_20210819.txt", 'r')
row = f.readlines()


def insert_record(split_data):
    s = "INSERT INTO `" + country + "`(`Customer Name`, `Customer ID`, " \
                                      "`Customer Open Date`, `Last Consulted Date`," \
                                      " `Vaccination Type`, `Doctor Consulted`," \
                                      " `State`, `Country`," \
                                      " `Date of Birth`, `Active Customer`)" \
                                      " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    v = split_data[2::1]
    print("value ", v)
    cursor.execute(s, v)
    print("Record Data Successfully ")


for i in range(0, len(row)):
    split = row[i].split("|")
    flag = 0
    if split[1].lower() == 'h':
        sql = "INSERT INTO `test` (`Customer Name`, `Customer Open Date`, `Customer ID`) VALUES (%s,%s,%s);"
        val = split[2:(len(split[i]) - 1)]
        print("value ", val)
        # executing the quires
        cursor.execute(sql, val)

    elif split[1].lower() == 'd':
        country = split[9]
        sql = "SHOW TABLES"
        cursor.execute(sql)
        for tb in cursor:
            print(tb)
            print(country)
            if country.lower() in tb:
                flag = 1

        split[10] = datetime.strptime(split[10], '%m%d%Y')
        if flag:
            insert_record(split)

        else:

            sql = "CREATE TABLE `hospital`.`" + country + "`( `Customer Name` VARCHAR(255) NOT NULL ," \
                            " `Customer ID` VARCHAR(18) NOT NULL , `Customer Open Date` DATE NOT NULL , " \
                            "`Last Consulted Date` DATE NULL , `Vaccination Type` CHAR(5) NULL , " \
                            "`Doctor Consulted` CHAR(255) NULL , `State` CHAR(5) NULL , " \
                            "`Country` CHAR(5) NULL , `Post Code` INT(5) NULL , " \
                            "`Date of Birth` DATE NULL , `Active Customer` CHAR(1) NULL , " \
                            "PRIMARY KEY (`Customer Name`)) ;"
            cursor.execute(sql)
            insert_record(split)

    elif split[1].lower() == 't':
        sql = "INSERT INTO `test` (`Customer ID`)" \
              " VALUES (%s);"
        print("Split", split)

        val = split[2::2]
        print("value ", val)
        cursor.execute(sql, val)

connection.commit()
connection.close()
