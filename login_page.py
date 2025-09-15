def login(username_user):
    file=open('login_system.txt','r')
    content=file.read()
    file.close()

    usernames=content.split('-')
    for username in usernames:
        if username !="" and username_user in usernames:
            print("login sucessful.")
            break
        else:
            print('invalid username.')
            break



def register(username):
    file=open('login_system.txt','r')
    content=file.read()
    file.close()

    usernames=content.split('-')
    if username in usernames:
        print('usernames already exits.')
    else:
        file=open('login_system.txt','a')
        file.write(username + '-')
        file.close()
        print('username added.')

    

while True:
    choice= input("what operation do you want to perform:'l' for login and 'r' for register:").lower()
    match choice:
        case "l":
            username=input("enter username:")
            login(username)

        case "r":
            username=input("enter username:")
            register(username)

        case "_":
            print('Invalid input.')

    again= input('Do you want to continue? (y/n):').lower()
    match again:
        case "n":
            print("Thank U")

