import csv
import OpenSQLdb
from NewSQLdb import Database
from contact import Contact

class AddressBook(object):
    MAX_CONTACTS = 1024

    def __init__(self, database='', name='', filepath='', num_contacts=0,has_changed=False):
        self.database = database
        self.name = name
        self.filepath = filepath
        self.num_contacts = 0
        self.has_changed = False
        self.cur;

    def init_db(self):
        table = string.maketrans("","")
        if database is '' and name is '' and filepath is '':
            self.name = (raw_input("Name your address book: ").replace(" ", "")).translate(table, string.punctuation)
            self.database = name + ".db"
            con = sqlite3.connect(database)

            with con:
                self.cur = con.cursor()
                try:
                	cur.execute("CREATE TABLE Contacts(Last Name, First Name, Address, City, State, Zip Code, Phone, Email)")
                except OperationalError:
                	None
        else:
            database = "sqlite3 "  + name + ".db"
            os.system(database)

    def add(self, contact):
        num_contacts+=1
        has_changed = True
        cur.execute("INSERT INTO " + name + contact.to_dao())

    def delete(self, contact):
        num_contacts-=1 #TODO: Check that entry is successfully deleted
        has_changed = True
        cur.execute("DELETE FROM" + name + contact.to_dao())
