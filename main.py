from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

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
        self.size_hint = (Window.width, None)
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

class ePustaka(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"

        def on_search(instance, value):
            layout.clear_widgets()
            for book in book_data:
                if value.lower() in book['title'].lower():
                    layout.add_widget(BookCard(book))

        search_bar = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=10,
            size_hint_y=None,
            height="48dp"
        )
        search_textfield = MDTextField(mode="rectangle", hint_text="Search", on_text=on_search)
        search_button = MDIconButton(icon="magnify", on_release=lambda x: on_search(search_textfield, search_textfield.text))
        search_bar.add_widget(search_textfield)
        search_bar.add_widget(search_button)

        layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for book in book_data:
            layout.add_widget(BookCard(book))
        scroll_view = ScrollView(
            size_hint=(1, None),
            size=(Window.width, Window.height + 48), 
            do_scroll_y=True,
            do_scroll_x=False
        )
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

        main_layout = MDBoxLayout(orientation="vertical", spacing=0)
        main_layout.add_widget(search_bar)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(bottom_navigation)

        return main_layout

ePustaka().run()