from catalogue_page import Catalogue_Page
import tkinter









class Admin_Catalogue_Page(Catalogue_Page):
    def __init__(self, root):
        super().__init__(root)
        self.catalogue_window.title("Admin Catalogue Page")
    








class User_Catalogue_Page(Catalogue_Page):
    def __init__(self, root):
        super().__init__(root)
        self.catalogue_window.title("User Catalogue Page")






