


"""
Test address book application

Author: Hannah Smith
Contributors in alphabetic order by last name:
        Abdulmajeed Kadi, Max Kohl, Garrett Morrison, Joshua Yang
"""


from peewee import *
from fileUtils import *
from playhouse.csv_loader import dump_csv
from contact import ContactDAO
import sys


# Instantiate SqliteDatabase object that models will use to persist data.
DATABASE = 'application.db'
db = SqliteDatabase(DATABASE)  # db manages the connection and executes queries


class BaseModel(Model):
    """ Standard base model class that specifies which database to use.
    Subclasses automatically use correct storage """
    class Meta:
        database = db


class AddressBook(BaseModel):
    """ The AddressBook object model representing a single collection
    of contacts
    :param name: A string, the name of the book given by user.
    :param id: An int, the auto-incrementing integer primary key field.
    """
    name = CharField(unique=True)

    class Meta:
        order_by = ('id',)


class Contact(BaseModel):
    """ A representation of an addressbook contact in the database. By
    default, Contacts are ordered by last name.
    :param ab: An int, the foreign key used to map a Contact to the
    AddressBook it belongs to.
    """
    first_name = CharField()
    last_name = CharField()
    address = CharField()
    city = CharField()
    state = CharField()
    zip_code = CharField(null=False)
    phone = CharField()
    email = CharField()
    ab = ForeignKeyField(AddressBook)

    class Meta:
        order_by = ('last_name',)


def create_tables():
    """ Creates the tables in the database containing the AddressBook
    and Contact models. Only needs to be performed once at the initialization
    of the app. """
    db.connect()
    # db.drop_tables([AddressBook, Contact])
    db.create_tables([AddressBook, Contact], True)

# first_name =
# last_name =
# address =
# city =
# state =
# zip_code =
# phone =
# email =


def create_addressbook(name):
    """ Creates a new AddressBook record. If an AddressBook already exists
    with the name provided, the database will raise an IntegrityError.
    :param name: string, the name of the Addressbook
    """
    q = AddressBook.select().where(AddressBook.name == name)
    if q.exists():
        addressbook = AddressBook.get(AddressBook.name == name)
    else:
        with db.transaction():
            addressbook = AddressBook.create(
                name=name,
            )

    return addressbook


def create_contact(contact, ab):
    """ Creates a new Contact and prints out the number of rows modified.
    :param contact: object, the ContactDAO to be created.
    :param ab: int, the id of the AddressBook the Contact will be added to.
    """
    try:
        with db.transaction():
            person = Contact.create(
                first_name=contact.first_name,
                last_name=contact.last_name,
                address=contact.address,
                city=contact.city,
                state=contact.state,
                zip_code=contact.zip_code,
                phone=contact.phone,
                email=contact.email,
                ab=ab
            )
        # print person.save() # Prints 1 if successful
        #print_info(person)
        return person.id  # Return id of Contact
    except IntegrityError:
        print 'Contact already exists'


def search_contacts(name, ab):
    """ Returns a list of Contacts in an AddressBook matching search input.
    :param last: string, last name of Contact to search for.
    :param first: string, first name of Contact to search for.
    :param ab: int, id of AddressBook being searched.
    """
    result = None
    try:
        result = Contact.get(
            (Contact.last_name == name) |
            (Contact.first_name == name) &
            (Contact.ab == ab))
        print "Found: "
        print_info(result)

    except DoesNotExist:
        print "No contact found"
    return result


# def string_search(info, ab):
#     results = Contact.select().where(
#         (Contact.ab == ab) & (
#             (Contact.first_name.contains(info)) |
#             (Contact.last_name.contains(info)) |
#             (Contact.address.contains(info)) |
#             (Contact.city.contains(info)) |
#             (Contact.state.contains(info)) |
#             (Contact.zip_code.contains(info)) |
#             (Contact.phone.contains(info)) |
#             (Contact.email.comtains(info))
#         ))
#     for result in results:
#         print_info(result)


def delete_contact(contact):
    contact.delete_instance()


def print_info(contact):
    """ Prints a Contact.
    :param contact: Contact, the contact to print.
    """
    print contact.first_name + " " + contact.last_name + " " + contact.address + " " + contact.city + " " + contact.state + " " + contact.zip_code + " " + contact.phone + " " + contact.email


def populate_addressbook(csv_file, id):
    """ Adds Contacts from a csv file to an AddressBook. Calls method
    import_csv from fileUtils.py to read csv into dictionary.
    :param id: int, the id of the AddressBook to add Contacts to.
    :param csv_file: string, the file name of the csv to import.
    """
    contact_data = import_csv(csv_file, id)
    with db.atomic():
        for data_dict in contact_data:
            Contact.create(**data_dict)
    print "Created contacts in book with id " + str(id)


