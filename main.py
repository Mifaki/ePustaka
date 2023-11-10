from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

Window.size = (400, 800)

book_data = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "F. Scott Fitzgerald",
        "description": "Set in 1922, explores Jay Gatsby's life, wealth, love, and the American Dream."
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "Harper Lee",
        "description": "Classic exploring racial injustice and moral growth through Scout Finch and her father, Atticus Finch."
    },
    {
        "id": 3,
        "title": "1984",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "George Orwell",
        "description": "Dystopian novel following Winston Smith's rebellion against the Party's totalitarian regime."
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "Jane Austen",
        "description": "Romantic novel exploring complex relationships and social hierarchy through Elizabeth Bennet and Mr. Darcy."
    },
    {
        "id": 5,
        "title": "The Catcher in the Rye",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "J.D. Salinger",
        "description": "Novel featuring teenage angst, following Holden Caulfield's journey through identity, alienation, and loss."
    },
    {
        "id": 6,
        "title": "The Hobbit",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "J.R.R. Tolkien",
        "description": "Fantasy novel following Bilbo Baggins on an unexpected adventure with dragons, dwarves, elves, and a magical ring."
    },
]


screen = '''
ScreenManager:
    LoginScreen:
    HomeScreen:
    DetailScreen:
    HistoryScreen:
    AdminHomeScreen:
    NewBookScreen:
    EditBookScreen:
    EditFormScreen:

<LoginScreen>:
    id: login_layout 
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0

<HomeScreen>:
    id: home_layout 
    name: 'home'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0

<DetailScreen>:
    id: detail_layout 
    name: 'detail'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0

<HistoryScreen>:
    id: history_layout  
    name: 'history'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0
    
<NewBookScreen>:
    id: newBook_layout  
    name: 'newBook'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0

<EditBookScreen>:
    id: editBook_layout  
    name: 'editBook'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 0
'''


class BookCard(MDCard):
    book_info = DictProperty({})

    def __init__(self, book_info, **kwargs):
        super(BookCard, self).__init__(**kwargs)
        self.book_info = book_info

        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("400dp", "200dp")

        button_container = MDBoxLayout(orientation='vertical',adaptive_size=True, padding=10)
        button = MDRectangleFlatButton(
            text="View Details",
            size_hint_y=None,
            height="42dp",
            width=self.width,
            md_bg_color="blue",
            text_color="white",
        )
        button.bind(on_release=self.show_details)
        button_container.add_widget(button)
        button_container.pos_hint = { 'center_x': 0.5}

        short_desc = book_info['description'][:50]

        self.add_widget(
            Builder.load_string(
                f'''
BoxLayout:
    orientation: "vertical"
    padding: "20dp"
    spacing: "8dp"

    MDLabel:
        text: "{book_info['title']}"
        halign: "center"
        font_style: "H6"
    
    MDLabel:
    MDLabel:
    
    MDBoxLayout:
        orientation: "horizontal"
        width: "{Window.width}"

        MDLabel:
            text: "{book_info['status']}"
            theme_text_color: "Secondary"

        MDLabel:
            text: "{book_info['peminjaman']}"
            theme_text_color: "Secondary"
    
    MDLabel:

    MDLabel:
        text: "Author: {book_info['author']}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "{short_desc}"
        theme_text_color: "Secondary"
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
'''
            )
        )
        self.add_widget(button_container)

    def show_details(self, *args):
        app = MDApp.get_running_app()
        app.show_book_details(self.book_info)

