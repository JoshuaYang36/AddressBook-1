import csv
from contact import Contact

class AddressBook(object):
    MAX_CONTACTS = 100

    def __init__(self, name, contact_list):
        self.name = name;
        self.size = 0;
        self.contact_list = contact_list;


    def write_to_csv(self,output):
        #FIXME: need to have addressbook name as filename
        with open(output, 'wb') as f:
            writer = csv.writer(f)
            #Create header rows for contact
            data = [
                ('First Name', 'Last Name', 'Address', 'City', 'State', 'Zip', 'Phone','Email'),
            ]

            for contact in contact_list:
                writer.writerow(contact.to_csv())
        f.close()

    def get_database(self):
        return self.name + '.db'

    def add_contact(self, contact):
        contact_list.append(contact)
        size += 1

    def find_id(self, id):
        for contact in contact_list:
            if contact
