# integration/code/streetrace/race.py
from .models import CrewMember, Car

class RaceManagementModule:
    def __init__(self):
        self.races = {}

    def create_race(self, race_id: str, name: str, difficulty: int, prize: int):
        self.races[race_id] = {
            "name": name,
            "difficulty": difficulty,
            "prize": prize,
            "participants": []
        }

    def enter_race(self, race_id: str, driver: CrewMember, car: Car):
        if race_id not in self.races:
            raise ValueError("Race doesn't exist.")
        if driver.role != "driver":
            raise ValueError("Only drivers can be entered into a race.")
        if driver.status != "available":
            raise ValueError("Driver is not available.")
        if car.condition <= 0:
            raise ValueError("Car is too damaged to race.")
        
        self.races[race_id]["participants"].append({"driver": driver, "car": car})
        driver.status = "busy"