class AdminBookCard(MDCard):
    book_info = DictProperty({})

    def __init__(self, book_info, **kwargs):
        super(AdminBookCard, self).__init__(**kwargs)
        self.book_info = book_info

        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("300dp", "200dp")

        button = Button(text="Edit", size_hint_y=None, height="40dp")
        button.bind(on_release=self.edit_book)

        self.add_widget(
            Builder.load_string(
                f'''
BoxLayout:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDLabel:
        text: "{book_info['title']}"
        halign: "center"
        font_style: "H6"

    MDLabel:
        text: "Status: {book_info['status']}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "Peminjaman: {book_info['peminjaman']}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "Author: {book_info['author']}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "{book_info['description']}"
        theme_text_color: "Secondary"
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
'''
            )
        )
        self.add_widget(button)

    def edit_book(self, *args):
        app = MDApp.get_running_app()
        edit_book_screen = app.root.get_screen("editBook")

        # Set the book_info for the EditBookScreen
        edit_book_screen.set_book_info(self.book_info)

        app.root.current = "editBook"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        main_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_height=True)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        label = MDLabel(text="ePustaka", halign='center', font_style="H3")

        button_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_width=True, adaptive_height=True, padding=50)
        button_layout.bind(minimum_width=button_layout.setter('width'))

        user_button = MDFillRoundFlatButton(text="Login as User", text_color="white", size_hint_y=None, height=50, width=80)
        user_button.bind(on_release=lambda instance: self.switch_to_screen("User"))
        admin_button = MDFillRoundFlatButton(text="Login as Admin", text_color="white", size_hint_y=None, height=50, width=80)
        admin_button.bind(on_release=lambda instance: self.switch_to_screen("Admin"))

        main_layout.add_widget(label)

        button_layout.add_widget(user_button)
        button_layout.add_widget(admin_button)

        button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.9}
        
        main_layout.add_widget(button_layout)

        main_layout.pos_hint = {'center_y': 0.5, 'center_x': 0.5}

        self.add_widget(main_layout)

    def switch_to_screen(self, role):
        if role == 'User':
            self.manager.current = 'home' 
        elif role == 'Admin':
            self.manager.current = 'admin_home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.home_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=10)

        search_bar = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=10,
            adaptive_height=True
        )
        self.search_textfield = MDTextField(id='search_bar', mode='rectangle', hint_text='Search')
        search_button = MDIconButton(icon="magnify")
        search_button.bind(on_release=self.trigger_search)

        search_bar.add_widget(self.search_textfield)
        search_bar.add_widget(search_button)
        self.home_layout.add_widget(search_bar)

        scroll = ScrollView(size_hint_y=None, height=Window.height, do_scroll_y=True, do_scroll_x=False)
        self.book_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.book_grid.bind(minimum_height=self.book_grid.setter('height'))
        scroll.add_widget(self.book_grid)

        self.home_layout.add_widget(scroll)
        self.add_widget(self.home_layout)

        for book in book_data:
            self.add_book_to_grid(book)

        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        history_nav_item = MDBottomNavigationItem(name='history_page', text='History', icon='history')
        logout_nav_item = MDBottomNavigationItem(name='logout', text='Logout', icon='logout')
        history_nav_item.bind(on_tab_press=self.switch_to_history_screen) 
        logout_nav_item.bind(on_tab_press=self.logout) 
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(history_nav_item)
        bottom_nav.add_widget(logout_nav_item)
        self.home_layout.add_widget(bottom_nav)

    def switch_to_history_screen(self, instance):
        self.manager.current = 'history'

    def logout(self, instance):
        self.manager.current = 'login'

    def clear_book_grid(self):
        self.book_grid.clear_widgets()

    def add_book_to_grid(self, book_info):
        self.book_grid.add_widget(BookCard(book_info))

    def on_search(self, instance, value):
        self.clear_book_grid()
        for book in book_data:
            if value.lower() in book['title'].lower():
                self.add_book_to_grid(book)

    def trigger_search(self, instance):
        self.on_search(self.search_textfield, self.search_textfield.text)
    
    def refresh_home_screen(self, book_title, new_status, new_peminjaman):
        for book in book_data:
            if book['title'] == book_title:
                book['status'] = new_status
                book['peminjaman'] = new_peminjaman

        self.clear_book_grid()
        for book in book_data:
            self.add_book_to_grid(book)
    
    def get_borrowed_books(self):
        borrowed_books = [book for book in book_data if book['peminjaman'] == 'Borrowed']
        return borrowed_books


