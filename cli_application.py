

"""
CLI Address book application

Author: Hannah Smith
Contributors in alphabetic order by last name:
        Abdulmajeed Kadi, Max Kohl, Garrett Morrison, Joshua Yang
"""


from peewee import *
from playhouse.csv_loader import dump_csv
import sys
import csv


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
        print "Addressbook exists, opening..."
        addressbook = AddressBook.get(AddressBook.name == name)
    else:
        with db.transaction():
            addressbook = AddressBook.create(
                name=name,
            )

    return addressbook


def create_contact(contact, ab):
    """ Creates a new Contact and prints out the number of rows modified.
    :param contact: dict, the Contact to be created.
    :param ab: int, the id of the AddressBook the Contact will be added to.
    """
    try:
        print(type(contact))
        contact.update({'ab': ab})
        with db.transaction():
            person = Contact.create(**contact)
        # print person.save() # Prints 1 if successful
        print_info(person)
        return person.id  # Return id of Contact
    except IntegrityError:
        print 'Contact already exists'

# def display_all_contacts(addressbook_id):
#     """ Prints all contacts in an addressbook.
#     :param addressbook_id: int, id of the address book to print.
#     """
#     contacts = Contact.select().where(Contact.ab == addressbook_id)
#     print "{0:<15s} {1:<15s} {2:<15s} {3:<15s} {4:<15s} {5:<15s} {6:<15s} {7:<15s}".format("Last Name","First Name","Address","City","State","Zip Code","Phone","Email")
#     limit = 20
#     i = 0
#     while i < limit:
#         for contact in contacts:
#             print "{0:<15} {1:<15} {2:<015} {3:<15} {4:<15} {5:<15} {6!r:<15} {7:<015}".format(contact.last_name,contact.first_name, contact.address, contact.city, contact.state,contact.zip_code, contact.phone, contact.email)
#             i = i + 1

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


def string_search(info, ab):
    """Returns a list of contacts satisfying the search query.
    :param info: search term, will find this string for any field except ID
    :param ab: int, id of AddressBook being searched.
    """
    info = info.rstrip()
    if info == "" or info == "Search tool":
        return Contact.select().where(Contact.ab == ab)
    else:
        results = Contact.select().where(
         (Contact.ab == ab) & (
             (Contact.first_name.contains(info)) |
             (Contact.last_name.contains(info)) |
             (Contact.address.contains(info)) |
             (Contact.city.contains(info)) |
             (Contact.state.contains(info)) |
             (Contact.zip_code.contains(info)) |
             (Contact.phone.contains(info)) |
             (Contact.email.contains(info))
         ))
    return results


def delete_contact(contact):
    contact.delete_instance()


def print_info(contact):
    """ Prints a Contact.
    :param contact: Contact, the contact to print.
    """
    print contact.first_name + " " + contact.last_name + " " + contact.address + " " + contact.city + " " + contact.state + " " + contact.zip_code + " " + contact.phone + " " + contact.email


def import_addressbook(in_file, id):
    """ Adds Contacts from a csv file to an AddressBook.
    :param id: int, the id of the AddressBook to add Contacts to.
    :param csv_file: string, the file name of the csv to import.
    """
    contact_data = []
    try:
        with open(in_file, 'rb') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                row.update({'ab': id})
                contact_data.append(row)

        with db.atomic():
            for data_dict in contact_data:
                Contact.create(**data_dict)
        print "Created contacts in book with id " + str(id)
    except IOError:
        print "No such file exists!"
        return

