import sqlite3 
import sys
import string
import os

from sqlite3 import OperationalError

class SQLdb:
	""" 
	Defines user actions related to the database suchs as New, Open, Close, Save, Save as, Add, Delete, 
	Edit, Search
	"""
	def __init__(self):

		table = string.maketrans("","")
		w = True
		while w: 
			action = raw_input("Would you like to create a new addressbook or open an existing one? Choose one (New/Open): ").replace(" ", "").translate(table, string.punctuation)
			
			if action == "New" or action == "new":
				w = False
				self.NewSQLdb()
			elif action == "Open" or action == "open":
				w = False
				self.OpenSQLdb()
			else:
				pass


	def NewSQLdb(self):
		""" Creats new addressbook """

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

	def OpenSQLdb(self):
		
		""" Open existing addressbook DB """

		table = string.maketrans("","")

		#Takes user input and removes all spaces and punctuation. 
		addressbook = raw_input("Addressbook name: ").replace(" ", "").translate(table, string.punctuation)
		db_name = "sqlite3 "  + addressbook + ".db" 


		os.system(db_name)

	def delete(self):
		pass


if __name__ == "__main__":
	SQLdb()
