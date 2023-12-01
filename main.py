# Import dari functools
from functools import partial

#import dari kivy
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

# Import dari kivymd
from kivymd.app import MDApp
from kivymd.uix.button import (
    MDFlatButton,
    MDFillRoundFlatButton,
    MDIconButton,
    MDRectangleFlatButton,
    MDFloatingActionButton,
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import (
    MDBottomNavigation,
    MDBottomNavigationItem,
)

#Deklarasi ukuran window
Window.size = (400, 800)

# Data dummy untuk tampilan awal
book_data = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "F. Scott Fitzgerald",
        "description": "Set in 1922, explores Jay Gatsby's life, wealth, love, and the American Dream.",
        "jumlah": 1,
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "Harper Lee",
        "description": "Classic exploring racial injustice and moral growth through Scout Finch and her father, Atticus Finch.",
        "jumlah": 2,
    },
    {
        "id": 3,
        "title": "1984",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "George Orwell",
        "description": "Dystopian novel following Winston Smith's rebellion against the Party's totalitarian regime.",
        "jumlah": 3,
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "Jane Austen",
        "description": "Romantic novel exploring complex relationships and social hierarchy through Elizabeth Bennet and Mr. Darcy.",
        "jumlah": 2,
    },
    {
        "id": 5,
        "title": "The Catcher in the Rye",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "J.D. Salinger",
        "description": "Novel featuring teenage angst, following Holden Caulfield's journey through identity, alienation, and loss.",
        "jumlah": 1,
    },
    {
        "id": 6,
        "title": "The Hobbit",
        "status": "Available",
        "peminjaman": "Not borrowed",
        "author": "J.R.R. Tolkien",
        "description": "Fantasy novel following Bilbo Baggins on an unexpected adventure with dragons, dwarves, elves, and a magical ring.",
        "jumlah": 2,
    },
]

# String KivyMD untuk definisi screen
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

# Kelas BookCard untuk menampilkan kartu buku pada main screen (user).
class BookCard(MDCard):
    def __init__(self, book_info, **kwargs):
        super(BookCard, self).__init__(**kwargs)
        self.book_info = book_info

        # Konfigurasi tata letak dan tampilan kartu buku.
        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("400dp", "200dp")

        # Kontainer untuk tombol "View Details".
        button_container = MDBoxLayout(orientation='vertical',adaptive_size=True, padding=10)

        # Tombol "View details"
        button = MDRectangleFlatButton(
            text="View Details",
            size_hint_y=None,
            height="42dp",
            width=self.width,
            md_bg_color="blue",
            text_color="white",
        )
        # Menambahkan fungsi "show details" pada tombol "View Details"
        button.bind(on_release=self.show_details)

        # Menambahkan tombol kedalam kontainer
        button_container.add_widget(button)

        # Membuat kontainer pada posisi tengah terhadap sumbu x
        button_container.pos_hint = { 'center_x': 0.5}

        # Desckripsi singkat dengan mengambil 50 karakter pertama dari deskripsi
        short_desc = book_info['description'][:50]

        # Menambahkan widget dengan memuat string KivyMD untuk layout kartu buku.
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
        # Menambhkan kontainer kedalam layout
        self.add_widget(button_container)

    # Mendaklarasikan fungsi "show_details"
    def show_details(self, *args):

        # Mendapatkan instance aplikasi (MDApp) yang sedang berjalan.
        app = MDApp.get_running_app()

        # Memanggil metode show_book_details pada instance aplikasi untuk menampilkan rincian buku.
        app.show_book_details(self.book_info)

