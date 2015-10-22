"""
Address Book Graphical User interface
Author: Abdulmajeed Kadi
Contributors in alphabetic order by last name:
        Max Kohl, Garrett Morrison, Hannah Smith, Joshua Yang
"""
import tkFileDialog
from Tkinter import *
from test import *
import tkSimpleDialog # For Addressbook name
import tkMessageBox


class Application(Frame):

    def retrieve_input(self):
        contact = {"first_name": None, "last_name": None, "address": None,
            "city": None, "state": None, "zip_code": None, "phone": None, "email": None}
        if self.address.get() == "Address line 2":
            address = self.address.get() + " " + self.address2.get()
        else:
            address = self.address.get()

        contact["first_name"] = self.fname.get()
        contact["last_name"] = self.lname.get()
        contact["address"] = address
        contact["city"] = self.city.get()
        contact["state"] = self.state.get()
        contact["zip_code"] = self.zip.get()
        contact["phone"] = self.phone.get()
        contact["email"] = self.email.get()

        return contact

    def add(self):
        contact = self.retrieve_input()
        person = create_contact(contact, addressbook.id) #FIXME: The 4 needs to be replaced by the addressbook.id of the book it belongs to
        #contact[8] = "add")
        new_contact = Contact.get(Contact.id == person)
        self.display_address(self,new_contact)

    def sort_contacts(self,*args):
        s = '\t\t'
        order = self.sort_by.get()
        if order == "Zip Code": # zip_code, ties broken by first name
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.zip_code,Contact.first_name)
            self.listbox.delete(0,END)
            for i in temp_list:
                self.listbox.insert(END, str(i.id) + s + i.first_name + s + i.last_name + s + i.address + s + i.city + s + i.state + s + i.zip_code)
        if order == "Last Name": # last name
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.first_name)
            self.listbox.delete(0,END)
            for i in temp_list:
                self.listbox.insert(END, str(i.id) + s + i.first_name + s + i.last_name + s + i.address + s + i.city + s + i.state + s + i.zip_code)
        if order == "First Name":
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.last_name)
            self.listbox.delete(0,END)
            for i in temp_list:
                self.listbox.insert(END, str(i.id) + s + i.first_name + s + i.last_name + s + i.address + s + i.city + s + i.state + s + i.zip_code)

    def list_content_update(self):
        a = ["strings"]
        # a = updated list from the data base "updated one". Each element of the
        # list should be "name tab tab zip"
        a = Contact.select() #FIXME: This is not the correct usage of this function
        self.display_address(self, a)

    def delete(self):

        try:
            if tkMessageBox.askyesno('Verify', 'Are you sure you want to delete?'):
                del_contact = Contact.get(Contact.id == self.id_box.get())
                del_contact.delete_instance()
                self.populate_listbox()

                self.fname.delete(0, END)
                self.lname.delete(0, END)
                self.address.delete(0, END)
                self.address2.delete(0, END)
                self.city.delete(0, END)
                self.state.delete(0, END)
                self.zip.delete(0, END)
                self.email.delete(0, END)
                self.phone.delete(0, END)
                self.id_box.delete(0, END)

            else:
                showinfo('No', 'Delete has been cancelled')
        except ValueError:
            print "Double click the contact you want to delete, then click delete again!"


    def searching(self):
        contact = self.search.get()
        contacts = string_search(contact, self.addressbook.id)
        s = "\t\t"
        self.create_listbox()
        for i in contacts:
            self.listbox.insert(END, str(i.id) + s + i.first_name + s + i.last_name + s + i.address + s + i.city + s + i.state + s + i.zip_code)

    def update(self):
        db_id = self.id_box.get()

        try:

            d = Contact.delete().where(Contact.id == db_id)
            d.execute()

        except ValueError:
            print "Double click the contact you want to update, then click update again!"

        self.add()
        self.populate_listbox()

    def erase(self):
        self.fname.delete(0, END)
        self.lname.delete(0, END)
        self.address.delete(0, END)
        self.address2.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zip.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.id_box.delete(0,END)
        print "Function, erase had happen to all feilds"

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0]).split("\t\t")


        contact = Contact.get(Contact.id == value[0])

        self.fname.delete(0, END)
        self.lname.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zip.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.id_box.delete(0,END)

        if(contact.first_name != "First name"):
            self.fname.insert(0, contact.first_name)
        if(contact.last_name != "Last name"):
            self.lname.insert(0, contact.last_name)
        if(contact.address != "Address"):
            self.address.insert(0, contact.address)
        if(contact.city != "City"):
            self.city.insert(0, contact.city)
        if(contact.state != "State"):
            self.state.insert(0, contact.state)
        if(contact.zip_code != "Zip"):
            self.zip.insert(0, contact.zip_code)
        if(contact.email != "Email address"):
            self.email.insert(0, contact.email)
        if(contact.phone != "Phone number"):
            self.phone.insert(0, contact.phone)

        self.id_box.insert(0, value[0])

        print self.id_box.get()

    def display_address(self, b, array): #FIXME: What is 'b'??
        s = "\t\t"
        if type(array) == dict:
            for item in array:
                if type(item) == str:
                    self.listbox.insert(END, item)
                else:
                    list_output = item.last_name + s + item.zip_code
                    self.listbox.insert(END, list_output)
        else:
            list_output = str(array.id) + s + array.first_name + s + array.last_name + s + array.address + s + array.city + s + array.state + s + array.zip_code
            self.listbox.insert(END, list_output)
        # self.listbox.place(x=1, y=2)
        # end of list view
    def populate_listbox(self):
        ab = self.addressbook.id
        contacts = Contact.select().where(Contact.ab == ab)
        s = "\t\t"
        self.create_listbox()
        for i in contacts:
            self.listbox.insert(END, str(i.id) + s + i.first_name + s + i.last_name + s + i.address + s + i.city + s + i.state + s + i.zip_code)

    def createWidgets(self):
        all_contact_instances = Contact.select()
        print(self.addressbook.id)
        # Textbox entry
        self.search = Entry(self, width=30)
        self.search.grid(row=1, column=0, columnspan=2,pady=10,padx=5)
        self.search.delete(0, END)
        self.search.insert(0, "Search for contact")

        self.fname = Entry(self, width=15)
        self.fname.grid(row=5, column=0, sticky=W,pady=5)
        self.fname.delete(0, END)
        self.fname.insert(0, "First name")

        self.lname = Entry(self, width=15)
        self.lname.grid(row=5,column=1, sticky=W,pady=5)
        self.lname.delete(0, END)
        self.lname.insert(0, "Last name")

        self.address = Entry(self, width=25)
        self.address.grid(row=6, sticky=W,pady=5)
        self.address.delete(0, END)
        self.address.insert(0, "Address line 1")

        self.address2 = Entry(self, width=25)
        self.address2.grid(row=7, sticky=W)
        self.address2.delete(0, END)
        self.address2.insert(0, "Address line 2")

        self.city = Entry(self, width=15)
        self.city.grid(row=8, sticky=W,pady=10)
        self.city.delete(0, END)
        self.city.insert(0, "City")

        self.state = Entry(self, width=15)
        self.state.grid(row=8, column=1, sticky=W,pady=5)
        self.state.delete(0, END)
        self.state.insert(0, "State")

        self.zip = Entry(self, width=10)
        self.zip.grid(row=8, column=2, sticky=W,pady=5)
        self.zip.delete(0, END)
        self.zip.insert(0, "Zip")

        self.email = Entry(self, width=20)
        self.email.grid(row=9, column=0, sticky=W,pady=5)
        self.email.delete(0, END)
        self.email.insert(0, "Email address")

        self.phone = Entry(self, width=20)
        self.phone.grid(row=10, column=0, sticky=W,pady=5)
        self.phone.delete(0, END)
        self.phone.insert(0, "Phone number")

        self.id_box = Entry(self, width=0)
        self.id_box.grid(row=16, column=0, sticky=W)
        self.id_box.delete(0, END)
        self.id_box.insert(0, "")
        # end of textbox
        # self.sort_label = Label(text="Sort by: ")
        # self.sort_label.grid(row=5,column=3,padx=5,pady=10,stick=E)
        sort = ["Last Name","First Name","Zip Code"]
        self.sort_by = StringVar()

        self.sort_by.trace("w",callback=self.sort_contacts)
        self.sort_option = OptionMenu(self,self.sort_by,*sort)

        self.sort_option.grid(row=5,column=3,sticky=W)
        # Bottons
        self.search_b = Button(self)
        self.search_b["text"] = "Search",
        self.search_b["command"] = self.searching
        self.search_b.grid(row=1, column=2)

        self.add_b = Button(self)
        self.add_b["text"] = "Add",
        self.add_b["command"] = self.add
        self.add_b.grid(row=14, column=1)

        self.delete_b = Button(self)
        self.delete_b["text"] = "Delete",
        self.delete_b["command"] = self.delete
        self.delete_b.grid(row=14, column=2)

        self.update_b = Button(self)
        self.update_b["text"] = "Update",
        self.update_b["command"] = self.update
        self.update_b.grid(row=14, column=3, sticky=E)

        self.erase_b = Button(self)
        self.erase_b["text"] = "New",
        self.erase_b["command"] = self.erase
        self.erase_b.grid(row=14, column=0, sticky=E)


        self.show_all = Button(self)
        self.show_all["text"] = "Show all contacts"
        self.show_all["command"] = self.populate_listbox
        self.show_all.grid(row=15, column=1)
        # end of bottons

        self.create_listbox()

        self.populate_listbox()


    def create_listbox(self):
        self.listbox = Listbox(self, width=75)
        self.listbox.grid(row=2, column=0, columnspan=10,pady=10,padx=5)
        self.listbox.bind("<Double-Button-1>", self.OnDouble)


    def export(self):
        test.export_addressbook("exported_filename.tsv", 1)

        # this function will call the function that will make the export of the
        # data base

    def impot(self):
        # this function will call the function that will make the import to the
        # data base
        print "imported"
        imported_contacts = askopenfilename()
        # now use "imported_contacts" as the file path of the file that you'll
        # parse contact from
        self.list_content_update()  # this call is so that we will get an updated listbox

    def __init__(self, addressbook, master=None):
        Frame.__init__(self, master,bd=10)
        #
        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New")

        menu.add_command(label="Export", command=self.export)
        menu.add_command(label="Import", command=self.impot)
        menu.add_command(label="Quit", command=self.quit)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Copy")

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

        self.canvas = Canvas(self, bg="white", width=400,
                             height=400, bd=0, highlightthickness=0)
        #
        self.grid()
        self.addressbook = addressbook
        self.createWidgets()

if __name__ == "__main__":
    root = Tk()
    root.geometry("540x426")
    create_tables()
    BOOK_NAME = tkSimpleDialog.askstring("Addressbook name","Enter addressbook name") #Simple dialog gets book name
    addressbook = create_addressbook(BOOK_NAME)

    # root.resizable(width=FALSE, height=FALSE) # this for the window to be unrealizable
    app = Application(addressbook, master=root)
    app.mainloop()