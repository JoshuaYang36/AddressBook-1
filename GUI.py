


"""
Address Book Graphical User interface

Author: Abdulmajeed Kadi
Contributors in alphabetic order by last name:
        Max Kohl, Garrett Morrison, Hannah Smith, Joshua Yang
"""


from Tkinter import *

class Application(Frame):
	def add(self):
		print "Function, addition had happen to DB"
	"""def add(self, fname, lname, ad1, ad2, city, state, zip):
		print fname
		print lname
		print ad1
		print ad2
		print city
		print state
		print zip"""
		
	def delete(self):
		print "Function, deletion had happen to DB"
	
	def searc(self):
		print "Function, search had happen to DB"
	
	def update(self):
		print "Function, update had happen to DB"
	
	def erase(self):
		print "Function, erase had happen to all feilds"
		
	def OnDouble(self, event):
		widget = event.widget
		selection=widget.curselection()
		value = widget.get(selection[0])
		print "selection:", selection, ": '%s'" % value
		
	def display_address(self, b, array):
		# List view
		listbox = Listbox(self, width=25)
		listbox.grid(row=2,column=0)
		listbox.insert(END, "a list entry")
		listbox.bind("<Double-Button-1>", self.OnDouble)
		for item in array:
			listbox.insert(END, item)
		#self.listbox.place(x=1, y=2)
		# end of list view

	def createWidgets(self):
		a = ["one", "two", "three", "four"]
		self.display_address(self, a)
		
		# Textbox entry
		self.search = Entry(self, width=20)
		self.search.grid(row=1,column=0)
		self.search.delete(0, END)
		self.search.insert(0, "Search tool")
		 
		self.fname = Entry(self, width=15)
		self.fname.grid(row=5,sticky=W)
		self.fname.delete(0, END)
		self.fname.insert(0, "First name")
		
		self.lname = Entry(self, width=10)
		self.lname.grid(row=5,column=1, sticky=W)
		self.lname.delete(0, END)
		self.lname.insert(0, "Last name")
		
		self.address = Entry(self, width=20)
		self.address.grid(row=6,sticky=W)
		self.address.delete(0, END)
		self.address.insert(0, "Address line 1")
		
		self.address2 = Entry(self, width=20)
		self.address2.grid(row=7,sticky=W)
		self.address2.delete(0, END)
		self.address2.insert(0, "Address line 2")
		
		self.city = Entry(self, width=10)
		self.city.grid(row=8, sticky=W)
		self.city.delete(0, END)
		self.city.insert(0, "City")
		
		self.state = Entry(self, width=5)
		self.state.grid(row=8,column=1, sticky=W)
		self.state.delete(0, END)
		self.state.insert(0, "State")
		
		self.zip = Entry(self, width=5)
		self.zip.grid(row=8,column=2)
		self.zip.delete(0, END)
		self.zip.insert(0, "Zip")
		
		self.email = Entry(self, width=18)
		self.email.grid(row=9,column=0, sticky=W)
		self.email.delete(0, END)
		self.email.insert(0, "Email address")
		
		self.phone = Entry(self, width=13)
		self.phone.grid(row=10,column=0, sticky=W)
		self.phone.delete(0, END)
		self.phone.insert(0, "Phone number")
		# end of textbox
		
		#Bottons
		self.searchB = Button(self)
		self.searchB["text"] = "Search",
		self.searchB["command"] = self.searc
		self.searchB.grid(row=1,column=1)
		
		self.add_b = Button(self)
		self.add_b["text"] = "Add",
		#self.add_b["command"] = self.add(self, fname.get(), lname.get(), address.get(), address2.get(), city.get(), state.get(), zip.get())
		self.add_b["command"] = self.add
		self.add_b.grid(row=10,column=2, sticky=W)
		
		self.delete_b = Button(self)
		self.delete_b["text"] = "Delete",
		self.delete_b["command"] = self.delete
		self.delete_b.grid(row=13,column=1, sticky=W)
		
		self.update_b = Button(self)
		self.update_b["text"] = "Update",
		self.update_b["command"] = self.update
		self.update_b.grid(row=13,column=2, sticky=W)
		
		self.erase_b = Button(self)
		self.erase_b["text"] = "Erase",
		self.erase_b["command"] = self.erase
		self.erase_b.grid(row=10,column=1, sticky=W)
		# end of bottons
		
	def __init__(self, master=None):
		Frame.__init__(self, master)
		#
		self.menubar = Menu(self)
		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=menu)
		menu.add_command(label="New")
		menu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Edit", menu=menu)
		menu.add_command(label="Copy")
		
		try:
			self.master.config(menu=self.menubar)
		except AttributeError:
			# master is a toplevel window (Python 1.4/Tkinter 1.63)
			self.master.tk.call(master, "config", "-menu", self.menubar)
			
		self.canvas = Canvas(self, bg="white", width=400, height=400, bd=0, highlightthickness=0)
		#
		self.grid()
		self.createWidgets()

if __name__ == "__main__":
	root = Tk()
	root.geometry("430x400")
	#root.resizable(width=FALSE, height=FALSE) # this for the window to be unrealizable  
	app = Application(master=root)
	app.mainloop()
	root.destroy()
	
