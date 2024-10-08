import tkinter
import mysql.connector
import sqlite3
from tkinter import messagebox
import bcrypt                       ## Auto handles salting, widely recomended - research and reference



## Object oriented approach, greater efficiency, more scalable - maybe make in C++ for better scalability as future concept since its better at that?


class   Login_Page():


    def __init__(self, root):
        self.root=root                                                                                ## with root = tkinter, we neeed to pass route through 
        self.login_window=self.root                                                                   ## Creating the main page
        self.login_window.title("Login_page")                                                         ## What its called
        self.login_window.geometry("400x300")                                                         ## Its size
        padd=20                                                             
        self.login_window["padx"]=padd
        self.info_label=tkinter.Label(self.login_window, text ="Login Page")                          ## Labeling the top left
        self.info_label.grid(row=0, column=0)                                                         ## Defining the location on a grid



        self.info_email=tkinter.Label(self.login_window, text ="Email")                               ## Labeling the Email text
        self.info_email.grid(row=1, column=0)                                                         ## Placing that text within the grid

        self.email_entry=tkinter.StringVar()                                                          ## Storing the entry as a string - WHY???? - SQL sanitisation???

        self.email_entry=tkinter.Entry(self.login_window, textvariable=self.email_entry)              ## Assigning a name to en entry field           and            Specifying we want to use tkinters .StringVar as the text type for this field
        self.email_entry.grid(row=1, column=1)                                                        ## Placing that entry field in the grid



        self.info_password=tkinter.Label(self.login_window, text = "Password")                        ## Repeating for password - Remember we dont want to repeat code? Generalise thi code so instead of password or email, just "input" ?
        self.info_password.grid(row=2, column=0)                                                      ## ''

        self.password_entry=tkinter.StringVar()                                                       ## ''

        self.password_entry=tkinter.Entry(self.login_window, textvariable=self.password_entry, show="*")        ## ''    and show="*" shows inputs as * for (for password protection)
        self.password_entry.grid(row=2, column=1)                                                     ## ''


                            

        self.login_button=tkinter.Button(self.login_window, text="Login", command=self.login)                           ## Assigning a name and adding text login button        and       initiate the login function
        self.login_button.grid(row=3, column=1, pady=5)                                                                 ## Placing the button in the grid

        self.create_account_button=tkinter.Button(self.login_window, text="Create Account", command=self.open_registration_window)                ## Assigning a name and adding text to create accountbutton       and      initiate page traversal??
        self.create_account_button.grid(row=4, column=1, pady=5)                                                        ## Placing the button in the grid

    def verify_password(self, password, stored_password):                                           ##checks the password input, hashes it with crype then compares to the stored password on the database (defined the login function)
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)

    def login(self):
        email = self.email_entry.get()                                                                  ## assigning a name to the function of pulling the values that have been input into the email entry field
        password = self.password_entry.get()                                                            ## ''
    
        connect = sqlite3.connect("practise_DB.db")                                                 ## assigning a name to the funtion of connecting to my practise datatbase         and       remember the .db
        c = connect.cursor()                                                                        ## assigning a name to the function of making a request to the connected database

        c.execute("SELECT Password FROM Login_Database WHERE Email=?", (email,))                ## "?" work as a placeholder for the tuple values- include the comma since its a tuple. Pulling the stored password to compare against hashed password from field entry
    
        row=c.fetchone()                                                                            ## goes one by one along a row looking for matching email
        if row:                                                                                 ## if a matching email was found
            stored_password = row[0]                                                            ## pulls the stored password from the database that correlates to the matching email
            if self.verify_password(password, stored_password):                                 ## if verify password passes its check, login success
                messagebox.showinfo("Info", "Login Success")
            else: 
                messagebox.showinfo("Info", "Incorrect Password")                               ## Else the password didnt correlate to the matching emails
            
        else:
            messagebox.showinfo("Info", "Login Failed")                                         ## Else there wasnt a stored email matching the one put in the field


    def open_registration_window(self):
        Registration_Page(self.root)                        ## Pass the root over to the registration page



class Registration_Page():

    def __init__(self, root):
        self.root=root
        self.reg_window=tkinter.Toplevel(root) 
        self.reg_window.title("Registration Page")
        self.reg_window.geometry("400x300")
        padd=20
        self.reg_window["padx"]=padd
        self.info_label=tkinter.Label(self.reg_window, text ="Registration Page")
        self.info_label.grid(row=0, column=0)

        self.email_label=tkinter.Label(self.reg_window, text ="Email")
        self.email_label.grid(row=1, column=0)

        self.email_reg=tkinter.StringVar()

        self.email_reg=tkinter.Entry(self.reg_window, textvariable=self.email_reg)
        self.email_reg.grid(row=1, column=1)

        self.password_label=tkinter.Label(self.reg_window, text="Password")
        self.password_label.grid(row=2, column=0)

        self.password_reg=tkinter.StringVar()

        self.password_reg=tkinter.Entry(self.reg_window, textvariable=self.password_reg)
        self.password_reg.grid(row=2, column=1)


        self.register_button=tkinter.Button(self.reg_window, text="Register", command=self.register)
        self.register_button.grid(row=3, column=1, pady=5)


        self.back_to_login_button=tkinter.Button(self.reg_window, text="Back to Login", command=self.back_to_login)               ## button for returning to login page and destroying instance of registration page
        self.back_to_login_button.grid(row=4, column=1, pady=5)



    def hash_password(self, password):                                          ## Uses bcrypt to hash the password input
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())        ## takes the password and encodes it using 'utf-8' to turn the string into bytes that bcrypy can encode, then salts for added security against rainbow tables. (research and reference) why use utf and bcrypt?

    def register(self):
        email = self.email_reg.get()
        password = self.password_reg.get() 
        hashed_password = self.hash_password(password)


        connect = sqlite3.connect("practise_DB.db")
        c = connect.cursor()

        c.execute("SELECT * FROM Login_Database WHERE Email=?" , (email,))                ## check if email already exists in database ## When using placeholders (?), the second argument must always be a tuple, even if it's a single value. add comma
        row = c.fetchone()                                                                ##

        if row:
            messagebox.showinfo("Error", "Email already exists")                          ## If email was fetched, it already exists and returns this message
        else:


            c.execute("INSERT INTO Login_Database (Email, Password) VALUES (?, ?)", (email, hashed_password))     ## Establish the touple paired to the placeholder outside of the sql query
            connect.commit()                                                                    ## Commits the change to the database
            messagebox.showinfo("Info", "Account Created")

    def back_to_login(self):                    

        self.reg_window.destroy()           ## destroy registration instance
                


    




if __name__ == "__main__":
    root = tkinter.Tk()
    app = Login_Page(root)
    root.mainloop()



## Need to add a back function from the register page to the login page
