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
        person = create_contact(contact, 4) #FIXME: The 4 needs to be replaced by the addressbook.id of the book it belongs to
        #contact[8] = "add")
        new_contact = Contact.get(Contact.id == person)
        self.display_address(self,new_contact)


    def list_content_update(self):
        a = ["strings"]
        # a = updated list from the data base "updated one". Each element of the
        # list should be "name tab tab zip"
        a = Contact.select() #FIXME: This is not the correct usage of this function
        self.display_address(self, a)

    def delete(self):
        if askyesno('Verify', 'Are you sure you want to delete?'):
            contact = self.retrieve_input()
            contact[8] = "add"
            self.list_content_update()
            for i in contact:
                print(i)
        else:
            showinfo('No', 'Delete has been cancelled')

    def search(self):
        # need implementation
        # a call to the self.display_address(self, results_of_search)
        print "Function, search had happen to DB"

    def update(self):
        # need implementation
        self.list_content_update()
        print "Function, update had happen to DB"

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
        print "Function, erase had happen to all feilds"

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        print "selection:", selection, ": '%s'" % value

    def display_address(self, b, array): #FIXME: What is 'b'??
        if type(array) == dict:
            for item in array:
                if type(item) == str:
                    self.listbox.insert(END, item)
                else:
                    list_output = item.last_name + "\t\t" + item.zip_code
                    self.listbox.insert(END, list_output)
        else:
            list_output = array.last_name + "\t\t" + array.first_name + "\t\t" + array.address + "\t\t" + array.city + "\t\t" + array.state + "\t\t" + array.zip_code
            self.listbox.insert(END, list_output)
        # self.listbox.place(x=1, y=2)
        # end of list view

    def createWidgets(self):
    	all_contact_instances = Contact.select()
    	print all_contact_instances[0].lname
        # Textbox entry
        self.search = Entry(self, width=40)
        self.search.grid(row=1, column=0, columnspan=2)
        self.search.delete(0, END)
        self.search.insert(0, "Search for contact")

        self.fname = Entry(self, width=15)
        self.fname.grid(row=5, sticky=W)
        self.fname.delete(0, END)
        self.fname.insert(0, "First name")

        self.lname = Entry(self, width=10)
        self.lname.grid(row=5, column=1, sticky=W)
        self.lname.delete(0, END)
        self.lname.insert(0, "Last name")

        self.address = Entry(self, width=20)
        self.address.grid(row=6, sticky=W)
        self.address.delete(0, END)
        self.address.insert(0, "Address line 1")

        self.address2 = Entry(self, width=20)
        self.address2.grid(row=7, sticky=W)
        self.address2.delete(0, END)
        self.address2.insert(0, "Address line 2")

        self.city = Entry(self, width=10)
        self.city.grid(row=8, sticky=W)
        self.city.delete(0, END)
        self.city.insert(0, "City")

        self.state = Entry(self, width=5)
        self.state.grid(row=8, column=1, sticky=W)
        self.state.delete(0, END)
        self.state.insert(0, "State")

        self.zip = Entry(self, width=5)
        self.zip.grid(row=8, column=2, sticky=W)
        self.zip.delete(0, END)
        self.zip.insert(0, "Zip")

        self.email = Entry(self, width=18)
        self.email.grid(row=9, column=0, sticky=W)
        self.email.delete(0, END)
        self.email.insert(0, "Email address")

        self.phone = Entry(self, width=13)
        self.phone.grid(row=10, column=0, sticky=W)
        self.phone.delete(0, END)
        self.phone.insert(0, "Phone number")
        # end of textbox

        # Bottons
        self.searchB = Button(self)
        self.searchB["text"] = "Search",
        self.searchB["command"] = self.search
        self.searchB.grid(row=1, column=2)

        self.add_b = Button(self)
        self.add_b["text"] = "Add",
        self.add_b["command"] = self.add
        self.add_b.grid(row=13, column=1)

        self.delete_b = Button(self)
        self.delete_b["text"] = "Delete",
        self.delete_b["command"] = self.delete
        self.delete_b.grid(row=13, column=2)

        self.update_b = Button(self)
        self.update_b["text"] = "Update",
        self.update_b["command"] = self.update
        self.update_b.grid(row=13, column=3, sticky=E)

        self.erase_b = Button(self)
        self.erase_b["text"] = "New",
        self.erase_b["command"] = self.erase
        self.erase_b.grid(row=13, column=0, sticky=E)
        # end of bottons


        self.listbox = Listbox(self, width=65)
        self.listbox.grid(row=2, column=0, columnspan=6)
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

    def __init__(self, master=None):
        Frame.__init__(self, master)
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

        self.createWidgets()

if __name__ == "__main__":
    root = Tk()
    root.geometry("470x400")
    create_tables()
    BOOK_NAME = tkSimpleDialog.askstring("Book name","Enter book name") #Simple dialog gets book name
    addressbook = create_addressbook(BOOK_NAME)
    print("addressbook id: "+ str(addressbook.id))
    # root.resizable(width=FALSE, height=FALSE) # this for the window to be unrealizable
    app = Application(master=root)
    app.mainloop()
