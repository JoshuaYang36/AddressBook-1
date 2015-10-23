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
from tkFileDialog import askopenfilename

class Application(Frame):

    def retrieve_input(self):
        contact = {"first_name": None, "last_name": None, "address": None,
            "city": None, "state": None, "zip_code": None, "phone": None, "email": None}

        if self.address2.get() != "Address line 2":
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
        self.populate_listbox()

    def sort_contacts(self,*args):

        order = self.sort_by.get()
        if order == "Zip Code": # zip_code, ties broken by first name
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.zip_code,Contact.first_name)
            self.listbox.delete(0,END)
            for i in temp_list:

                if i.phone != "":
                    i.phone.replace(" ","")
                    phone = "(" + i.phone[0:3] + ")" + " "+ i.phone[3:6] + "-" + i.phone[6:10]
                else:
                    phone = ""
                fmt_str = "{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15} {6:<15} {7:<15} {8:<15}".format(str(i.id), i.last_name,i.first_name, i.address, i.city, i.state,i.zip_code, phone, i.email)
                self.listbox.insert(END, fmt_str)       

        if order == "Last Name": # last name
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.last_name)
            self.listbox.delete(0,END)
            for i in temp_list:

                if i.phone != "":
                    i.phone.replace(" ","")
                    phone = "(" + i.phone[0:3] + ")" + " "+ i.phone[3:6] + "-" + i.phone[6:10]
                else:
                    phone = ""
                fmt_str = "{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15} {6:<15} {7:<15} {8:<15}".format(str(i.id), i.last_name,i.first_name, i.address, i.city, i.state,i.zip_code, phone, i.email)
                self.listbox.insert(END, fmt_str)

        if order == "First Name":
            temp_list = Contact.select().where(Contact.ab == addressbook.id).order_by(Contact.first_name)
            self.listbox.delete(0,END)
            for i in temp_list:

                
                if i.phone != "":
                    i.phone.replace(" ","")
                    phone = "(" + i.phone[0:3] + ")" + " "+ i.phone[3:6] + "-" + i.phone[6:10]
                else:
                    phone = ""
                fmt_str = "{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15} {6:<15} {7:<15} {8:<15}".format(str(i.id), i.last_name,i.first_name, i.address, i.city, i.state,i.zip_code, phone, i.email)
                self.listbox.insert(END, fmt_str)



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

            if i.phone != "":
                i.phone.replace(" ","")
                phone = "(" + i.phone[0:3] + ")" + " "+ i.phone[3:6] + "-" + i.phone[6:10]
            else:
                    phone = ""
            fmt_str = "{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15} {6:<15} {7:<15} {8:<15}".format(str(i.id), i.last_name,i.first_name, i.address, i.city, i.state,i.zip_code, phone, i.email)
            self.listbox.insert(END, fmt_str)

            

    def update(self):
        db_id = self.id_box.get()
        print(db_id)
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

        super_id = ""
        value = widget.get(selection[0])

        for i in range (10):
            if value[i].isdigit():
                super_id += value[i]
            else:
                break

        contact = Contact.get(Contact.id == super_id)

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

        self.id_box.insert(0, super_id)


    def populate_listbox(self):
        ab = self.addressbook.id
        contacts = Contact.select().where(Contact.ab == ab)
        s = "\t\t"
        self.create_listbox()
        for i in contacts:

            if i.phone != "":
                i.phone.replace(" ","")
                phone = "(" + i.phone[0:3] + ")" + " "+ i.phone[3:6] + "-" + i.phone[6:10]
            else:
                    phone = ""
            fmt_str = "{0:<15} {1:<15} {2:<15} {3:<15} {4:<15} {5:<15} {6:<15} {7:<15} {8:<15}".format(str(i.id), i.last_name,i.first_name, i.address, i.city, i.state,i.zip_code, phone, i.email)
            self.listbox.insert(END, fmt_str)


    def createWidgets(self):
        all_contact_instances = Contact.select()

        # Textbox entry
        self.search = Entry(self, width=30)
        self.search.grid(row=1, column=0, columnspan=2,pady=5)
        self.search.delete(0, END)
        self.search.insert(0, "Search for contact")

        self.lfname = Label(self, text = "First Name")
        self.lfname.grid(row=5, column=0)

        self.fname = Entry(self, width=15)
        self.fname.grid(row=5, column=1, sticky=W)
        self.fname.delete(0, END)
      
        self.lfname = Label(self, text = "Last Name")
        self.lfname.grid(row=5, column=2)

        self.lname = Entry(self, width=15)
        self.lname.grid(row=5,column=3, sticky=W)
        self.lname.delete(0, END)
        

        self.laddress = Label(self, text = "Address 1")
        self.laddress.grid(row=6, column=0)

        self.address = Entry(self, width=25)
        self.address.grid(row=6, column=1, sticky=W)
        self.address.delete(0, END)
        


        self.laddress2 = Label(self, text = "Address 2")
        self.laddress2.grid(row=7, column=0)

        self.address2 = Entry(self, width=25)
        self.address2.grid(row=7, column=1, sticky=W)
        self.address2.delete(0, END)
   


        self.lcity = Label(self, text = "City")
        self.lcity.grid(row=8, column=0)

        self.city = Entry(self, width=15)
        self.city.grid(row=8, column =1, sticky=W)
        self.city.delete(0, END)
     


        self.lstate = Label(self, text = "State")
        self.lstate.grid(row=8, column=2)

        self.state = Entry(self, width=15)
        self.state.grid(row=8, column=3, sticky=W)
        self.state.delete(0, END)


        self.lzip = Label(self, text = "Zip Code")
        self.lzip.grid(row=8, column=4)

        self.zip = Entry(self, width=10)
        self.zip.grid(row=8, column=5, sticky=W)
        self.zip.delete(0, END)


        self.lemail = Label(self, text = "Email")
        self.lemail.grid(row=9, column=0)

        self.email = Entry(self, width=20)
        self.email.grid(row=9, column=1, sticky=W)
        self.email.delete(0, END)
        

        self.lphone = Label(self, text = "Phone")
        self.lphone.grid(row=10, column=0)

        self.phone = Entry(self, width=20)
        self.phone.grid(row=10, column=1, sticky=W)
        self.phone.delete(0, END)
        

        self.id_box = Entry(self, width=0)
        self.id_box.grid(row=16, column=0, sticky=W)
        self.id_box.delete(0, END)
        self.id_box.insert(0, "")
        # end of textbox
        # self.sort_label = Label(text="Sort by: ")
        # self.sort_label.grid(row=5,column=3,padx=5,pady=10,stick=E)
        sort = ["Last Name","First Name","Zip Code"]
        self.sort_by = StringVar()
        self.sort_by.set("Last Name")

        self.sort_by.trace("w",callback=self.sort_contacts)
        self.sort_option = OptionMenu(self,self.sort_by,*sort)


        self.sort_option.grid(row=5,column=5)
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
        self.listbox = Listbox(self, width=105)
        self.listbox.grid(row=2, column=0, columnspan=10,pady=10,padx=5)
        self.listbox.bind("<Double-Button-1>", self.OnDouble)


    def export(self):
        file_name = AddressBook.get(AddressBook.id == addressbook.id).name + ".tsv"
        export_addressbook(file_name, addressbook.id)

        # this function will call the function that will make the export of the
        # data base

    def impot(self):
        # this function will call the function that will make the import to the
        # data base
        imported_contacts = askopenfilename()
        populate_addressbook(imported_contacts,addressbook.id)
        # now use "imported_contacts" as the file path of the file that you'll
        # parse contact from
        self.populate_listbox()
        # this call is so that we will get an updated listbox

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
    root.geometry("760x470")
    create_tables()
    BOOK_NAME = tkSimpleDialog.askstring("Addressbook name","Enter addressbook name") #Simple dialog gets book name
    addressbook = create_addressbook(BOOK_NAME)

    # root.resizable(width=FALSE, height=FALSE) # this for the window to be unrealizable
    app = Application(addressbook, master=root)
    app.mainloop()
