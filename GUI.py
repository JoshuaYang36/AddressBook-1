from Tkinter import *

class Application(Frame):
	def add(self):
		print "Function, addition had happen to DB"
		
	def delete(self):
		print "Function, deletion had happen to DB"
	
	def display_address(self, b, array):
		# List view
		listbox = Listbox(self)
		listbox.pack()
		listbox.insert(END, "a list entry")
		for item in array:
			listbox.insert(END, item)
		#self.listbox.place(x=1, y=2)
		# end of list view

	def createWidgets(self):
		a = ["one", "two", "three", "four","one", "two", "three", "four","one", "two", "three", "four","one", "two", "three", "four"]
		self.display_address(self, a)
		
		# Textbox entry 
		self.e = Entry(self)
		#self.e.grid(row=0,column=0)
		#self.e.pack()
		self.e.delete(0, END)
		self.e.insert(0, "a default value")
		self.e.pack({"side": "top"})
		#self.e.place(x=160, y=35, width=120, height=25) 
		#self.e.grid(row=0,column=0)
		
		self.e2 = Entry(self)
		self.e2.pack()
		self.e2.delete(0, END)
		self.e2.insert(0, "a default value")
		self.e2.pack({"side": "bottom"})
		
		
		# end of textbox
		
		#Bottons
		self.add_b = Button(self)
		self.add_b["text"] = "Add",
		self.add_b["command"] = self.add
		self.add_b.pack({"side": "left"})
		
		self.delete_b = Button(self)
		self.delete_b["text"] = "Delete",
		self.delete_b["command"] = self.delete
		self.delete_b.pack({"side": "left"})
		
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		self.QUIT.pack({"side": "left"})
		
		# end of bottons
		
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		
root = Tk()
root.geometry("500x500")

#root.resizable(width=FALSE, height=FALSE) # this for the window to be unrealizable  
app = Application(master=root)
app.mainloop()
root.destroy()
