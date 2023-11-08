from kivy.lang import Builder
from kivy.properties import DictProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

Window.size = (400, 800)

book_data = [
        {
            "title": "The Great Gatsby",
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": "F. Scott Fitzgerald",
            "description": "A novel written by American author F. Scott Fitzgerald."
        },
        {
            "title": "To Kill a Mockingbird",
            "status": "Unavailable",
            "peminjaman": "Borrowed",
            "author": "Harper Lee",
            "description": "A classic novel by Harper Lee dealing with serious issues."
        },
        {
            "title": "1984",
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": "George Orwell",
            "description": "A dystopian social science fiction novel by George Orwell."
        },
        {
            "title": "Pride and Prejudice",
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": "Jane Austen",
            "description": "A romantic novel by Jane Austen."
        },
        {
            "title": "The Catcher in the Rye",
            "status": "Unavailable",
            "peminjaman": "Borrowed",
            "author": "J.D. Salinger",
            "description": "A novel by J.D. Salinger, featuring themes of teenage angst."
        },
        {
            "title": "The Hobbit",
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": "J.R.R. Tolkien",
            "description": "A fantasy novel by J.R.R. Tolkien, following the journey of Bilbo Baggins."
        }
]

screen = '''
ScreenManager:
    HomeScreen:
    DetailScreen:
    HistoryScreen:

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
'''


class BookCard(MDCard):
    book_info = DictProperty({})

    def __init__(self, book_info, **kwargs):
        super(BookCard, self).__init__(**kwargs)
        self.book_info = book_info

        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("300dp", "200dp")

        button = Button(text="View Details", size_hint_y=None, height="40dp")
        button.bind(on_release=self.show_details)

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

    def show_details(self, *args):
        app = MDApp.get_running_app()
        app.show_book_details(self.book_info)



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.home_layout = MDBoxLayout(orientation='vertical', spacing=0)

        self.search_bar = MDTextField(id='search_bar', mode='rectangle', hint_text='Search')
        search_button = MDIconButton(icon="magnify")
        search_button.bind(on_release=self.trigger_search)

        self.home_layout.add_widget(self.search_bar)
        self.home_layout.add_widget(search_button)

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
        history_nav_item.bind(on_tab_press=self.switch_to_history_screen)  # bind to switch screen
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(history_nav_item)
        self.home_layout.add_widget(bottom_nav)

    def switch_to_history_screen(self, instance):
        self.manager.current = 'history'

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
        self.on_search(self.search_bar, self.search_bar.text)
    
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
        self.detail_layout = MDBoxLayout(orientation='vertical', spacing=10)

        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        self.detail_layout.add_widget(back_button)

        scroll_view = ScrollView()
        self.book_detail_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.book_detail_grid.bind(minimum_height=self.book_detail_grid.setter('height'))
        scroll_view.add_widget(self.book_detail_grid)

        self.detail_layout.add_widget(scroll_view)
        self.add_widget(self.detail_layout)

    def on_enter(self, *args):
        pass

    def go_back(self, instance):
        self.manager.current = 'home' 

    def borrow_book(self, instance, book_info):
        if book_info['status'] == 'Available':
            book_info['status'] = 'Unavailable'
            book_info['peminjaman'] = 'Borrowed'
            instance.text = 'Borrowed'
            instance.disabled = True

            self.update_book_status(book_info['title'], 'Unavailable', 'Borrowed')
            self.show_book_details(book_info)
        else:
            instance.text = 'Unavailable'
            instance.disabled = True

    def update_book_status(self, book_title, new_status, new_peminjaman):

        app = MDApp.get_running_app()
        app.root.get_screen("home").refresh_home_screen(book_title, new_status, new_peminjaman)

        for book in book_data:
            if book['title'] == book_title:
                book['status'] = new_status
                book['peminjaman'] = new_peminjaman

    def show_book_details(self, book_info):
        self.book_detail_grid.clear_widgets()

        for key, value in book_info.items():
            label = MDLabel(text=f"{key.capitalize()}: {value}", size_hint=(1, None), height=40)
            self.book_detail_grid.add_widget(label)

        borrow_button = Button(
            text='Borrow' if book_info['status'] == 'Available' else 'Unavailable',
            size_hint=(1, None),
            height=40
        )

        if book_info['status'] == 'Unavailable':
            borrow_button.disabled = True

        borrow_button.bind(on_release=partial(self.borrow_book, book_info=book_info))
        self.book_detail_grid.add_widget(borrow_button)

        self.manager.current = 'detail'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.history_layout = MDBoxLayout(orientation='vertical', spacing=0)

        scroll_view = ScrollView()
        self.history_grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        scroll_view.add_widget(self.history_grid)

        self.history_layout.add_widget(scroll_view)

        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        home_nav_item.bind(on_tab_press=self.switch_to_home_screen)  # bind to switch screen
        history_nav_item = MDBottomNavigationItem(name='history_page', text='History', icon='history')
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(history_nav_item)

        self.history_layout.add_widget(bottom_nav)

        self.add_widget(self.history_layout)

    def on_enter(self, *args):
        self.show_borrowed_books()

    def show_borrowed_books(self):
        self.history_grid.clear_widgets() 

        borrowed_books = self.get_borrowed_books()

        for book in borrowed_books:
            self.add_book_to_history(book)

    def add_book_to_history(self, book_info):
        self.history_grid.add_widget(BookCard(book_info))

    def get_borrowed_books(self):
        home_screen = MDApp.get_running_app().root.get_screen("home")
        return home_screen.get_borrowed_books()

    def switch_to_home_screen(self, instance):
        self.manager.current = 'home'

class ePustaka(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()

        home_screen = HomeScreen(name="home")

        for book in book_data:
            home_screen.add_book_to_grid(book)

        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(DetailScreen(name="detail"))
        self.screen_manager.add_widget(HistoryScreen(name="history"))

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