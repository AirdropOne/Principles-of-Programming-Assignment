import tkinter
import mysql.connector
import sqlite3
from login_registration import Login_Page




class Catalogue_Page():                                                    ## Catalogue page class  ## Setting as a class for future reusability for user experience and admin experience branches


    def __init__(self, root):
        self.catalogue_window=root
        self.catalogue_window.title("Catalogue Page")
        self.catalogue_window.geometry("400x300")

        self.infolabel=tkinter.Label(self.catalogue_window, text="Catalogue Page")

        self.search_var=tkinter.StringVar()                                                     ## making sure to read field entry inputs as strings

        self.search_label=tkinter.Label(self.catalogue_window, text="Search")
        self.search_label.grid(row=1, column=0)

        self.search_entry=tkinter.Entry(self.catalogue_window, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=1)

        self.search_button=tkinter.Button(self.catalogue_window, text="Search")
        self.search_button.grid(row=1, column=2)

        self.login_button=tkinter.Button(self.catalogue_window, text="Login", command=self.open_login_page)
        self.login_button.grid(row=1, column=3)

    def open_login_page(self):
        Login_Page(self.catalogue_window)  # open the login page (alrady defined as a top window)   







if __name__ == "__main__":
    root = tkinter.Tk()
    app = Catalogue_Page(root)
    root.mainloop()


    