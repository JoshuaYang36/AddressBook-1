import string
import os
from peewee import *
from addressbook import AddressBook
from contact import Contact

# class Contact(object):
#     __init__(self, first_name, last_name, ):
#         self.first_name
#         se


def add_contact():
    addressbook_name = get_address_book()
    print addressbook_name
    addressbook = open(addressbook_name, "r")
    if os.path.getsize(addressbook_name) == 0:
        contact_list = []
    else:
        contact_list = pickle.load(addressbook)
    contact = get_contact_info()
    addressbook = open(addressbook_name,"wb")
    contact_list.append(contact)
    pickle.dump(contact_list, addressbook)
    print "Added contact to" + addressbook_name
    addressbook.close()


def get_address_book():
    addressbook_name = raw_input("Addressbook name: ")
    return addressbook_name


def get_contact_info():
    """
    Initiates a Null filled contact list and prompts users to fill out the fields, with a requirement of
    filling out at least one of the First/Last names, plus one other field.
    """
    # Prompts user to fill contact list with manual inputs
    print("Fill out the following contact fields. Press Enter to skip. Must fill out at least First/Last Name AND one other field.")
    # ln = raw_input("Last Name: ")
    # fn = raw_input("First Name: ")
    # adr = raw_input("Street Address: ")
    # ct = raw_input("City: ")
    # st = raw_input("State: ")
    # zc = raw_input("Zip Code: ")
    # ph = raw_input("Phone: ")
    # em = raw_input("Email: ")
    contact = [None] * 8
    contact[0] = raw_input("Last Name: ")
    contact[1] = raw_input("First Name: ")
    contact[2] = raw_input("Street Address: ")
    contact[3] = raw_input("City: ")
    contact[4] = raw_input("State: ")
    contact[5] = raw_input("Zip Code: ")
    contact[6] = raw_input("Phone: ")
    contact[7] = raw_input("Email: ")

    # contact.append(ln)
    # contact.append(fn)
    # contact.append(adr)
    # contact.append(ct)
    # contact.append(st)
    # contact.append(zc)
    # contact.append(ph)
    # contact.append(em)
    new_contact = Contact(contact)
    return new_contact
    # Checks to see if either first or last name has been filled out. Or both.
    iterate = True
    while iterate:
        if contact[0] == "" and contact[1] == "":
            print("Must fill out at least one of the name entries (First/Last)")
            contact[0] = raw_input("Last Name: ")
            contact[1] = raw_input("First Name: ")
        else:
            iterate = False

    # Checks to see if at least one other field is filled in.
    entries = 0
    for item in contact:
        if item != "":
            entries += 1

    # If not one other field is filled, will repeatedly prompt user to do so
    iterate = True
    while iterate:
        if entries >= 3:
            iterate = False
            new_contact = Contact(contact)
            return new_contact
        else:
            print("Must fill out at least one of the following fields.")
            contact[2] = raw_input("Street Address: ")
            contact[3] = raw_input("City: ")
            contact[4] = raw_input("State: ")
            contact[5] = raw_input("Zip Code: ")
            contact[6] = raw_input("Phone: ")
            contact[7] = raw_input("Email: ")

def find_contact_info():
    contact = [None] * 3
    contact[0] = raw_input("Last Name: ")
    contact[1] = raw_input("First Name: ")
    contact[2] = raw_input("Zip Code: ")

    return contact

def retreive():
    addressbook_name = get_address_book()
    print addressbook_name
    addressbook = open(addressbook_name, "r")
    if os.path.getsize(addressbook_name) == 0:
        contact_list = []
    else:
        contact_list = pickle.load(addressbook)
    contact_info = find_contact_info()
    first_name = contact_info[0]
    last_name = contact_info[1]
    zip_code = contact_info[2]

    for contact in contact_list:
        if contact.first_name == first_name or contact.last_name == last_name or contact.zip_code == zip_code:
            print contact
    addressbook.close()

def delete():
    addressbook_name = get_address_book()
    print addressbook_name
    addressbook = open(addressbook_name, "r")
    if os.path.getsize(addressbook_name) == 0:
        print "Addressbook is empty"
        return
    else:
        contact_list = pickle.load(addressbook)
    contact_info = find_contact_info()
    first_name = raw_input("Enter First Name to be deleted: ")

    for contact in contact_list:
        if contact.first_name == first_name:
            contact_list.remove(contact)
            print "Removed contact"
    pickle.dump(contact_list,addressbook)
    addressbook.close()

def display():
    addressbook_name = get_address_book()
    print addressbook_name
    addressbook = open(addressbook_name, "r")
    if os.path.getsize(addressbook_name) == 0:
        print "Addressbook is empty"
        return
    else:
        contact_list = pickle.load(addressbook)
    for contact in contact_list:
        print contact

    addressbook.close()


iterate = True
while iterate:
    action = raw_input(
        "What would you like to do? Choose one: \n\t[1] Add\n\t[2] Delete\n\t[3] Retrieve\n\t[4] Display\n\t[5] Quit ")

    if action == "add" or action == "1":
        # iterate = False
        add_contact()
    elif action == "delete" or action == "2":
        # iterate = False
        delete()
    elif action == "retrieve" or action == "3":
        # iterate = False
        retreive()
    elif action == "display" or action == "4":
        # iterate = False
        display()
    elif action == "quit" or action == "5":
        break
    else:
        print("Invalid input. Please type one -> (Add/Delete/Retrieve/Edit)")