class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.detail_layout = MDFloatLayout()

        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        back_button.pos_hint = {'x': 0, 'y': 0.9}
        self.detail_layout.add_widget(back_button)

        self.book_detail_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_height=True, padding=15)
        self.book_detail_layout.bind(minimum_height=self.book_detail_layout.setter('height'))
        self.book_detail_layout.pos_hint = { 'y': 0.5}

        self.detail_layout.add_widget(self.book_detail_layout)
        self.add_widget(self.detail_layout)

    def on_enter(self, *args):
        pass

    def go_back(self, instance):
        self.manager.current = 'home' 

    def borrow_or_return_book(self, instance, book_info):
        history_screen = self.manager.get_screen("history")
        if book_info['status'] == 'Available':
            book_info['status'] = 'Unavailable'
            book_info['peminjaman'] = 'Borrowed'
            instance.text = 'Return' 
            self.update_book_status(book_info['title'], 'Unavailable', 'Borrowed')
            self.show_book_details(book_info)
        elif book_info['status'] == 'Unavailable' and book_info['peminjaman'] == 'Borrowed':
            book_info['status'] = 'Available'
            book_info['peminjaman'] = 'Returned'
            instance.text = 'Borrow'  
            self.update_book_status(book_info['title'], 'Available', 'Returned')
            self.show_book_details(book_info)
            history_screen.history_grid.clear_widgets()

    def update_book_status(self, book_title, new_status, new_peminjaman):
        app = MDApp.get_running_app()
        app.root.get_screen("home").refresh_home_screen(book_title, new_status, new_peminjaman)

        for book in book_data:
            if book['title'] == book_title:
                book['status'] = new_status
                book['peminjaman'] = new_peminjaman

    def show_book_details(self, book_info):
        self.book_detail_layout.clear_widgets()

        for key, value in book_info.items():
            if(key == "id"): continue
            label = MDLabel(text=f"{key.capitalize()}: {value}", size_hint=(1, None), height=32)
            self.book_detail_layout.add_widget(label)

        borrow_button = MDRectangleFlatButton(
            text='Borrow' if book_info['status'] == 'Available' else 'Return',
            size_hint=(1, None),
            height=42,
            md_bg_color="blue",
            text_color="white"
        )

        borrow_button.bind(on_release=partial(self.borrow_or_return_book, book_info=book_info))
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(borrow_button)

        self.manager.current = 'detail'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.history_layout = MDBoxLayout(orientation='vertical', spacing=0)

        title = MDLabel(text="History", halign='center')
        self.history_layout.add_widget(title)

        scroll_view = ScrollView(size_hint_y=None, height=Window.height, do_scroll_y=True, do_scroll_x=False)
        self.history_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        scroll_view.add_widget(self.history_grid)

        self.history_layout.add_widget(scroll_view)

        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        history_nav_item = MDBottomNavigationItem(name='history_page', text='History', icon='history')
        logout_nav_item = MDBottomNavigationItem(name='logout', text='Logout', icon='logout')
        home_nav_item.bind(on_tab_press=self.switch_to_home_screen) 
        logout_nav_item.bind(on_tab_press=self.logout) 
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(history_nav_item)
        bottom_nav.add_widget(logout_nav_item)
        self.history_layout.add_widget(bottom_nav)

        self.add_widget(self.history_layout)

    def on_enter(self, *args):
        self.show_returned_books()
    
    def switch_to_home_screen(self, instance):
        self.manager.current = 'home'
    
    def logout(self, instance):
        self.manager.current = 'login'
    
    def clear_history_grid(self):
        self.history_grid.clear_widgets()

    def show_returned_books(self):
        self.history_grid.clear_widgets() 

        returned_books = self.get_returned_books()

        for book in returned_books:
            self.add_book_to_history(book)

    def add_book_to_history(self, book_info):
        self.history_grid.add_widget(BookCard(book_info))

    def get_returned_books(self):
        returned_books = [book for book in book_data if book['peminjaman'] == 'Returned']
        return returned_books

class AdminHomeScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminHomeScreen, self).__init__(**kwargs)
        self.admin_home_layout = MDBoxLayout(orientation='vertical', spacing=0)

        add_book_button = MDFlatButton(text="Add New Book", on_release=self.go_to_new_book)
        self.admin_home_layout.add_widget(add_book_button)

        scroll = ScrollView(size_hint_y=None, height=Window.height, do_scroll_y=True, do_scroll_x=False)
        self.book_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.book_grid.bind(minimum_height=self.book_grid.setter('height'))
        scroll.add_widget(self.book_grid)

        self.admin_home_layout.add_widget(scroll)

        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        logout_nav_item = MDBottomNavigationItem(name='logout', text='Logout', icon='logout')
        home_nav_item.bind(on_tab_press=self.switch_to_home_screen)
        logout_nav_item.bind(on_tab_press=self.logout)
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(logout_nav_item)
        self.admin_home_layout.add_widget(bottom_nav)

        self.add_widget(self.admin_home_layout)

        for book in book_data:
            self.add_book_to_grid(book)

    def on_enter(self, *args):
        admin_home_screen = self.manager.get_screen('admin_home')
        admin_home_screen.clear_book_grid()
        for book in book_data:
            admin_home_screen.add_book_to_grid(book)

    def switch_to_home_screen(self, instance):
        self.manager.current = 'home'
    
    def go_to_new_book(self, instance):
        self.manager.current = 'newBook'

    def logout(self, instance):
        self.manager.current = 'login'

    def clear_book_grid(self):
        self.book_grid.clear_widgets()

    def add_book_to_grid(self, book_info):
        self.book_grid.add_widget(AdminBookCard(book_info))

class NewBookScreen(Screen):
    def __init__(self, **kwargs):
        super(NewBookScreen, self).__init__(**kwargs)
        self.new_book_layout = MDBoxLayout(orientation='vertical', spacing=10)

        title_field = MDTextField(hint_text="Title")
        author_field = MDTextField(hint_text="Author")
        description_field = MDTextField(hint_text="Description")
        save_button = MDFlatButton(text="Save", on_release=self.add_new_book)

        self.new_book_layout.add_widget(title_field)
        self.new_book_layout.add_widget(author_field)
        self.new_book_layout.add_widget(description_field)
        self.new_book_layout.add_widget(save_button)

        self.add_widget(self.new_book_layout)

    def add_new_book(self, instance):
        title = self.new_book_layout.children[3].text
        author = self.new_book_layout.children[2].text
        description = self.new_book_layout.children[1].text

        # Generate the new book's ID by incrementing the last book's ID
        new_book_id = book_data[-1]['id'] + 1 if book_data else 1  # If book_data is empty, start with ID 1

        new_book = {
            "id": new_book_id,
            "title": title,
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": author,
            "description": description
        }

        # Add the new book to the book data
        book_data.append(new_book)

        # Clear existing book data in AdminHomeScreen
        admin_home_screen = self.manager.get_screen('admin_home')
        admin_home_screen.clear_book_grid()
        for book in book_data:
            admin_home_screen.add_book_to_grid(book)

        # Clear existing book data in HomeScreen
        home_screen = self.manager.get_screen('home')
        home_screen.clear_book_grid()
        for book in book_data:
            home_screen.add_book_to_grid(book)
        
        self.new_book_layout.children[3].text = ""
        self.new_book_layout.children[2].text = ""
        self.new_book_layout.children[1].text = ""

        self.manager.current = 'admin_home'

