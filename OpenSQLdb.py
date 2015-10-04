import sqlite3 
import sys
import os

from sqlite3 import OperationalError


# Open existing addressbook DB
db_name = "sqlite3 " + raw_input("Addressbook name: ") + ".db"
print(db_name)


os.system(db_name)