# Kelas AdminBookCard untuk menampilkan kartu buku dengan opsi pengeditan pada admin.
class AdminBookCard(MDCard):
    def __init__(self, book_info, **kwargs):
        super(AdminBookCard, self).__init__(**kwargs)
        self.book_info = book_info

        # Konfigurasi tata letak dan tampilan kartu buku.
        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = ("400dp", "200dp")

        # Kontainer untuk tombol "Edit Book Details".
        button_container = MDBoxLayout(orientation='vertical',adaptive_size=True, padding=10)

        # Tombol "Edit Book Details"
        button = MDRectangleFlatButton(
            text="Edit Book Details",
            size_hint_y=None,
            height="42dp",
            width=self.width,
            md_bg_color="blue",
            text_color="white",
        )

        # Menambahkan fungsi "edit_book" pada tombol "Edit Book Details"
        button.bind(on_release=self.edit_book)

        # Menambahkan tombol kedalam kontainer
        button_container.add_widget(button)

        # Membuat kontainer pada posisi tengah terhadap sumbu x
        button_container.pos_hint = { 'center_x': 0.5}

        # Desckripsi singkat dengan mengambil 50 karakter pertama dari deskripsi
        short_desc = book_info['description'][:50]
        
        # Menambahkan widget dengan memuat string KivyMD untuk layout kartu buku.
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
        # Menambhkan kontainer kedalam layout
        self.add_widget(button_container)

    def edit_book(self, *args):
        # Mendapatkan instance aplikasi (MDApp) yang sedang berjalan.
        app = MDApp.get_running_app()
        # Mendapatkan instance layar "editBook" dari aplikasi.
        edit_book_screen = app.root.get_screen("editBook")
        # Mengatur informasi buku pada layar "editBook".
        edit_book_screen.set_book_info(self.book_info)
        # Mengganti layar saat ini dengan layar "editBook".
        app.root.current = "editBook"

# Kelas LoginScreen untuk halaman Login
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Mendaklarasikan main_layout menggunakan MDBoxLayout.
        main_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_height=True)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Menambahkan label "BacaCepat" ke main_layout.
        label = MDLabel(text="BacaCepat", halign='center', font_style="H3")
        main_layout.add_widget(label)

        # Mendaklarasikan button_layout menggunakan MDBoxLayout.
        button_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_width=True, adaptive_height=True, padding=50)
        button_layout.bind(minimum_width=button_layout.setter('width'))

        # Membuat tombol "Login as User" dengan fungsi panggilan kembali untuk beralih ke screen "home".
        user_button = MDFillRoundFlatButton(text="Login as User", text_color="white", size_hint_y=None, height=50, width=80)
        user_button.bind(on_release=lambda instance: self.switch_to_screen("User"))

        # Membuat tombol "Login as Admin" dengan fungsi panggilan kembali untuk beralih ke screen "admin_home".
        admin_button = MDFillRoundFlatButton(text="Login as Admin", text_color="white", size_hint_y=None, height=50, width=80)
        admin_button.bind(on_release=lambda instance: self.switch_to_screen("Admin"))

        # Menambahkan tombol ke button_layout.
        button_layout.add_widget(user_button)
        button_layout.add_widget(admin_button)

        # Menetapkan posisi button_layout.
        button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.9}

        # Menambahkan button_layout ke main_layout.
        main_layout.add_widget(button_layout)

        # Menetapkan posisi main_layout.
        main_layout.pos_hint = {'center_y': 0.5, 'center_x': 0.5}

        # Menambahkan main_layout ke screen.
        self.add_widget(main_layout)

    # Fungsi untuk beralih screen berdasarkan role yang diberikan
    def switch_to_screen(self, role):
        # Memeriksa peran dan beralih ke screen yang sesuai.
        if role == 'User':
            self.manager.current = 'home' 
        elif role == 'Admin':
            self.manager.current = 'admin_home'

