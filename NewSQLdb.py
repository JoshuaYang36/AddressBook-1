import sqlite3 
import sys

from sqlite3 import OperationalError


# Create New Addressbook DB
db_name = raw_input("Name your address book: ") + ".db"

con = sqlite3.connect(db_name)

with con:

    cur = con.cursor()    
    try:
    	cur.execute("CREATE TABLE Contacts(Last Name, First Name, Address, City, State, Zip Code, Phone, Email)")
    except OperationalError:
    	None 


    cur.execute("INSERT INTO Contacts VALUES('Yang','Josh', '52642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanfg','Joosh', '526422', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yaneg','Jjosh', '526424', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yangg','Jossh', '526442', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshhh', '522642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshh', '526442', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yaang','Joosh', '5265642', NULL, NULL, NULL, NULL, NULL)")
    cur.execute("INSERT INTO Contacts VALUES('Yyang','Jossh', '5264742', NULL, NULL, NULL, NULL, NULL)")

    cur.execute("SELECT * FROM Contacts")