def export_addressbook(out_file, id):
    """ Exports Contacts to a file in csv format.
    :param id: int, the id of the AddressBook to export.
    :param out_file: string, the file to export data to.
    """

    with open(out_file, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        query = Contact.select().where(Contact.ab == id).order_by(Contact.last_name)
        dump_csv(query, f, csv_writer=writer)

def edit_contact(contact):
    """ Allows user to edit Contact fields.
    :param contact: Contact, a contact model object.
    """
    keep_running = True
    while keep_running:
        print("CONTACT: " + contact.first_name + " " + contact.last_name)
        print("What field would you like to edit?")
        print_info(contact)
        prompt = "Enter option number:\n\t[1] First Name\n\t[2] Last Name\n\t[3] Address\n\t[4] City\n\t[5] State\n\t[6] Zip Code\n\t[7] Phone\n\t[8] Email\n\n[9] Exit"
        choice = get_user_input_as_int(prompt)
        if choice == 1:
            new = raw_input("Enter First Name: ")
            contact.first_name = new
            contact.save()
            keep_running = False
        elif choice ==2:
            new = raw_input("Enter Last Name: ")
            contact.last_name = new
            contact.save()
            keep_running = False
        elif choice == 3:
            new = raw_input("Enter Address: ")
            contact.address = new
            contact.save()
            keep_running = False
        elif choice == 4:
            new = raw_input("Enter City: ")
            contact.city = new
            contact.save()
            keep_running = False
        elif choice == 5:
            new = raw_input("Enter State: ")
            contact.state = new
            contact.save()
            keep_running = False
        elif choice == 6:
            new = raw_input("Enter Zip Code: ")
            contact.zip_code = new
            contact.save()
            keep_running = False
        elif choice == 7:
            new = raw_input("Enter Phone: ")
            contact.phone = new
            contact.save()
            keep_running = False
        elif choice == 8:
            new = raw_input("Enter Email: ")
            contact.email = new
            contact.save()
            keep_running = False
        elif choice == 9:
            keep_running = False
            contact_menu(contact)
        else:
            print "Invalid input! Returning to contact menu."
            keep_running = False
            contact_menu(contact)

def contact_menu(contact):
    keep_running = True
    ab = contact.ab

    while keep_running:
        print("CONTACT: " + contact.first_name + " " + contact.last_name)
        print_info(contact)
        ab = contact.ab
        prompt = "Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n"
        # print(
        #    "Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n")
        contact_action = get_user_input_as_int(prompt)
        # contact_action = int(raw_input(
        #    "Enter option number:\n\t[1] Edit Contact\n\t[2] Delete Contact\n\t[3] Return to main menu\n"))

        if contact_action == 1:
            edit_contact(contact)
            keep_running = False
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
        prompt = "Enter option number:\n\t[1] Add contact\n\t[2] Retrieve contact\n\t[3] Import address book\n\t[4] Export address book\n\t[5] Print contacts\n\t[6] Main Menu\n"
        book_action = get_user_input_as_int(prompt)
        # book_action = int(raw_input(
        #    "Enter option number:\n\t[1] Add contact\n\t[2] Retrieve contact\n\t[3] Import address book\n\t[4] Export address book\n\t[5] Main Menu\n"))

        if book_action == 1:
            contact = {"first_name": None, "last_name": None, "address": None,
            "city": None, "state": None, "zip_code": None, "phone": None, "email": None}
            print("Fill out the following contact fields. Press Enter to skip. Must fill out at least First/Last Name AND one other field.")

            prompt = "Last Name: "
            contact['last_name'] = get_user_input_as_string(prompt)
            prompt = "First Name: "
            contact['first_name'] = get_user_input_as_string(prompt)
            prompt = "Street Address: "
            contact['address'] = get_user_input_as_string(prompt)
            prompt = "City: "
            contact['city'] = get_user_input_as_string(prompt)
            prompt = "State: "
            contact['state'] = get_user_input_as_string(prompt)
            prompt = "Zip Code: "
            contact['zip_code'] = get_user_input_as_string(prompt)
            prompt = "Phone: "
            contact['phone'] = get_user_input_as_string(prompt)
            prompt = "Email: "
            contact['email'] = get_user_input_as_string(prompt)
            # contact[0] = raw_input("Last Name: ")
            # contact[1] = raw_input("First Name: ")
            # contact[2] = raw_input("Street Address: ")
            # contact[3] = raw_input("City: ")
            # contact[4] = raw_input("State: ")
            # contact[5] = raw_input("Zip Code: ")
            # contact[6] = raw_input("Phone: ")
            # contact[7] = raw_input("Email: ")

            create_contact(contact, addressbook.id)
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
            # IN_FILE = raw_input("Enter file name to import: ")
            import_addressbook(IN_FILE, addressbook.id)

        elif book_action == 4:
            prompt = "Enter file to export to: "
            OUT_FILE = get_user_input_as_string(prompt)
            # OUT_FILE = raw_input("Enter file to export to: ")
            export_addressbook(OUT_FILE, addressbook.id)

        elif book_action == 5:
            display_all_contacts(addressbook.id)

        elif book_action == 6:
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
            print("Invalid input, please enter string.")
        elif type(user_input) == str:
            valid_input = True
    return user_input.rstrip('\n')

def main():
    create_tables()
    keep_running = True

    while keep_running:
        print("ADDRESSBOOK APPLICATION\n")
        prompt = "Enter option number:\n\t[1] Create Address Book\n\t[2] Open Address Book\n\t[3] Exit\n"
        home_action = get_user_input_as_int(prompt)
        # home_action = int(raw_input(
        #    "Enter option number:\n\t[1] Create Address Book\n\t[2] Open Address Book\n\t[3] Exit\n"))

        if home_action == 1 or home_action == 2:
            prompt = "Enter name of Address Book: "
            BOOK_NAME = get_user_input_as_string(prompt)
            addressbook = create_addressbook(BOOK_NAME)
            book_menu(addressbook)
        elif home_action == 3:
            keep_running = False
            db.close()
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
