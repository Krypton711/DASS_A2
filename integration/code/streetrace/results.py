# integration/code/streetrace/results.py
import random
from .models import CrewMember, Car
from .inventory import InventoryModule
from .crew import CrewManagementModule

class ResultsModule:
    def __init__(self, inventory: InventoryModule, crew_manager: CrewManagementModule):
        self.inventory = inventory
        self.crew_manager = crew_manager
        self.rankings = {}

    def record_race_outcome(self, race_data: dict, winner_driver: CrewMember, sponsor_bonus: int = 0):
        if not race_data["participants"]:
            raise ValueError("No participants in race.")
            
        # Update prize money
        total_payout = race_data["prize"] + sponsor_bonus
        self.inventory.add_cash(total_payout)
        
        # Free up participants and apply wear/tear
        for p in race_data["participants"]:
            driver = p["driver"]
            car = p["car"]
            driver.status = "available"
            
            # Simulated damage
            damage = 15
            car.condition = max(0, car.condition - damage)
            
            if driver == winner_driver:
                self.crew_manager.update_skill(driver, 2)
                self.rankings[driver.id] = self.rankings.get(driver.id, 0) + 10
            else:
                self.crew_manager.update_skill(driver, 1)
