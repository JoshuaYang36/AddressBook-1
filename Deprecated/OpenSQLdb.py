import sqlite3 
import sys
import os
import string

from sqlite3 import OperationalError


"""
Open existing addressbook DB
"""

table = string.maketrans("","")

#Takes user input and removes all spaces and punctuation. 
addressbook = (raw_input("Addressbook name: ").replace(" ", "")).translate(table, string.punctuation)
db_name = "sqlite3 "  + addressbook + ".db" 


os.system(db_name)



