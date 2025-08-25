text = input("Enter a string: ")

vowels = 0
consonants = 0

for ch in text.lower():
    if ch in "aeiou":
        vowels += 1
    elif ch >= 'a' and ch <= 'z':
        consonants += 1

print("Vowels:", vowels)
print("Consonants:", consonants)