# Kelas HomeScreen untuk menmpilkan screen home
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Mendefinisikan home_layout menggunakan MDBoxLayout.
        self.home_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=10)

        # Membuat search_bar menggunakan MDBoxLayout.
        search_bar = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=10,
            adaptive_height=True
        )

        # Membuat input field untuk pencarian.
        self.search_textfield = MDTextField(id='search_bar', mode='rectangle', hint_text='Search')

        # Membuat tombol pencarian.
        search_button = MDIconButton(icon="magnify")
        search_button.bind(on_release=self.trigger_search)

        # Menambahkan input field dan tombol pencarian ke search_bar.
        search_bar.add_widget(self.search_textfield)
        search_bar.add_widget(search_button)
        self.home_layout.add_widget(search_bar)

        # Membuat area scroll menggunakan ScrollView.
        scroll = ScrollView(size_hint_y=None, height=Window.height, do_scroll_y=True, do_scroll_x=False)

        # Membuat grid buku menggunakan GridLayout.
        self.book_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.book_grid.bind(minimum_height=self.book_grid.setter('height'))

        # Menambahkan grid buku ke area scroll.
        scroll.add_widget(self.book_grid)

        # Menambahkan area scroll ke home_layout.
        self.home_layout.add_widget(scroll)

        # Menambahkan home_layout ke layar.
        self.add_widget(self.home_layout)

        # Menambahkan setiap buku ke dalam grid.
        for book in book_data:
            self.add_book_to_grid(book)

        # Membuat navigasi bawah menggunakan MDBottomNavigation.
        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        history_nav_item = MDBottomNavigationItem(name='history_page', text='History', icon='history')
        logout_nav_item = MDBottomNavigationItem(name='logout', text='Logout', icon='logout')

        # Menghubungkan tombol dengan fungsi switch_to_history_screen dan logout.
        history_nav_item.bind(on_tab_press=self.switch_to_history_screen)
        logout_nav_item.bind(on_tab_press=self.logout)

        # Menambahkan item navigasi ke navigasi bawah.
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(history_nav_item)
        bottom_nav.add_widget(logout_nav_item)

        # Menambahkan navigasi bawah ke home_layout.
        self.home_layout.add_widget(bottom_nav)

    def switch_to_history_screen(self, instance):
        # Beralih ke history screen.
        self.manager.current = 'history'

    def logout(self, instance):
        # Beralih ke login screen.
        self.manager.current = 'login'

    def clear_book_grid(self):
        # Menghapus semua widget dari grid buku.
        self.book_grid.clear_widgets()

    def add_book_to_grid(self, book_info):
        # Menambahkan widget Bookcard ke dalam grid buku.
        self.book_grid.add_widget(BookCard(book_info))

    def on_search(self, instance, value):
        # Membersihkan grid buku dan menambahkan buku yang cocok dengan hasil pencarian.
        self.clear_book_grid()
        for book in book_data:
            if value.lower() in book['title'].lower():
                self.add_book_to_grid(book)

    def trigger_search(self, instance):
        # Memulai pencarian berdasarkan teks yang dimasukkan.
        self.on_search(self.search_textfield, self.search_textfield.text)

    def refresh_home_screen(self, book_title, new_status, new_peminjaman):
        # Memperbarui status dan peminjaman buku di layar utama.
        for book in book_data:
            if book['title'] == book_title:
                book['status'] = new_status
                book['peminjaman'] = new_peminjaman

        # Membersihkan grid buku dan menambahkan buku yang diperbarui.
        self.clear_book_grid()
        for book in book_data:
            self.add_book_to_grid(book)

    def get_borrowed_books(self):
        # Mengembalikan daftar buku yang dipinjam.
        borrowed_books = [book for book in book_data if book['peminjaman'] == 'Borrowed']
        return borrowed_books


