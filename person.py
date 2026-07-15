class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print("Hi I am " + self.name + " and I am " + self.age + " years old.")


person1 = Person("Josh", "18")
person2 = Person("Laci", "20")

person1.introduce()
person2.introduce()
