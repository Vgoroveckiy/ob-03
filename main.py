# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) и методы (`make_sound()`, `eat()`) для всех животных.
# 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`. Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
# 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных и вызывает метод `make_sound()` для каждого животного.
# 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках. Должны быть методы для добавления животных и сотрудников в зоопарк.
# 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические методы (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).

# Дополнительно:
# Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл и возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.

import json


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        print(f"{self.name} ест.")


class Bird(Animal):
    def make_sound(self):
        print(f"{self.name} чирикает.")


class Mammal(Animal):
    def make_sound(self):
        print(f"{self.name} мяукает.")


class Reptile(Animal):
    def make_sound(self):
        print(f"{self.name} шипит.")


class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def feed_animal(self):
        print(f"{self.name} не кормит животных.")

    def heal_animal(self):
        print(f"{self.name} не лечит животных.")


class ZooKeeper(Employee):
    def feed_animal(self):
        print(f"{self.name} кормит животных.")


class Veterinarian(Employee):
    def heal_animal(self):
        print(f"{self.name} лечит животных.")


class Zoo:
    def __init__(self, filename="zoo_state.json"):
        self._animals = []
        self._employees = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                zoo_state = json.load(file)
                for animal in zoo_state["animals"]:
                    animal_type = globals()[animal["type"]]
                    self.add_animal(animal_type(animal["name"], animal["age"]))
                for employee in zoo_state["employees"]:
                    employee_type = globals()[employee["role"]]
                    self.add_employee(employee_type(employee["name"], employee["age"]))
        except FileNotFoundError:
            pass

    def add_animal(self, animal):
        self._animals.append(animal)

    def add_employee(self, employee):
        self._employees.append(employee)

    def get_animals(self):
        return self._animals

    def get_employees(self):
        return self._employees

    def save_to_file(self, filename):
        zoo_state = {
            "animals": [
                {"name": animal.name, "age": animal.age, "type": type(animal).__name__}
                for animal in self._animals
            ],
            "employees": [
                {
                    "name": employee.name,
                    "age": employee.age,
                    "role": type(employee).__name__,
                }
                for employee in self._employees
            ],
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(zoo_state, file, ensure_ascii=False, indent=4)


zoo = Zoo("zoo_state.json")
# zoo.add_animal(Bird("Петух", 3))
# zoo.add_animal(Mammal("Кошка", 2))
# zoo.add_animal(Reptile("Змея", 1))
# zoo.add_employee(Veterinarian("Вася", 25))
# zoo.add_employee(ZooKeeper("Петя", 30))
# zoo.add_employee(ZooKeeper("Коля", 25))
# zoo.save_to_file("zoo_state.json")

print("Список животных в зоопарке:")
for animal in zoo.get_animals():
    print(f"{animal.name} ({animal.age} лет)")

print("Активности животных:")
for animal in zoo.get_animals():
    animal.make_sound()
    animal.eat()

print(f"Список сотрудников в зоопарке:")
for employee in zoo.get_employees():
    print(f"{employee.name} ({employee.age} лет)")

print("Активности сотрудников:")
for employee in zoo.get_employees():
    employee.feed_animal()
    employee.heal_animal()
