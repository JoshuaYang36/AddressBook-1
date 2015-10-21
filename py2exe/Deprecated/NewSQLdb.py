


"""
Test SQLite3 Database

Author: Joshua Yang
Contributors in alphabetic order by last name:
        Abdulmajeed Kadi, Max Kohl, Garrett Morrison, Hannah Smith
"""


import sqlite3 
import sys
import string

from sqlite3 import OperationalError

"""
Creates new addressbook
"""

table = string.maketrans("","")

#Takes user input and removes all spaces and punctuation.
addressbook = (raw_input("Name your address book: ").replace(" ", "")).translate(table, string.punctuation)
db_name =  addressbook + ".db"

con = sqlite3.connect(db_name)

with con:

    cur = con.cursor()    
    try:
    	cur.execute("CREATE TABLE Contacts(Last Name, First Name, Address, City, State, Zip Code, Phone, Email)")
    except OperationalError:
    	None 

    #Test inputs for DB
    cur.execute("INSERT INTO Contacts VALUES('Yang','Josh', '52642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanfg','Joosh', '526422', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yaneg','Jjosh', '526424', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yangg','Jossh', '526442', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshhh', '522642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshh', '526442', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yaang','Joosh', '5265642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yyang','Jossh', '5264742', NULL, NULL, NULL, NULL, NULL)")

