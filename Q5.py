def append_to_file():
    try:
        with open("user_input.txt", "a") as file:
            while True:
                text = input("Enter text (type 'exit' to stop): ")
                if text.lower() == "exit":
                    break
                file.write(text + "\n")
        print("Data saved to file.")
    except Exception as e:
        print("An error occurred:", e)

append_to_file()
