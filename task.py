import json

def register(username,password):
    dict_credential = {username:password}
    json_credential = json.dumps(dict_credential)
    file = open("dict_credential.txt","a")
    file.write(json_credential+"-")
    file.close()

def login(username,password):
    file = open("dict_credential.txt","r")
    content = file.read()
    file.close()
    
    json_credential = content.split("-") 
    for i in json_credential:
        if i != "":
            dict_i = json.loads(i)
            if username in dict_i and dict_i[username]==password:
                print("Login Successful.")
                break
    else:
        print("Invalid credential. Please try again")

choice = input("Enter r for register and l for login: ").lower()
match choice:
    case 'r':
        username = input("ENter your username: ")
        password = input("Enter your password: ")
        register(username,password)
    case 'l':
        username_l = input("ENter your username: ")
        password_l = input("Enter your password: ")
        login(username_l,password_l)
    case _:
        print("Invalid input. Please try again")