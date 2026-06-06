class Car:
    def __init__(self, brand, color, speed):
        self.brand = brand
        self.color = color
        self.speed = speed

    def drive(self):
        print("The " + self.color + " " + self.brand +
              " is driving at" + str(self.speed) + " km/h")

    def accelerate(self):
        self.speed += 10

    def brake(self):
        self.speed -= 10

    def drive(self):
        print("The " + self.color + " " + self.brand +
              " is driving at " + str(self.speed) + " km/h")


car1 = Car("Ferrari", "Red", 0)
car2 = Car("Lamborghini", "Yellow", 0)

car1.accelerate()
car1.accelerate()
car2.accelerate()
car2.brake()

print(car1.brand + " is going " + str(car1.speed) + " km/h")
print(car2.brand + " is going " + str(car2.speed) + " km/h")
car1.drive()
car2.drive()
