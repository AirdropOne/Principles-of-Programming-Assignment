import tkinter
import sqlite3
from login_registration import Login_Page
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os
import cv2
from pyzbar.pyzbar import decode
from tkinter import filedialog



class Catalogue_Page:
    
    def __init__(self, root):
        self.catalogue_window = root
        self.catalogue_window.title("Catalogue Page")
        self.catalogue_window.geometry("535x830")

        self.infolabel = tkinter.Label(self.catalogue_window, text="Catalogue Page")
        
        self.search_var = tkinter.StringVar()
        
        self.search_label = tkinter.Label(self.catalogue_window, text="Search")
        self.search_label.grid(row=1, column=0)
        
        self.search_entry = tkinter.Entry(self.catalogue_window)
        self.search_entry.grid(row=1, column=1)
        
        self.search_button = tkinter.Button(self.catalogue_window, text="Search", command=self.search_products)
        self.search_button.grid(row=1, column=2)
        
        self.login_button = tkinter.Button(self.catalogue_window, text="Login", command=self.open_login_page)
        self.login_button.grid(row=1, column=3)
        
        self.category_var = tkinter.StringVar(value="All Categories")
        self.category_label = tkinter.Label(root, text="Filter by Category")
        self.category_label.grid(row=2, column=0)
        
        self.category_menu = ttk.Combobox(root, textvariable=self.category_var)
        self.category_menu['values'] = ("All Categories", "Bicycles", "Accessories")
        self.category_menu.grid(row=2, column=1)
        
        self.catalogue_frame = tkinter.Frame(self.catalogue_window)
        self.catalogue_frame.grid(row=3, column=0, columnspan=4)
        
        self.display_products(self.pull_products())
        
        self.scan_button = tkinter.Button(self.catalogue_window, text="Scan QR Code", command=self.scan_qr_code)
        self.scan_button.grid(row=4, column=0, columnspan=4, pady=10)



    def open_login_page(self):
        Login_Page(self.catalogue_window)
    
    
    
    def pull_products(self, search_query=None, category=None):
        connect = sqlite3.connect("bike_shop_DB.db")
        c = connect.cursor()
        
        query = "SELECT product_id, name, category, price, quantity FROM Product_Database"
        params = []
        
        if search_query or (category and category != "All Categories"):
            query += " WHERE"
        
        if search_query:
            query += " LOWER(name) LIKE ?"
            params.append(f'%{search_query}%')
            
        if category and category != "All Categories":
            if search_query:
                query += " AND"
            query += " Category=?"
            params.append(category)
        
        c.execute(query, params)
        rows = c.fetchall()
        
        connect.close()
        return rows



    def display_products(self, products):
        for widget in self.catalogue_frame.winfo_children():
            widget.destroy()
        
        for i, row in enumerate(products):
            product_frame = tkinter.Frame(self.catalogue_frame, borderwidth=1, relief="solid", padx=10, pady=10)
            product_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")
            
            name_label = tkinter.Label(product_frame, text=row[1], font=("Helvetica", 12, "bold"))
            name_label.pack(pady=2)
            
            category_label = tkinter.Label(product_frame, text=f"Category: {row[2]}", font=("Helvetica", 10))
            category_label.pack(pady=2)
            
            price_label = tkinter.Label(product_frame, text=f"Price: £{row[3]}")
            price_label.pack(pady=2)
            
            quantity_label = tkinter.Label(product_frame, text=f"Available: {row[4]}")
            quantity_label.pack(pady=2)
            
            purchase_button = tkinter.Button(product_frame, text="Purchase", command=self.not_logged_in)
            purchase_button.pack(pady=5)
            
            details_button = tkinter.Button(product_frame, text="Details", command=lambda name=row[1]: self.display_product_details(name))   
            details_button.pack(pady=5)
            
            
            



    def display_product_details(self, product_name):
        details = self.get_product_details(product_name)
        
        if details:
            detail_window = tkinter.Toplevel(self.catalogue_window)
            detail_window.title("Product Details")
            detail_window.geometry("300x200")
            
            name_label = tkinter.Label(detail_window, text=f"Name: {product_name}", font=("Helvetica", 12, "bold"))
            name_label.pack(pady=5)
            
            description_label = tkinter.Label(detail_window, text=f"For a detailed description please scan the QR Code")
            description_label.pack(pady=5)
            
            price_label = tkinter.Label(detail_window, text=f"Price: £{details[1]}")
            price_label.pack(pady=5)
            
            
            
            data = details[2]                                                               ## generate a qr code with the product id in it
            qr_code = qrcode.make(data, error_correction=qrcode.constants.ERROR_CORRECT_L)  ##error correction allows for more redundancy in the qr code (was needed for certain products)
            
            qr_file_path = f"qr_codes/{product_name}.png"                                   ## save the qr code as a png file named after the product in the qr_codes folder
            qr_code.save(qr_file_path)                                                      ##save it
            
            qr_image = Image.open(qr_file_path)
            self.qr_photo = ImageTk.PhotoImage(qr_image)                                    ##set image as an imageTk so tkinter can use it
            
            
            qr_label = tkinter.Label(detail_window, image=self.qr_photo)
            qr_label.pack(pady=5)
            
            
            
            
        else:
            messagebox.showinfo("Error", "No details available for this product")



    def get_product_details(self, product_name):    ## To get product details from the database
        connect = sqlite3.connect("bike_shop_DB.db")
        c = connect.cursor()
        
        c.execute("SELECT product_id, price, description FROM Product_Database WHERE name = ?", (product_name,))
        result = c.fetchone()
        
        connect.close()
        return result


    def search_products(self):
        search_query = self.search_entry.get().lower()
        selected_category = self.category_var.get()
        
        filtered_products = self.pull_products(search_query=search_query, category=selected_category)
        self.display_products(filtered_products)


    def scan_qr_code(self):
        qr_code_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        
        if qr_code_path:
            
            qr_code_image = cv2.imread(qr_code_path)
            detector = cv2.QRCodeDetector()
            
            retval, decoded_info, points = detector.detectAndDecode(qr_code_image)
            
            if retval:
                messagebox.showinfo("QR Code Scanned", f"Details: {retval}")
                self.display_product_details(retval)
            else:
                messagebox.showerror("Error", "Failed to scan the QR code.")





    def not_logged_in(self):
        messagebox.showinfo("Error", "You need to be logged in to purchase products")
        

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Catalogue_Page(root)
    root.mainloop()