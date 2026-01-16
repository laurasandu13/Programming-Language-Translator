class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello, I am ", self.name)

    def haveBirthday(self):
        self.age += 1
        print(self.name, " is now ", self.age)

    def isAdult(self):
        if self.age >= 18:
            return True
        else:
            return False


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(self.name, " says: Woof!")

    def getDogYears(self):
        dogYears = self.age * 7
        return dogYears


print("=== CLASS DEMO ===")
alice = Person("Alice", 25)
alice.greet()
alice.haveBirthday()
isAliceAdult = alice.isAdult()
if isAliceAdult:
    print("Alice is an adult")
buddy = Dog("Buddy", 3)
buddy.bark()
years = buddy.getDogYears()
print("Dog years: ", years)
print("=== DONE ===")
