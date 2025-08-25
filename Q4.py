class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


length = float(input("Enter length: "))
width = float(input("Enter width: "))
rect = Rectangle(length, width)

print("Area:", rect.area())
print("Perimeter:", rect.perimeter())
