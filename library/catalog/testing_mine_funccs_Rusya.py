class Car:
    def __init__(self, mark, speed):
        self.mark = mark
        self.speed = speed


toyota = Car("Toyota", 250)
lexus = Car("Lexus", 300)
Car.mark = "Ford"
bmw = Car("BMW", 400)
print(Car.mark)
