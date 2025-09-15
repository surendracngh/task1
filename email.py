import sqlite3

# ------------------------
# Database setup
# ------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


# ------------------------
# Register new user
# ------------------------
def register_user(email, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("⚠️ Error: Email already registered.")


# ------------------------
# Login user
# ------------------------
def login_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("✅ Login successful! Welcome,", email)
    else:
        print("❌ Invalid email or password.")


# ------------------------
# Main Program
# ------------------------
if __name__ == "__main__":
    init_db()

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            email = input("Enter email: ")
            password = input("Enter password: ")
            register_user(email, password)

        elif choice == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            login_user(email, password)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("⚠️ Invalid choice, try again.")
