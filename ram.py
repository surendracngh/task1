import os

# Base Book class
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"

    def to_file_string(self):
        return f"book,{self.title},{self.author},{self.isbn}\n"

# EBook inherits from Book
class EBook(Book):
    def __init__(self, title, author, isbn, file_size):
        super().__init__(title, author, isbn)
        self.file_size = file_size

    def display_info(self):
        return f"{super().display_info()}, File Size: {self.file_size}MB"

    def to_file_string(self):
        return f"ebook,{self.title},{self.author},{self.isbn},{self.file_size}\n"

# Library class
class Library:
    def __init__(self, filename="library.txt"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """Load books from file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == "book":
                        self.books.append(Book(data[1], data[2], data[3]))
                    elif data[0] == "ebook":
                        self.books.append(EBook(data[1], data[2], data[3], data[4]))

    def save_books(self):
        """Save books to file."""
        with open(self.filename, "w") as file:
            for book in self.books:
                file.write(book.to_file_string())

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        print(f"✅ Book '{book.title}' added to the library.")

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                self.save_books()
                print(f"❌ Book '{book.title}' removed from the library.")
                return
        print("⚠️ Book not found.")

    def search_book(self, title):
        results = [book for book in self.books if title.lower() in book.title.lower()]
        if results:
            print("\n🔍 Search Results:")
            for b in results:
                print(b.display_info())
        else:
            print("⚠️ No book found with that title.")

    def view_books(self):
        if not self.books:
            print("📚 Library is empty.")
        else:
            print("\n📚 All Books in Library:")
            for b in self.books:
                print(b.display_info())

# Main Program
def main():
    lib = Library()

    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. View All Books")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")

        match choice:
            case "1":
                book_type = input("Enter book type (book/ebook): ").strip().lower()
                title = input("Enter title: ")
                author = input("Enter author: ")
                isbn = input("Enter ISBN: ")

                if book_type == "ebook":
                    file_size = input("Enter file size in MB: ")
                    book = EBook(title, author, isbn, file_size)
                else:
                    book = Book(title, author, isbn)

                lib.add_book(book)

            case "2":
                isbn = input("Enter ISBN of book to remove: ")
                lib.remove_book(isbn)

            case "3":
                title = input("Enter title to search: ")
                lib.search_book(title)

            case "4":
                lib.view_books()

            case "5":
                print("👋 Exiting Library System. Goodbye!")
                break

            case _:
                print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()