def export_addressbook(out_file, id):
    """ Exports Contacts to a file in csv format.
    :param id: int, the id of the AddressBook to export.
    :param out_file: string, the file to export data to.
    """

    with open(out_file, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        query = Contact.select().where(Contact.ab == id).order_by(Contact.last_name)
        dump_csv(query, f, csv_writer=writer)


def contact_menu(contact):
    keep_running = True

    while keep_running:
        print("CONTACT: " + contact.first_name + " " + contact.last_name)
        print_info(contact)
        ab = contact.ab
        prompt = "Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n"
        #print(           
        #	"Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n")
        contact_action = get_user_input_as_int(prompt)
        #contact_action = int(raw_input(
        #    "Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n"))

        if contact_action == 1:
            pass
        elif contact_action == 2:
            contact.delete_instance()
            book_menu(ab)
            keep_running = False
        elif contact_action == 3:
            book_menu(ab)
            keep_running = False
        else:
            print("Invalid input")


def book_menu(addressbook):
    print("ADDRESSBOOK: " + addressbook.name)
    keep_running = True

    while keep_running:
    	prompt = "Enter option number:\n\t[1] Add contact\n\t[2] Retrieve contact\n\t[3] Import address book\n\t[4] Export address book\n\t[5] Main Menu\n"
        book_action = get_user_input_as_int(prompt)
        #book_action = int(raw_input(
        #    "Enter option number:\n\t[1] Add contact\n\t[2] Retrieve contact\n\t[3] Import address book\n\t[4] Export address book\n\t[5] Main Menu\n"))

        if book_action == 1:
            contact = [None] * 8
            print("Fill out the following contact fields. Press Enter to skip. Must fill out at least First/Last Name AND one other field.")

            prompt = "Last Name: "
            contact[0] = get_user_input_as_string(prompt)
            prompt = "First Name: "
            contact[1] = get_user_input_as_string(prompt)
            prompt = "Street Address: "
            contact[2] = get_user_input_as_string(prompt)
            prompt = "City: "
            contact[3] = get_user_input_as_string(prompt)
            prompt = "State: "
            contact[4] = get_user_input_as_string(prompt)
            prompt = "Zip Code: "
            contact[5] = get_user_input_as_string(prompt)
            prompt = "Phone: "
            contact[6] = get_user_input_as_string(prompt)
            prompt = "Email: "
            contact[7] = get_user_input_as_string(prompt)
            #contact[0] = raw_input("Last Name: ")
            #contact[1] = raw_input("First Name: ")
            #contact[2] = raw_input("Street Address: ")
            #contact[3] = raw_input("City: ")
            #contact[4] = raw_input("State: ")
            #contact[5] = raw_input("Zip Code: ")
            #contact[6] = raw_input("Phone: ")
            #contact[7] = raw_input("Email: ")

            new_contact = ContactDAO(contact)
            create_contact(new_contact, addressbook.id)
            print("Contact created!")

        elif book_action == 2:
            prompt = "Enter first or last name of contact: "
            SEARCH_NAME = get_user_input_as_string(prompt)
            FOUND_CONTACT = search_contacts(SEARCH_NAME, addressbook.id)

            if FOUND_CONTACT is not None:
                keep_running = False
                contact_menu(FOUND_CONTACT)

        elif book_action == 3:
            prompt = "Enter file name to import: "
            IN_FILE = get_user_input_as_string(prompt)
            #IN_FILE = raw_input("Enter file name to import: ")
            populate_addressbook(IN_FILE, addressbook.id)

        elif book_action == 4:
            prompt = "Enter file to export to: "
            OUT_FILE = get_user_input_as_string(prompt)
            #OUT_FILE = raw_input("Enter file to export to: ")
            export_addressbook(OUT_FILE, addressbook.id)

        elif book_action == 5:
            keep_running = False

        else:
            print("Invalid input")


def get_user_input_as_int(prompt):
	"""
	Fix for bug #1, this flushes stdout before processing input.
	"""
	valid_input = False
	while not valid_input:
		"""
		The next three lines of uncommented code are derived from Jonathan Gardner's code example: 
		https://mail.python.org/pipermail/python-bugs-list/2002-March/010726.html
		"""
		print(prompt)
		sys.stdout.flush()
		user_input = int(sys.stdin.readline())
		if type(user_input) == None:
			print("Invalid input, please enter an integer.")
		elif type(user_input) == int:
			valid_input = True
	return user_input


def get_user_input_as_string(prompt):
	"""
	Fix for bug #1, this flushes stdout before processing input.
	"""
	valid_input = False
	while not valid_input:
		"""
		The next three lines of uncommented code are derived from Jonathan Gardner's code example: 
		https://mail.python.org/pipermail/python-bugs-list/2002-March/010726.html
		"""
		print(prompt)
		sys.stdout.flush()
		user_input = sys.stdin.readline()
		if type(user_input) == None:
			print("Invalid input, please enter an integer.")
		elif type(user_input) == str:
			valid_input = True
	return user_input





def main():
    # BOOK1 = 'Book01'
    # BOOK2 = 'Book02'
    # DATA_FILE = 'dataOct-13-2015.csv'
    # MOCK_DATA = [{ "first_name": "Dorothy", "last_name": "Bennett", "address": "620 Everett Crossing", "city": "Staten Island", "state": "NY", "zip_code": "62756-543", "phone": "1-(914)285-4062", "email": "dbennett0@zdnet.com" }, { "first_name": "Alice", "last_name": "Dunn", "address": "99 Saint Paul Center", "city": "Portland", "state": "OR", "zip_code": "24598-0121", "phone": "1-(971)898-2830", "email": "adunn1@webs.com" }, { "first_name": "Willie", "last_name": "Wilson", "address": "8 Walton Center", "city": "Long Beach", "state": "CA", "zip_code": "51655-111", "phone": "1-(562)553-1798", "email": "wwilson2@fotki.com" }, { "first_name": "Jason", "last_name": "Olson", "address": "300 Eagan Avenue", "city": "Albany", "state": "NY", "zip_code": "55319-110", "phone": "1-(518)773-8518", "email": "jolson3@csmonitor.com" }, { "first_name": "Kevin", "last_name": "Moore", "address": "57553 Laurel Plaza", "city": "El Paso", "state": "TX", "zip_code": "54868-5021", "phone": "1-(915)623-2962", "email": "kmoore4@loc.gov" }]

    create_tables()

    keep_running = True

    while keep_running:
        print("ADDRESSBOOK APPLICATION\n")
        prompt = "Enter option number:\n\t[1] Create Address Book\n\t[2] Open Address Book\n\t[3] Exit\n"
        home_action = get_user_input_as_int(prompt)
        #home_action = int(raw_input(
        #    "Enter option number:\n\t[1] Create Address Book\n\t[2] Open Address Book\n\t[3] Exit\n"))

        if home_action == 1 or home_action == 2:
        	prompt = "Enter name of Address Book: "
        	BOOK_NAME = get_user_input_as_string(prompt)
        	addressbook = create_addressbook(BOOK_NAME)
        	book_menu(addressbook)
        elif home_action == 3:
            keep_running = False
        else:
            print("Invalid input")

        # elif action == "delete":
        #     self.delete(addressbook)
        # elif action == "retrieve":
        #     print 'retrieving '+addressbook
        #     self.retrieve(addressbook)
        # elif action == "edit":
        #     iterate = False
        #     self.edit(cur, addressbook)
        # elif action == "quit":
        #     iterate = False
        # else:
        #     print("Invalid input. Please type one -> (Add/Delete/Retrieve/Edit)")

    # Fill addressbook with data in DATA_FILE
    # print "Populating addressbook..."
    # populate_addressbook(addressbook.id, DATA_FILE)
    #
    # num_contacts = Contact.select().where(Contact.ab == addressbook.id).count()
    # print addressbook.name+" now has "+str(num_contacts)+" contacts!"
    #
    # person1 = ContactDAO(['Smith','Hannah','992 E 18th','eugene','oregon','97403','5339369958','hus@uoregon.edu'])
    # print "Inserting "+person1.first_name+" "+person1.last_name+" into "+addressbook.name
    # person1_id = create_contact(person1, addressbook.id)
    #
    # person2 = ContactDAO(['Doe','Van','2954 NE 30th','Portland','OR','97212','5032818856','vps@juno.com'])
    # create_contact(person2, addressbook.id)
    # print "Retrieving contact named "+person2.first_name+" from "+addressbook.name
    # get_person2 = Contact.get(Contact.first_name == person2.first_name)
    # print_info(get_person2)
    #
    # print "Deleting "+person1.first_name+" from "+addressbook.name
    # del_person1 = Contact.get(Contact.id == person1_id)
    # del_person1.delete_instance()
    #
    # try:
    #     Contact.get(Contact.id == person1_id)
    # except DoesNotExist:
    #     print "Deletion successful!"
    #
    # print "Creating second addressbook..."
    # addressbook2 = create_addressbook(BOOK2)
    #
    # with db.atomic():
    #     for data in MOCK_DATA:
    #         data.update({'ab':addressbook2.id})
    #         Contact.create(**data)
    #
    # num_contacts = Contact.select().where(Contact.id == addressbook2.id).count()
    # print addressbook2.name+" now has "+str(num_contacts)+" contacts!"
    #
    # print "Exporting addressbook..."
    # export_addressbook(addressbook2.id, 'test.csv')
    #


if __name__ == "__main__":
    main()