# Kelas DetailScreen untuk menampilkan screen detail dari buku
class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)

        # Membuat detail_layout menggunakan MDFloatLayout.
        self.detail_layout = MDFloatLayout()

        # Membuat tombol kembali menggunakan MDIconButton.
        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        back_button.pos_hint = {'x': 0, 'y': 0.9}

        # Menambahkan tombok kembali kedalam detail_layout
        self.detail_layout.add_widget(back_button)

        # Membuat book_detail_layout menggunakan MDBoxLayout.
        self.book_detail_layout = MDBoxLayout(orientation='vertical', spacing=20, adaptive_height=True, padding=15)
        self.book_detail_layout.bind(minimum_height=self.book_detail_layout.setter('height'))
        self.book_detail_layout.pos_hint = {'y': 0.5}

        # Menambahkan book_detail_layout ke detail_layout.
        self.detail_layout.add_widget(self.book_detail_layout)
        self.add_widget(self.detail_layout)

    def on_enter(self, *args):
        pass
    
    # Membuat fungsi go_back
    def go_back(self, instance):
        # Kembali ke home screen.
        self.manager.current = 'home'

    # Membuat fungsi borrow_or_return_book
    def borrow_or_return_book(self, instance, book_info):
        # Mendapatkan instance dari layar sejarah.
        history_screen = self.manager.get_screen("history")

        home_screen = self.manager.get_screen("home")

        # Memeriksa status buku dan melakukan tindakan yang sesuai.
        if book_info['status'] == 'Available' and book_info['peminjaman'] != 'Borrowed':
            
            # Kurangi jumlah buku.
            self.update_qty(book_info['title'], -1)

            if book_info['jumlah'] <= 0:
                book_info['status'] = 'Unavailable'


            # Ubah teks tombol menjadi 'Return'.
            instance.text = 'Return'

            # Ubah peminjaman menjadi 'Borrowed'.
            book_info['peminjaman'] = 'Borrowed'

        elif book_info['peminjaman'] == 'Borrowed':
            # Tambah jumlah buku.
            self.update_qty(book_info['title'], 1)

            if book_info['jumlah'] > 0:
                book_info['status'] = 'Available'

            # Ubah status menjadi "Available" dan peminjaman menjadi "Returned".
            book_info['peminjaman'] = 'Returned'

            # Ubah teks tombol menjadi 'Borrow'.
            instance.text = 'Borrow'


            history_screen.history_grid.clear_widgets()

        # Tampilkan kembali detail buku.
        self.show_book_details(book_info)

        home_screen.refresh_home_screen(book_info['title'], book_info['status'], book_info['peminjaman'])

    def update_qty(self, book_title, change):
        # Memperbarui jumlah buku.
        for book in book_data:
            if book['title'] == book_title:
                book['jumlah'] += change

    # Memperbarui status buku di home screen.
    def show_book_details(self, book_info):
        # Menghapus semua widget dari book_detail_layout.
        self.book_detail_layout.clear_widgets()
        self.book_detail_layout.pos_hint = {'top': 0.9}

        # Menambahkan label untuk setiap detail buku ke dalam tata letak.
        for key, value in book_info.items():
            if key == "id":
                continue
            label = MDLabel(text=f"{key.capitalize()}: {value}", size_hint=(1, None), height=32)
            self.book_detail_layout.add_widget(label)

        # Membuat tombol pinjam atau kembalikan buku.
        borrow_button = MDRectangleFlatButton(
            text='Borrow' if book_info['peminjaman'] == 'Not Borrowed' or book_info['peminjaman'] == 'Returned' else 'Return',
            size_hint=(1, None),
            height=42,
            md_bg_color="blue",
            text_color="white"
        )

        # Menghubungkan fungsi untuk menangani acara tombol.
        borrow_button.bind(on_release=partial(self.borrow_or_return_book, book_info=book_info))

        # Menambahkan tombol ke dalam tata letak.
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(Label())
        self.book_detail_layout.add_widget(borrow_button)

        # Beralih ke layar detail.
        self.manager.current = 'detail'

