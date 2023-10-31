from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

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

class BookCard(MDCard):
    def __init__(self, book_info, **kwargs):
        super(BookCard, self).__init__(**kwargs)
        title = book_info["title"]
        status = book_info["status"]
        peminjaman = book_info["peminjaman"]
        author = book_info["author"]
        description = book_info["description"]
        
        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("300dp", "200dp")
        
        self.add_widget(Builder.load_string(
            f'''
BoxLayout:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    MDLabel:
        text: "{title}"
        halign: "center"
        font_style: "H6"

    MDLabel:
        text: "Status: {status}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "Peminjaman: {peminjaman}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "Author: {author}"
        theme_text_color: "Secondary"

    MDLabel:
        text: "{description}"
        theme_text_color: "Secondary"
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
'''
        ))

class Test(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"

        scroll_view = ScrollView()
        layout = Builder.load_string('''
BoxLayout:
    orientation: "vertical"
    spacing: "8dp"
    padding: "8dp"
''')

        for book in book_data:
            layout.add_widget(BookCard(book))

        scroll_view.add_widget(layout)

        bottom_navigation = MDBottomNavigation(
            MDBottomNavigationItem(
                name="home_page",
                text="Home",
                icon="home"
            ),
            MDBottomNavigationItem(
                name="history_page",
                text="History",
                icon="history"
            )
        )

        layout.add_widget(bottom_navigation)

        return scroll_view

Test().run()
