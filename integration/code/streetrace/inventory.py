# integration/code/streetrace/inventory.py
from .models import Car

class InventoryModule:
    def __init__(self, initial_cash: int = 0):
        self.cash_balance = initial_cash
        self.cars = {}
        self.spare_parts = 0
        self.tools = 0

    def add_car(self, car: Car):
        if car.id in self.cars:
            raise ValueError(f"Car {car.id} already in inventory.")
        self.cars[car.id] = car

    def add_cash(self, amount: int):
        if amount > 0:
            self.cash_balance += amount

    def deduct_cash(self, amount: int):
        if amount > self.cash_balance:
            raise ValueError("Insufficient funds!")
        self.cash_balance -= amount
            
    def get_available_cars(self) -> list:
        return [c for c in self.cars.values() if c.condition > 0]