# Kelas HistoryScreen untuk menampilkan Screen History.
class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # Membuat history_layout menggunakan MDBoxLayout.
        self.history_layout = MDBoxLayout(orientation='vertical', spacing=0)

        # Menambahkan label judul ke dalam history_layout.
        title = MDLabel(text="History", halign='center')
        self.history_layout.add_widget(title)

        # Membuat ScrollView untuk memungkinkan scroll di dalam GridLayout.
        scroll_view = ScrollView(size_hint_y=None, height=Window.height, do_scroll_y=True, do_scroll_x=False)
        self.history_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        scroll_view.add_widget(self.history_grid)

        # Menambahkan ScrollView ke dalam history_layout.
        self.history_layout.add_widget(scroll_view)

        # Membuat bottom navigation untuk menu navigasi.
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

        # Menambahkan history_layout ke dalam Screen.
        self.add_widget(self.history_layout)

    # Membuat fungsi on_enter yang akan dieksekusi saat masuk kedalam screen
    def on_enter(self, *args):
        # Menampilkan buku yang sudah dikembalikan saat masuk ke layar.
        self.show_returned_books()

    # Membuat fungsi switch_to_home_screen
    def switch_to_home_screen(self, instance):
        # Berpindah ke layar home saat item navigasi home dipilih.
        self.manager.current = 'home'
    
    # Membuat fungsi logout
    def logout(self, instance):
        # Berpindah ke layar login saat item navigasi logout dipilih.
        self.manager.current = 'login'
    
    # Membuat fungsi clear_history_grid
    def clear_history_grid(self):
        # Menghapus semua widget di dalam history_grid.
        self.history_grid.clear_widgets()

    # Membuat fungsi show_returned_books
    def show_returned_books(self):
        # Menghapus semua widget di dalam history_grid.
        self.history_grid.clear_widgets() 

        # Mendapatkan buku yang sudah dikembalikan.
        returned_books = self.get_returned_books()

        # Menambahkan setiap buku yang sudah dikembalikan ke dalam history_grid.
        for book in returned_books:
            self.add_book_to_history(book)

    # Membuat fungsi add_book_to_history
    def add_book_to_history(self, book_info):
        # Menambahkan kartu buku ke dalam history_grid.
        self.history_grid.add_widget(BookCard(book_info))

    # Membuat fungsi get_returned_book
    def get_returned_books(self):
        # Mendapatkan daftar buku yang sudah dikembalikan.
        returned_books = [book for book in book_data if book['peminjaman'] == 'Returned']
        return returned_books

# Kelas AdminHomeScreen untuk menampilkan Screen Home Admin.
class AdminHomeScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminHomeScreen, self).__init__(**kwargs)
        self.admin_home_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=10)

        # Membuat ScrollView untuk memungkinkan scroll di dalam GridLayout.
        scroll = ScrollView(size_hint_y=None, height=Window.height + 42, do_scroll_y=True, do_scroll_x=False)
        self.book_grid = GridLayout(cols=1, spacing=8, size_hint=(None, None), size=(Window.width, 0))
        self.book_grid.bind(minimum_height=self.book_grid.setter('height'))
        scroll.add_widget(self.book_grid)

        # Menambahkan ScrollView ke dalam admin_home_layout.
        self.admin_home_layout.add_widget(scroll)

        # Membuat tombol tambah buku dengan MDFloatingActionButton.
        add_book_button = MDFloatingActionButton(icon="plus", on_release=self.go_to_new_book, padding=5)
        add_book_button.pos_hint = {'right': 1.0, 'y': 0.3}
        self.admin_home_layout.add_widget(add_book_button)

        # Membuat bottom navigation untuk menu navigasi.
        bottom_nav = MDBottomNavigation()
        home_nav_item = MDBottomNavigationItem(name='home_page', text='Home', icon='home')
        logout_nav_item = MDBottomNavigationItem(name='logout', text='Logout', icon='logout')
        home_nav_item.bind(on_tab_press=self.switch_to_home_screen)
        logout_nav_item.bind(on_tab_press=self.logout)
        bottom_nav.add_widget(home_nav_item)
        bottom_nav.add_widget(logout_nav_item)
        self.admin_home_layout.add_widget(bottom_nav)

        # Menambahkan admin_home_layout ke dalam Screen.
        self.add_widget(self.admin_home_layout)

        # Menambahkan buku-buku yang sudah ada ke dalam grid.
        for book in book_data:
            self.add_book_to_grid(book)

    # Membuat fungsi on_enter yang akan dieksekusi saat masuk ke dalam screen,
    def on_enter(self, *args):
        # Memperbarui tampilan grid setiap kali masuk ke layar.
        admin_home_screen = self.manager.get_screen('admin_home')
        admin_home_screen.clear_book_grid()
        for book in book_data:
            admin_home_screen.add_book_to_grid(book)

    # Membuat fungsi switch to home screen.
    def switch_to_home_screen(self, instance):
        self.manager.current = 'admin_home'

    # Membuat fungsi go_to_new_book
    def go_to_new_book(self, instance):
        self.manager.current = 'newBook'

    # Membuat fungsi logout
    def logout(self, instance):
        self.manager.current = 'login'

    # Membuat fungsi clear_book_grid
    def clear_book_grid(self):
        self.book_grid.clear_widgets()

    # Membuat fungsi add_book_to_grid
    def add_book_to_grid(self, book_info):
        self.book_grid.add_widget(AdminBookCard(book_info))

