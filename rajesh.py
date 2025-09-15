def login(username_user):
    with open('login_system.txt', 'r') as file:
        content = file.read()

    usernames = content.split('-')
    if username_user in usernames and username_user != "":
        print("Login successful.")
    else:
        print("Invalid username.")

def register(username):
    with open('login_system.txt', 'a') as file:
        file.write(username + '-')
    print("Registration successful.")

while True:
    choice = input("What operation do you want to perform? (l for login, r for register): ").lower()

    match choice:
        case "l":
            username = input("Enter username: ")
            login(username)

        case "r":
            username = input("Enter username: ")
            register(username)

        case _:
            print("Invalid input.")

    again = input("Do you want to continue? (y/n): ").lower()
    if again != 'y':
        print("Goodbye!")
        break
