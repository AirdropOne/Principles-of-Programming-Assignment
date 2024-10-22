import tkinter
import mysql.connector
import sqlite3
from login_registration import Login_Page
from tkinter import ttk



class Catalogue_Page():                                                    ## Catalogue page class  ## Setting as a class for future reusability for user experience and admin experience branches


    def __init__(self, root):
        self.catalogue_window=root
        self.catalogue_window.title("Catalogue Page")
        self.catalogue_window.geometry("400x300")

        self.infolabel=tkinter.Label(self.catalogue_window, text="Catalogue Page")

        self.search_var=tkinter.StringVar()                                                     ## making sure to read field entry inputs as strings - can be called back to later

        self.search_label=tkinter.Label(self.catalogue_window, text="Search")
        self.search_label.grid(row=1, column=0)

        self.search_entry=tkinter.Entry(self.catalogue_window, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=1)

        self.search_button=tkinter.Button(self.catalogue_window, text="Search")
        self.search_button.grid(row=1, column=2)

        self.login_button=tkinter.Button(self.catalogue_window, text="Login", command=self.open_login_page)
        self.login_button.grid(row=1, column=3)

        self.catagory_var=tkinter.StringVar(value="All Catagories")                                         ## for reading the selected catagory as a string, and setting the default value to "All catagories" - can be called back to later
        self.category_label=tkinter.Label(root, text="Filter by Category")                                  ## Label for the category filter
        self.category_label.grid(row=2, column=0)

        self.category_menu=ttk.Combobox(root, textvariable=self.catagory_var)                               ## Combobox function for the category filter, and applying the variable to the selected value string "All Categories"
        self.category_menu['values'] = ("All Categories", "Bicycles", "Accessories")                        ## setting the valuees for the category
        self.category_menu.grid(row=2, column=1)
    

        self.catalogue_frame=tkinter.Frame(self.catalogue_window)                                           ## Frame for the displaying the products in
        self.catalogue_frame.grid(row=3, column=0, columnspan=4)    
        self.display_products(self.pull_products())                                                       ## Displaying the products in the frame, pulled from the database




    def open_login_page(self):
        Login_Page(self.catalogue_window)                   ## open the login page (alrady defined as a top window)   



    def pull_products(self):
        connect = sqlite3.connect("bike_shop_DB.db")                                                ## assigning a name to the funtion of connecting to my practise datatbase         and       remember the .db
        c = connect.cursor() 

        c.execute("SELECT name, catagory, price, quantity FROM Product_Database")                             ## Pulling the name, catagory and price from the products table
        rows=c.fetchall()       
        return rows                                                                                 ## fetching all the rows in the table and returning them


    def display_products(self, products):                           ## take the products pulled from the database and but them into the frame
        for widget in self.catalogue_frame.winfo_children():          ## for each widget in the frame
            widget.destroy()                                         ## destroy the widget to clear previous products displayed
        
        for row in self.pull_products():                            ## for each row in the pulled products
            product_label=tkinter.Label(self.catalogue_frame, text=row[0] + " " + row[1] + " " + str(row[2]) + " " + str(row[3]))   ## create a label for the product with the name, catagory, price and quantity  (price and quantity needs to be converted to a string) within the frame
            product_label.pack()                                    ## pack the label into the frame to display the product

        


    #def search_products(self):
     #   search_query=self.search_var.get().lower                          ## get the search query from the search field and convert it to lowercase
      #  selected_catagory=self.catagory_var.get()                        ## get the selected catagory from the catagory combobox dropdown




if __name__ == "__main__":
    root = tkinter.Tk()
    app = Catalogue_Page(root)
    root.mainloop()


    