# Kelas NewBookScreen untuk menampilkan screen buku baru.
class NewBookScreen(Screen):
    def __init__(self, **kwargs):
        super(NewBookScreen, self).__init__(**kwargs)
        
        # Membuat new_book_layout menggunakan MDBoxLayout.
        self.new_book_layout = MDBoxLayout(orientation='vertical', spacing=10, adaptive_height=True, padding=10)
        self.new_book_layout.pos_hint = {'top': 1}

        # Membuat tombol kembali menggunakan MDIconButton.
        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        self.new_book_layout.add_widget(back_button)

        # Membuat field input menggunakan MDTextField.
        title_field = MDTextField(hint_text="Title")
        author_field = MDTextField(hint_text="Author")
        description_field = MDTextField(hint_text="Description")
        jumlah_field = MDTextField(hint_text="Jumlah")
        
        # Membuat tombol simpan menggunakan MDRectangleFlatButton.
        save_button = MDRectangleFlatButton(
            text="Save",
            md_bg_color="blue",
            text_color="white",
            size_hint=(1, None),
            height=42,
            on_release=self.add_new_book
        )

        # Menambahkan elemen-elemen ke dalam new_book_layout.
        self.new_book_layout.add_widget(title_field)
        self.new_book_layout.add_widget(author_field)
        self.new_book_layout.add_widget(description_field)
        self.new_book_layout.add_widget(jumlah_field)
        self.new_book_layout.add_widget(save_button)

        # Menambahkan new_book_layout ke dalam Screen.
        self.add_widget(self.new_book_layout)

    # Membuat Fungsi go_back.
    def go_back(self, instance):
        self.manager.current = "admin_home"

    # Membuat Fungsi add_new_book.
    def add_new_book(self, instance):
        # Mendapatkan nilai dari field input.
        title = self.new_book_layout.children[4].text
        author = self.new_book_layout.children[3].text
        description = self.new_book_layout.children[2].text
        jumlah = self.new_book_layout.children[1].text

        # Menentukan ID untuk buku baru.
        new_book_id = book_data[-1]['id'] + 1 if book_data else 1 

        # Membuat data buku baru.
        new_book = {
            "id": new_book_id,
            "title": title,
            "status": "Available",
            "peminjaman": "Not borrowed",
            "author": author,
            "description": description,
            "jumlah": int(jumlah)
        }

        # Menambahkan buku baru ke dalam daftar buku.
        book_data.append(new_book)

        # Mendapatkan instance dari layar admin_home.
        admin_home_screen = self.manager.get_screen('admin_home')

        # Menghapus dan menambahkan ulang grid buku di screen admin_home.
        admin_home_screen.clear_book_grid()
        for book in book_data:
            admin_home_screen.add_book_to_grid(book)

        # Mendapatkan instance dari screen home.
        home_screen = self.manager.get_screen('home')

        # Menghapus dan menambahkan ulang grid buku di screen home.
        home_screen.clear_book_grid()
        for book in book_data:
            home_screen.add_book_to_grid(book)
        
        # Mengosongkan field input setelah buku ditambahkan.
        self.new_book_layout.children[4].text = ""
        self.new_book_layout.children[3].text = ""
        self.new_book_layout.children[2].text = ""
        self.new_book_layout.children[1].text = ""

        # Beralih ke screen admin_home.
        self.manager.current = 'admin_home'

