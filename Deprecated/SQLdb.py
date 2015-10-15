import sqlite3
import sys
import string
import os
from os.path import isfile
from contact import ContactDAO
from test import *
from sqlite3 import OperationalError
table = string.maketrans("","")
class SQLdb:
	"""
	Defines user actions related to the database suchs as New, Open, Close, Save, Save as, Add, Delete,
	Edit, Search
	"""
	def __init__(self):
		"""
		Initiatizes the SQL DB that will hold a table called "Contacts". This table will include a field called "AB", which will
		be used to differentiate between different addressbooks
		"""

		#TODO: use :memory: to create database in RAM until user chooses to save
		#conn = sqlite3.connect('addressbook.db')

		# Prompts user to choose between creating a new addressbook or opening an existing one. Checks to see if user input is correct.
		w = True
		while w:
			action = raw_input("Would you like to create a new addressbook or open an existing one? Choose one (New/Open): ").replace(" ", "").translate(table, string.punctuation).lower()

			# If and elif statement differs only in the prompt it outputs to the user. Both call AccessSQLdb()
			# A new address book is created in the AddressBook table of the database.
			# The table autoincrements the id when a new AddressBook is created
			if  action == "new":
				w = False
				addressbook = (raw_input("Name your address book: ").replace(" ", "")).translate(table, string.punctuation).lower()
				book = create_addressbook(addressbook)
				self.AccessSQLdb(book)

			elif action == "open":
				w = False
				addressbook = raw_input("Addressbook to open: ").replace(" ", "").translate(table, string.punctuation).lower()
				self.AccessSQLdb(addressbook)

			else:
				print("Invalid Input. Please type one -> (New/Open)")


	def AccessSQLdb(self, addressbook):
		"""
		Prompts the user to choose from one of the following Addressbook actions: Add, Delete, Retrieve, Edit
		"""

		#Test inputs for DB

		#cur.execute("INSERT INTO Contacts VALUES('Yang','Josh', '52642', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yanfg','Joosh', '526422', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yaneg','Jjosh', '526424', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yangg','Jossh', '526442', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshhh', '522642', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yanag','Joshh', '526442', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yaang','Joosh', '5265642', NULL, NULL, NULL, NULL, NULL, addressbook)")
		#cur.execute("INSERT INTO Contacts VALUES('Yyang','Jossh', '5264742', NULL, NULL, NULL, NULL, NULL, addressbook)")

		# Checks to see if user input is valid. If so, do selected action
		iterate = True
		while iterate:
			action = raw_input("What would you like to do? Choose one (Add/Delete/Retrieve/Edit/Quit): ").replace(" ", "").translate(table, string.punctuation).lower()

			if action == "add":
				self.add(addressbook)
			elif action == "delete":
				self.delete(addressbook)
			elif action == "retrieve":
				print 'retrieving '+addressbook
				self.retrieve(addressbook)
			elif action == "edit":
				iterate = False
				self.edit(cur, addressbook)
			elif action == "quit":
				iterate = False
			else:
				print("Invalid input. Please type one -> (Add/Delete/Retrieve/Edit)")



	def delete(self, addressbook):
		book_id = AddressBook.get(AddressBook.name == addressbook).id
		contact = retrieve(addressbook)
		contact.delete_instance()

	def add(self, addressbook):
		#
		# Initiates a Null filled contact list and prompts users to fill out the fields, with a requirement of
		# filling out at least one of the First/Last names, plus one other field.
		book_id = AddressBook.get(AddressBook.name == addressbook).id
		contact = [None] * 8
		contact.append(book_id)

		#Prompts user to fill contact list with manual inputs
		print("Fill out the following contact fields. Press Enter to skip. Must fill out at least First/Last Name AND one other field.")

		contact[0] = raw_input("Last Name: ")
		contact[1] = raw_input("First Name: ")
		contact[2] = raw_input("Street Address: ")
		contact[3] = raw_input("City: ")
		contact[4] = raw_input("State: ")
		contact[5] = raw_input("Zip Code: ")
		contact[6] = raw_input("Phone: ")
		contact[7] = raw_input("Email: ")

		#Checks to see if either first or last name has been filled out. Or both.
		iterate = True
		while iterate:
			if contact[0] == "" and contact[1] == "":
				print("Must fill out at least one of the name entries (First/Last)")
				contact[0] = raw_input("Last Name: ")
				contact[1] = raw_input("First Name: ")
			else:
				iterate = False

		#Checks to see if at least one other field is filled in.
		entries = 0
		for item in contact:
			if item != "":
				entries += 1

		#If not one other field is filled, will repeatedly prompt user to do so
		iterate = True
		while iterate:
			if entries >= 3:
				iterate = False
				new_contact = ContactDAO(contact)
				p = create_contact(new_contact,book_id)
				print p
			else:
				print("Must fill out at least one of the following fields.")
				contact[2] = raw_input("Street Address: ")
				contact[3] = raw_input("City: ")
				contact[4] = raw_input("State: ")
				contact[5] = raw_input("Zip Code: ")
				contact[6] = raw_input("Phone: ")
				contact[7] = raw_input("Email: ")

	def retrieve(self, addressbook):
		lname = raw_input("Last Name: ")
		fname = raw_input("First Name: ")
		print 'Getting book with last name: '+lname+'\nfirst name:'+fname+'\nid:'+addressbook
		books = AddressBook.select().where(AddressBook.name == addressbook)
		for b in books:
			results = b.id
			results = search_contacts(lname,fname,results)
		for result in results:
			print "Retrieved "+result.first_name, result.last_name
			return result

if __name__ == "__main__":
	SQLdb()
