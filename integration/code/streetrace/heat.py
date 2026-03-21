# integration/code/streetrace/heat.py
class HeatTrackingModule:
    def __init__(self):
        self.heat_level = 0
        self.MAX_HEAT = 100

    def add_heat_from_race(self, difficulty: int):
        self.heat_level = min(self.MAX_HEAT, self.heat_level + difficulty * 5)

    def reduce_heat_with_lookout(self, lookout_skill: int):
        self.heat_level = max(0, self.heat_level - lookout_skill * 10)
        
    def is_busted(self) -> bool:
        # Static implementation for pure logical testing
        if self.heat_level > 80:
            return True
        return False
