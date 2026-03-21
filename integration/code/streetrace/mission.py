# integration/code/streetrace/mission.py
from .models import CrewMember
from .inventory import InventoryModule

class MissionPlanningModule:
    def __init__(self, inventory: InventoryModule):
        self.inventory = inventory

    def plan_repair_mission(self, car_id: str, mechanics: list, parts_required: int):
        if not mechanics:
            raise ValueError("Mechanic required for repair mission.")
        
        car = self.inventory.cars.get(car_id)
        if not car:
            raise ValueError("Car not found.")
            
        if self.inventory.spare_parts < parts_required:
            raise ValueError("Not enough spare parts.")
        
        mechanic = mechanics[0]
        if mechanic.status != "available":
            raise ValueError("Mechanic is not available.")
            
        # Execute repair
        self.inventory.spare_parts -= parts_required
        car.condition = 100
        mechanic.skill_level += 1
        
    def plan_heist_mission(self, driver: CrewMember, strategist: CrewMember):
        if not driver or driver.role != "driver":
            raise ValueError("Valid driver required.")
        if not strategist or strategist.role != "strategist":
            raise ValueError("Valid strategist required.")
            
        # Execute heist
        self.inventory.add_cash(1000)