# Kelas EditBookScreen untuk menampilkan screen edit buku.
class EditBookScreen(Screen):
    def __init__(self, **kwargs):
        super(EditBookScreen, self).__init__(**kwargs)

        # Membuat edit_layout menggunakan MDBoxLayout.
        self.edit_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, width=Window.width, padding=15)
        self.edit_layout.pos_hint = {'top': 1}
        self.book_info = {}

        self.dialog = None

        # Membuat top_iconn_layout untuk tombol kembali dan hapus.
        top_icon_layout = MDBoxLayout(orientation='horizontal', spacing=10, adaptive_height=True)
        back_button = MDIconButton(icon='arrow-left', on_release=self.go_back)
        delete_button = MDIconButton(icon="delete", on_release=self.show_delete_confirmation)
        top_icon_layout.add_widget(back_button)
        top_icon_layout.add_widget(Label())
        top_icon_layout.add_widget(delete_button)
        top_icon_layout.pos_hint = {'x': 0, 'y': 0.9}
        self.edit_layout.add_widget(top_icon_layout)

        # Membuat field input menggunakan MDTextField.
        self.title_field = MDTextField(hint_text="Title")
        self.author_field = MDTextField(hint_text="Author")
        self.description_field = MDTextField(hint_text="Description")
        self.status_field = MDTextField(hint_text="Status")
        self.peminjaman_field = MDTextField(hint_text="Peminjaman")
        self.jumlah_field = MDTextField(hint_text="Jumlah")

        # Membuat tombol simpan menggunakan MDRectangleFlatButton.
        save_button = MDRectangleFlatButton(
            text="Save",
            md_bg_color="blue",
            text_color="white",
            size_hint=(1, None),
            height=42,
            on_release=self.save_changes
        )

        # Menambahkan elemen-elemen ke dalam edit_layout.
        self.edit_layout.add_widget(self.title_field)
        self.edit_layout.add_widget(self.author_field)
        self.edit_layout.add_widget(self.description_field)
        self.edit_layout.add_widget(self.status_field)
        self.edit_layout.add_widget(self.peminjaman_field)
        self.edit_layout.add_widget(self.jumlah_field)
        self.edit_layout.add_widget(MDLabel())
        self.edit_layout.add_widget(MDLabel())
        self.edit_layout.add_widget(MDLabel())
        self.edit_layout.add_widget(MDLabel())
        self.edit_layout.add_widget(save_button)

        # Menambahkan edit_layout ke dalam Screen.
        self.add_widget(self.edit_layout)

    # Membuat fungsi go_back.
    def go_back(self, instance):
        self.manager.current = "admin_home"

    # Membuat fungsi save_changes.
    def save_changes(self, instance):
        app = MDApp.get_running_app()
    
        # Mendapatkan nilai dari field input.
        new_title = self.title_field.text
        new_author = self.author_field.text
        new_description = self.description_field.text
        new_status = self.status_field.text
        new_peminjaman = self.peminjaman_field.text
        new_jumlalh = int(self.jumlah_field.text)

        # Memperbarui informasi buku.
        self.book_info['title'] = new_title
        self.book_info['author'] = new_author
        self.book_info['description'] = new_description
        self.book_info['status'] = new_status
        self.book_info['peminjaman'] = new_peminjaman
        self.book_info['jumlah'] = new_jumlalh

        # Mencari buku yang akan diperbarui berdasarkan 'id' dan memperbarui data buku.
        for i, book in enumerate(book_data):
            if book['id'] == self.book_info['id']:
                book_data[i] = self.book_info
                break

        # Mendapatkan instance dari screen admin_home dan home.
        admin_home_screen = app.root.get_screen("admin_home")
        home_screen = app.root.get_screen("home")

        # Menghapus dan menambahkan ulang grid buku di screen admin_home dan home.
        admin_home_screen.clear_book_grid()
        home_screen.clear_book_grid()

        for book in book_data:
            home_screen.add_book_to_grid(book)
            admin_home_screen.add_book_to_grid(book)

        # Beralih ke screen admin_home.
        app.root.current = "admin_home"
    
    # Membuat fungsi set_book_info.
    def set_book_info(self, book_info):
        self.book_info = book_info

        # Mengisi nilai field input dengan informasi buku yang akan diedit.
        self.title_field.text = self.book_info.get('title', '')
        self.author_field.text = self.book_info.get('author', '')
        self.description_field.text = self.book_info.get('description', '')
        self.status_field.text = self.book_info.get('status', '')
        self.peminjaman_field.text = self.book_info.get('peminjaman', '')
        self.jumlah_field.text = str(self.book_info.get('jumlah', ''))

    # Membuat fungsi untuk menampilkan konfirmasi penghapusan.
    def show_delete_confirmation(self, instance):
        self.dialog = MDDialog(
            text="Are you sure you want to delete this book?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=self.close_dialog),
                MDFlatButton(text="Delete", on_release=self.delete_book)
            ],
        )
        self.dialog.open()

    # Membuat fungsi untuk menutup dialog konfirmasi penghapusan.
    def close_dialog(self, instance):
        self.dialog.dismiss()

    # Membuat fungsi untuk menghapus buku.
    def delete_book(self, instance):
        app = MDApp.get_running_app()

        # Menghapus dan menambahkan ulang grid buku di screen admin_home dan home.
        app.root.get_screen("admin_home").clear_book_grid()
        app.root.get_screen("home").clear_book_grid()

        for book in book_data:
            if book == self.book_info:
                book_data.remove(book)
                break
        
        for book in book_data:
            app.root.get_screen("admin_home").add_book_to_grid(book)
            app.root.get_screen("home").add_book_to_grid(book)
        
        # Menutup dialog konfirmasi penghapusan.
        if self.dialog:
            self.dialog.dismiss()
        
        # Beralih ke screen admin_home.
        self.manager.current = "admin_home"
    

