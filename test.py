from peewee import *
from fileUtils import *

#PY2EXE

DATABASE = 'application.db'
db = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        db = db

class AddressBook(BaseModel):
    name = CharField(unique=True)

    class Meta:
        order_by = ('id',)

class Contact(BaseModel):
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
    db.connect()
    db.create_tables([AddressBook,Contact])

# first_name =
# last_name =
# address =
# city =
# state =
# zip_code =
# phone =
# email =

def create_addressbook(name):
    try:
        with db.transaction():
            book = AddressBook.create(
                name = name,
            )

    except IntegrityError:
        print 'addressbook already exists'

def create_contact(contact,ab):
    try:
        with db.transaction():
            person = Contact.create(
                first_name = contact.first_name,
                last_name = contact.last_name,
                address = contact.address,
                city = contact.city,
                state = contact.state,
                zip_code = contact.zip_code,
                phone = contact.phone,
                email = contact.email,
                ab = ab
            )
        print person.save()
    except IntegrityError:
        print 'Contact already exists'

def add(contact,addressbook):
    try:
        create(contact,addressbook.id)
    except IntegrityError:
        pass

def search_contacts(last, first, ab):
    result = Contact.select().where(
        (Contact.last_name == last) &
        (Contact.first_name == first) &
        (Contact.ab == ab))
    for r in result:
        print 'RESULT: '+r.last_name+" "+r.first_name
    return result

def string_search(info, ab):
    results = Contact.select().where(
        (Contact.ab == ab) & (
        (Contact.first_name.contains(info)) |
        (Contact.last_name.contains(info)) |
        (Contact.address.contains(info)) |
        (Contact.city.contains(info)) |
        (Contact.state.contains(info)) |
        (Contact.zip_code.contains(info)) |
        (Contact.phone.contains(info)) |
        (Contact.email.comtains(info))
        ))
    for result in results:
        print_info(result)

def delete_contact(contact):
    contact.delete_instance()

def print_info(contact):
    print contact.first_name+" "+contact.last_name+" "+contact.address+" "+contact.city+" "+contact.state+" "+contact.zip_code+" "+contact.phone+" "+contact.email

def import_csv(ab):
    file_name = raw_input("Enter file to load")
    contact_data = process_csv(file_name,ab)

if __name__ == "__main__":

    # create 5 address books
    # for i in range(5):
    #     name = "book"+str(i)
    create_addressbook('book1')

    #BOOKS = AddressBook.select()

    #for book in BOOKS:
    with db.atomic():
        for data_dict in contact_list:
            Contact.create(**data_dict)
