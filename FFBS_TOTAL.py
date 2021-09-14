from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

login_page = Tk()
login_page.geometry("1080x720+250+0")
login_page.resizable(False,False)
login_page.title("FastFood Billing System")
if "nt" == os.name:
	login_page.iconbitmap('mainiconw.ico')
else:
	login_page.iconbitmap('@mainicon.xbm')
bg = PhotoImage(file="background720p.png")
label1 = Label(login_page, image = bg)
label1.place(x = 0, y = 0)

#Functions
def calculate():
	total = 0
	#print(items)
	#print(prices)
	q = []
	for data in qtys:
		q.append(int(data.get()))
	#print(q)
	for t in range(len(q)):
		total = total + q[t]*prices[t]
	#print(total)
	totalTxt.config(text = " Total Cost = Rs."+str(total))
def submit():
	stotal = 0
	orderDetails = []
	sq = []
	for data in qtys:
		sq.append(int(data.get()))
	for t in range(len(sq)):
		stotal = stotal + sq[t]*prices[t]
	
	for i in range(len(sq)):
		if sq[i] != 0:
			#print(items[i])
			#print(prices[i])
			#print(sq[i])
			orderDetails.append("Item :"+str(items[i])+";"+"Price :Rs."+str(prices[i])+";"+"Quantity :"+str(sq[i]))
	
	customer = custEntry.get()
	mobile = mobEntry.get()
	amt = stotal
	print(customer)
	print(mobile)
	print(orderDetails)
	print(amt)
	custEntry.delete(0,END)
	mobEntry.delete(0,END)
	messagebox.showinfo("Order Status","Order Placed Successfully")
	pass
def updateDb():
	conn = sqlite3.connect("Menu.db")
	c = conn.cursor()
	c.execute("""UPDATE itemList SET 
		item_name = :updatedName,
		item_price = :updatedPrice
		
		WHERE oid = :oid""",
		{
			'updatedName' : itemNameEdit.get(),
			'updatedPrice' : itemPriceEdit.get(),
			'oid' : selectEntry.get()
		})
	conn.commit()
	conn.close()
	updateWindow.destroy()
	selectEntry.delete(0,END)
	messagebox.showinfo("Information", "Data has been Modified")
	viewDb()