# Kelas BacaCepat untuk menginisialisasi aplikasi.
class BacaCepat(MDApp):
    def build(self):
        # Mengatur tema aplikasi ke "Light".
        self.theme_cls.theme_style = "Light"

        # Membuat instance dari ScreenManager.
        self.screen_manager = ScreenManager()

        # Membuat instance dari layar login.
        self.login_screen = LoginScreen(name="login")

        # Membuat instance dari layar home dan admin_home.
        home_screen = HomeScreen(name="home")
        admin_home_screen = AdminHomeScreen(name="admin_home") 

        # Menambahkan buku ke dalam grid di layar home dan admin_home.
        for book in book_data:
            home_screen.add_book_to_grid(book)
            admin_home_screen.add_book_to_grid(book) 

        # Menambahkan instance layar ke dalam ScreenManager.
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(admin_home_screen)
        self.screen_manager.add_widget(DetailScreen(name="detail"))
        self.screen_manager.add_widget(HistoryScreen(name="history"))
        self.screen_manager.add_widget(NewBookScreen(name="newBook"))
        self.screen_manager.add_widget(EditBookScreen(name="editBook"))

        # Mengembalikan instance ScreenManager.
        return self.screen_manager

    # Membuat fungsi on_search untuk menangani pencarian buku.
    def on_search(self, instance, value):
        # Mendapatkan instance layar home.
        home_screen = self.root.get_screen('home')

        # Menghapus dan menambahkan ulang grid buku di layar home berdasarkan pencarian.
        home_screen.clear_book_grid()

        for book in book_data:
            if value.lower() in book['title'].lower():
                home_screen.add_book_to_grid(book)

    # Membuat fungsi show_book_details untuk menampilkan detail buku di layar detail.
    def show_book_details(self, book_info):
        # Mendapatkan instance layar detail.
        detail_screen = self.root.get_screen("detail")

        # Menampilkan detail buku di layar detail.
        detail_screen.show_book_details(book_info)

# Menjalankan aplikasi jika file ini dijalankan sebagai program utama.
if __name__ == "__main__":
    BacaCepat().run()