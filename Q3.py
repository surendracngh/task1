def remove_vowels(text):
    result = ""
    for ch in text:
        if ch.lower() not in "aeiou":
            result += ch
    return result

user_input = input("Enter a string: ")
print("Without vowels:", remove_vowels(user_input))
