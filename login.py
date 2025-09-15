def login(username_input, password_input):
    with open('login_system.txt', 'r') as file:
        content = file.read().strip()

    if content == "":
        print("No users registered yet.")
        return

    users = content.strip('-').split('-')  # split user blocks

    for user in users:
        if ':' in user:
            username, password = user.split(':')
            if username == username_input and password == password_input:
                print("Login successful.")
                return

    print("Invalid username or password.")


def register(username_input, password_input):
    with open('login_system.txt', 'r') as file:
        content = file.read().strip()

    users = content.strip('-').split('-') if content else []

    for user in users:
        if ':' in user:
            username, _ = user.split(':')
            if username == username_input:
                print("Username already exists.")
                return

    with open('login_system.txt', 'a') as file:
        file.write(f"{username_input}:{password_input}-")

    print("Registration successful.")


while True:
    choice = input("Choose an option (l for login, r for register): ").lower()

    match choice:
        case "l":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)

        case "r":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)

        case _:
            print("Invalid input.")

    again = input("Do you want to continue? (y/n): ").lower()
    if again != 'y':
        print("Goodbye!")
        break