class EditBookScreen(Screen):
    def __init__(self, **kwargs):
        super(EditBookScreen, self).__init__(**kwargs)
        self.edit_layout = MDBoxLayout(orientation='vertical', spacing=10)
        self.book_info = {}
        
        self.dialog = None

        # Create and populate the fields with the book information
        self.title_field = MDTextField(hint_text="Title")
        self.author_field = MDTextField(hint_text="Author")
        self.description_field = MDTextField(hint_text="Description")
        self.status_field = MDTextField(hint_text="Status")
        self.peminjaman_field = MDTextField(hint_text="Peminjaman")
        delete_button = MDFlatButton(text="Delete", on_release=self.show_delete_confirmation)
        save_button = MDFlatButton(text="Save", on_release=self.save_changes)

        self.edit_layout.add_widget(self.title_field)
        self.edit_layout.add_widget(self.author_field)
        self.edit_layout.add_widget(self.description_field)
        self.edit_layout.add_widget(self.status_field)
        self.edit_layout.add_widget(self.peminjaman_field)
        self.edit_layout.add_widget(save_button)
        self.edit_layout.add_widget(delete_button)

        self.add_widget(self.edit_layout)
    
    def save_changes(self, instance):
        app = MDApp.get_running_app()

        
        new_title = self.title_field.text
        new_author = self.author_field.text
        new_description = self.description_field.text
        new_status = self.status_field.text
        new_peminjaman = self.peminjaman_field.text

        self.book_info['title'] = new_title
        self.book_info['author'] = new_author
        self.book_info['description'] = new_description
        self.book_info['status'] = new_status
        self.book_info['peminjaman'] = new_peminjaman

        for i, book in enumerate(book_data):
            if book['id'] == self.book_info['id']:
                book_data[i] = self.book_info
                break

        admin_home_screen = app.root.get_screen("admin_home")
        home_screen = app.root.get_screen("home")
        admin_home_screen.clear_book_grid()
        home_screen.clear_book_grid()

        for book in book_data:
            home_screen.add_book_to_grid(book)
            admin_home_screen.add_book_to_grid(book)

        app.root.current = "admin_home"
    
    def set_book_info(self, book_info):
        self.book_info = book_info

        self.title_field.text = self.book_info.get('title', '')
        self.author_field.text = self.book_info.get('author', '')
        self.description_field.text = self.book_info.get('description', '')
        self.status_field.text = self.book_info.get('status', '')
        self.peminjaman_field.text = self.book_info.get('peminjaman', '')

    def show_delete_confirmation(self, instance):
        self.dialog = MDDialog(
            text="Are you sure you want to delete this book?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=self.close_dialog),
                MDFlatButton(text="Delete", on_release=self.delete_book)
            ],
        )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def delete_book(self, instance):
        app = MDApp.get_running_app()
        app.root.get_screen("admin_home").clear_book_grid()
        app.root.get_screen("home").clear_book_grid()

        for book in book_data:
            if book == self.book_info:
                book_data.remove(book)
                break
        
        for book in book_data:
            app.root.get_screen("admin_home").add_book_to_grid(book)
            app.root.get_screen("home").add_book_to_grid(book)
        
        if self.dialog:
            self.dialog.dismiss()
        self.manager.current = "admin_home"
    

class ePustaka(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name="login")
        home_screen = HomeScreen(name="home")
        admin_home_screen = AdminHomeScreen(name="admin_home") 

        for book in book_data:
            home_screen.add_book_to_grid(book)
            admin_home_screen.add_book_to_grid(book) 

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(admin_home_screen)
        self.screen_manager.add_widget(DetailScreen(name="detail"))
        self.screen_manager.add_widget(HistoryScreen(name="history"))
        self.screen_manager.add_widget(NewBookScreen(name="newBook"))
        self.screen_manager.add_widget(EditBookScreen(name="editBook"))

        return self.screen_manager

    def on_search(self, instance, value):
        home_screen = self.root.get_screen('home')

        home_screen.clear_book_grid()

        for book in book_data:
            if value.lower() in book['title'].lower():
                home_screen.add_book_to_grid(book)

    def show_book_details(self, book_info):
        detail_screen = self.root.get_screen("detail")
        detail_screen.show_book_details(book_info)


if __name__ == "__main__":
    ePustaka().run()