def login():
	username = str(userEntry.get())
	password = str(passEntry.get())
	if username == "admin" and password == "1234" :
		def updateGui():
			global updateWindow
			updateWindow = Toplevel()
			updateWindow.geometry("640x360+250+0")
			
			
			conn = sqlite3.connect("Menu.db")
			c = conn.cursor()
			global itemNameEdit
			global itemPriceEdit
			itemName = Label(updateWindow, text = "Item Name :", font =("",20))
			itemName.place(x = 50, y = 20)
			itemNameEdit = Entry(updateWindow, font = "TimesNewRoman 20", bg = 'white', fg ='black')
			itemNameEdit.place(x = 200, y = 20)
			itemPrice = Label(updateWindow, text = "Item Name :", font =("",20))
			itemPrice.place(x = 50, y = 80)
			itemPriceEdit = Entry(updateWindow, font = "TimesNewRoman 20", bg = 'white', fg ='black')
			itemPriceEdit.place(x = 200, y = 80)
			updateBtn = Button(updateWindow, text = "Update Record", font = ("Segoe UI",20),command = updateDb)
			updateBtn.place(x= 160, y = 140)
			
			c.execute("SELECT * FROM itemList WHERE oid = (:placeholder)",
			{
				 'placeholder' : selectEntry.get()
			})
			#placeholder = selectEntry.get()
			itemDetails = c.fetchall()
			for record in itemDetails:
				itemNameEdit.insert(0,record[0])
				itemPriceEdit.insert(0,record[1])
			
			conn.commit()
			conn.close()
		def delToDb():
			conn = sqlite3.connect("Menu.db")
			c = conn.cursor()
			c.execute("DELETE FROM itemList WHERE oid = (:placeholder)",
			{
				 'placeholder' : selectEntry.get()
			})
			#placeholder = selectEntry.get()
			selectEntry.delete(0,END)
			conn.commit()
			conn.close()
			
			messagebox.showinfo("Report","Data Deleted Successfully")
			viewDb()
		def addToDb() :
			#Create a database connection
			conn = sqlite3.connect("Menu.db")
			#Create cursor
			c = conn.cursor()
			#Add data to the table
			c.execute("INSERT INTO itemList VALUES (:itemNameEntry, :itemPriceEntry)",
				{
					'itemNameEntry' : itemNameEntry.get(),     #python dictionary key : value
					'itemPriceEntry' : itemPriceEntry.get()
					})
			messagebox.showinfo("Report","Data Added Successfully")
			#Commit changes in the database
			conn.commit()
			#Close the connection of the database
			conn.close()
			#Clear the previous data on the Entry widget
			itemNameEntry.delete(0, END)
			itemPriceEntry.delete(0, END)
			return
		admin_frame = Frame(login_page, bg = "white")
		admin_frame.place(x=0, y = 0, height = 720, width = 1080)
		#Background
		label2 = Label(admin_frame, image = bg) 
		label2.place(x = 0, y = 0)
		#Take Item name
		itemNameLabel = Label(admin_frame, text = "Item Name :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		itemNameLabel.place(x = 50, y = 20)
		itemNameEntry = Entry(admin_frame,font = ("Timesnewroman",20), bg = "white", fg = "black")
		itemNameEntry.place(x = 210, y = 20)
		#Take Item price
		itemPriceLabel = Label(admin_frame, text = "Item Price :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		itemPriceLabel.place(x = 600, y = 20)
		itemPriceEntry = Entry(admin_frame,font = ("Timesnewroman",20), bg = "white", fg = "black")
		itemPriceEntry.place(x = 750, y = 20)
		#Select Item
		selectLabel = Label(admin_frame, text = "Select Item :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		selectLabel.place(x = 700, y = 400)
		global selectEntry
		selectEntry = Entry(admin_frame,font = ("Timesnewroman",20), bg = "white", fg = "black", width = 5)
		selectEntry.place(x = 850, y = 400)
		#Button addToDb
		addToDbBtn = Button(admin_frame, text = "Add Item", font = "Monospace 20", bg = "#F78D0D", fg = "black", command = addToDb)
		addToDbBtn.place(x = 700, y = 150)
		#Button viewDb
		viewDbBtn = Button(admin_frame, text = "View Items", font = "Monospace 20", bg = "#F78D0D", fg = "black", command = viewDb)
		viewDbBtn.place(x = 200, y = 150)
		#Button Update
		updateDbBtn = Button(admin_frame, text = "Update Items", font = "Monospace 20", bg = "#F78D0D", fg = "black", command = updateGui)
		updateDbBtn.place(x = 700, y = 550)
		#Button Delete
		delToDbBtn = Button(admin_frame, text = "Delete Items", font = "Monospace 20", bg = "#F78D0D", fg = "black", command = delToDb)
		delToDbBtn.place(x = 700, y = 650)
		#global logoutBtn
		#logoutBtn = Button(login_page,text= "Logout->", font = "Monospace 20", command = lambda : login_page.mainloop(self))
		#logoutBtn.place(x = 50, y = 650)
		return
		
	elif username == "cashier" and password == "4321" :
		cashier_frame = Frame(login_page, bg = "white")
		cashier_frame.place(x=0, y = 0, height = 720, width = 1080)
		#Background
		label3 = Label(cashier_frame, image = bg) 
		label3.place(x = 0, y = 0)
		#Create a database connection
		conn = sqlite3.connect("Menu.db")
		#Create cursor
		c = conn.cursor()
		c.execute("SELECT *, oid FROM itemList")
		itemDetails = c.fetchall()
		global items
		global prices
		global qtys
		items = []
		prices = []
		qtys = []
		#Customer details
		custLbl = Label(cashier_frame, text = "Customer Name :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		custLbl.place(x = 50, y = 25)
		global custEntry
		global mobEntry
		custEntry = Entry(cashier_frame, font = "TimesNewRoman 20", bg= "white", fg = "black")
		custEntry.place(x = 250, y = 25)
		mobLb = Label(cashier_frame, text = "Contact No. :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		mobLb.place(x = 605, y = 25)
		mobEntry = Entry(cashier_frame, font = "TimesNewRoman 20", bg= "white", fg = "black")
		mobEntry.place(x = 760, y = 25)
		global totalTxt
		totalTxt = Label(cashier_frame, text = "", font=("Franktur",20,"bold"), bg = "#e6f7ff", fg = "black")
		totalTxt.place(x= 750, y = 570)
		#Main Frame
		mainframe = Frame(login_page)
		mainframe.place(x=50,y=100)
		#Canvas create
		mycanvas = Canvas(mainframe, bg= 'white', height = 300,width=475)
		mycanvas.pack(side = LEFT, fill = BOTH, expand = 1)
		#Add a scrollbar to canvas
		my_scbar = ttk.Scrollbar(mainframe, orient = "vertical", command = mycanvas.yview)
		my_scbar.pack(side = RIGHT, fill=Y)
		#Config canvas
		mycanvas.configure(yscrollcommand = my_scbar.set)
		mycanvas.bind('<Configure>', lambda e : mycanvas.configure(scrollregion=mycanvas.bbox("all")))
		#2nd frame inside canvas
		second_frame = Frame(mycanvas, bg='white')
		#Add 2nd frame to window
		mycanvas.create_window((0,0), window = second_frame,anchor = "nw")
		
		#From database
		j=1
		for i in itemDetails :
			j=j+5
			itemNameLabel = Label(second_frame, text = str(i[2]) + " " + str(i[0]), font = "TimesNewRoman 20", bg = "white", fg = "black")
			itemNameLabel.grid(row = j, column = 0, sticky = W, padx =(8,20), pady = 6)
			itemPriceLabel = Label(second_frame, text = "Rs."+str(i[1]), font = "TimesNewRoman 20", bg = "white", fg = "black")
			itemPriceLabel.grid(row = j, column = 5, sticky = W,padx=15,pady = 6)           
			itemQtyLabel = Label(second_frame, text = "Qty :", font = "TimesNewRoman 20", bg = "white", fg = "black")
			itemQtyLabel.grid(row = j, column = 8, sticky = W,pady = 6)             
			itemQty = Entry(second_frame,font = ("Timesnewroman",20), bg = "white", fg = "black", width = 5)
			itemQty.insert(0,0)
			itemQty.grid(row = j, column = 10, sticky = W,padx = 4, pady = 6)                  
			items.append(i[0])
			prices.append(i[1])
			qtys.append(itemQty)
		
		#Commit changes in the database
		conn.commit()
		#Close the connection of the database
		conn.close()
		calBtn = Button(login_page, text = "Calculate Total", font = "Monospace 20", command = calculate, cursor = "hand2")
		calBtn.place(x= 750, y = 500)
		submitBtn = Button(login_page, text = "  Place Order  ", font = "Monospace 20", bg= '#993300',fg='black', cursor = "hand2", command = submit)
		submitBtn.place(x= 750, y = 650)
		#logoutBtn = Button(login_page,text= "Logout->", font = "Monospace 20", command = lambda : login_page.mainloop(self))
		#logoutBtn.place(x = 50, y = 650)
	else :
		messagebox.showerror("Error","Retry, Invalid Login", parent = login_page)

def viewDb():
	#Main Frame
	mainframe = Frame(login_page)
	mainframe.place(x=50,y=200)
	#Canvas create
	mycanvas = Canvas(mainframe, bg= 'white', height = 300,width=475)
	mycanvas.pack(side = LEFT, fill = BOTH, expand = 1)
	#Add a scrollbar to canvas
	my_scbar = ttk.Scrollbar(mainframe, orient = "vertical", command = mycanvas.yview)
	my_scbar.pack(side = RIGHT, fill=Y)
	#Config canvas
	mycanvas.configure(yscrollcommand = my_scbar.set)
	mycanvas.bind('<Configure>', lambda e : mycanvas.configure(scrollregion=mycanvas.bbox("all")))
	#2nd frame inside canvas
	second_frame = Frame(mycanvas, bg='white')
	#Add 2nd frame to window
	mycanvas.create_window((0,0), window = second_frame,anchor = "nw")
	
	#From database
	#Create a database connection
	conn = sqlite3.connect("Menu.db")
	#Create cursor
	c = conn.cursor()
	c.execute("SELECT *, oid FROM itemList")
	itemDetails = c.fetchall()
	
	j=1
	for i in itemDetails :
		j=j+5
		itemNameLabel = Label(second_frame, text = str(i[2]) + " " + str(i[0]), font = "TimesNewRoman 20", bg = "white", fg = "black")
		itemNameLabel.grid(row = j, column = 0, sticky = W, padx =(8,20), pady = 6)
		itemPriceLabel = Label(second_frame, text = "Rs."+str(i[1]), font = "TimesNewRoman 20", bg = "white", fg = "black")
		itemPriceLabel.grid(row = j, column = 5, sticky = W,padx=15,pady = 6)           
		#itemQtyLabel = Label(second_frame, text = "Qty :", font = "TimesNewRoman 20", bg = "white", fg = "black")
		#itemQtyLabel.grid(row = j, column = 8, sticky = W,pady = 6)             
		#itemQty = Entry(second_frame,font = ("Timesnewroman",20), bg = "white", fg = "black", width = 5)
		#itemQty.insert(0,0)
		#itemQty.grid(row = j, column = 10, sticky = W,padx = 4, pady = 6)                 
	#Commit changes in the database
	conn.commit()
	#Close the connection of the database
	conn.close()
#Create a frame for login
login_frame = Frame(login_page, bg = "white")
login_frame.place(x=150, y = 150, height = 300, width = 500)
titleLabel = Label(login_frame, text = "Please Login", font = "Timesnewroman 20 bold", bg = "white", fg = "#F78D0D")
titleLabel.place(x = 55, y = 25)
#Username field
userLabel = Label(login_frame, text = "Username", font = ("Goudy old style", 15, "bold"), bg = "white", fg = "gray")
userLabel.place(x = 55, y = 85)
userEntry = Entry(login_frame, font = ("Timesnewroman",15), bg = "white", fg = "black")
userEntry.place(x = 55, y = 115)
#Password field
passLabel = Label(login_frame, text = "Password", font = ("Goudy old style", 15, "bold"), bg = "white", fg = "gray")
passLabel.place(x = 55, y = 170)
passEntry = Entry(login_frame, font = ("Timesnewroman",15), bg = "white", fg = "black")
passEntry.place(x = 55, y = 200)
#Login Button
loginBtn = Button(login_page, text = "Login", font = ("Monospace",15,"bold"), width = 10, bg = "#F78D0D", fg = "black", cursor = "hand2", command = login)
loginBtn.place(x = 325, y = 430)

login_page.mainloop()
