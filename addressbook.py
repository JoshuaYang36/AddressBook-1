import csv
import sqlite3
from contact import Contact

class AddressBook(object):
    MAX_CONTACTS = 1024
    db_name = 'addressbook.db'

    def __init__(self, name,num_contacts=0):
        self.name = name
        self.num_contacts= 0
        self.has_changed = False

    def add(self, contact):
        self.num_contacts+=1
        self.has_changed = True

        conn = sqlite3.connect('addressbook.db')
        c = conn.cursor()
        c.execute("""
        insert into contacts (lname,fname,address,city,state,zcode,phone,email)
        values (?,?,?,?,?,?,?,?)
        """,(contact.last_name,contact.first_name,contact.address,contact.city,contact.state,contact.zip_code,contact.phone,contact.email,))
        conn.commit()

    def delete(self, contact):
        num_contacts-=1 #TODO: Check that entry is successfully deleted
        has_changed = True

        conn = sqlite3.connect('addressbook.db')
        c = conn.cursor()
        c.execute("""
        delete from contacts (lname,fname,address,city,state,zcode,phone,email)
        values (?,?,?,?,?,?,?,?)
        """,(contact.last_name,contact.first_name,contact.address,contact.city,contact.state,contact.zip_code,contact.phone,contact.email,))
        conn.commit()

    def retrieve(self, lname, fname):
        conn = sqlite3.connect('addressbook.db')
        c = conn.cursor()
        c.execute("""
        select * from contacts where lname like ?
        and fname like ?""",(lname,fname,))

        print c.fetchall()
        result = c.fetchall()
        conn.close()
        return result

    def display(self):
        conn = sqlite3.connect('addressbook.db')
        c = conn.cursor()
        c.execute("""
        select * from contacts
        """)
        for row in c:
            print(row)
        conn.close()
