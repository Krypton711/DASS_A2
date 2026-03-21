import sys
from streetrace.models import CrewMember, Car, Sponsor
from streetrace.registration import RegistrationModule
from streetrace.crew import CrewManagementModule
from streetrace.inventory import InventoryModule
from streetrace.race import RaceManagementModule
from streetrace.results import ResultsModule
from streetrace.mission import MissionPlanningModule
from streetrace.sponsorship import SponsorshipModule
from streetrace.heat import HeatTrackingModule

def main():
    print("==================================")
    print("    STREETRACE MANAGER - CLI      ")
    print("==================================")
    
    # Initialize Core Modules
    reg = RegistrationModule()
    crew = CrewManagementModule()
    inv = InventoryModule(initial_cash=5000)
    race = RaceManagementModule()
    results = ResultsModule(inventory=inv, crew_manager=crew)
    mission = MissionPlanningModule(inventory=inv)
    sponsor = SponsorshipModule()
    heat = HeatTrackingModule()

    # Seed initial data for demonstration
    m1 = reg.register_member("m1", "Dom")
    crew.assign_role(m1, "driver")
    inv.add_car(Car(id="c1", model="Dodge Charger", condition=100))
    
    m2 = reg.register_member("m2", "Tej")
    crew.assign_role(m2, "mechanic")
    
    print("\n[System Initialized with 1 Driver, 1 Mechanic, and 1 Car]")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. View Inventory")
        print("2. View Crew")
        print("3. Enter Race")
        print("4. Repair Car (Mission)")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            print(f"\nInventory: ${inv.cash_balance}")
            print(f"Cars: {[c.model for c in inv.get_available_cars()]}")
            
        elif choice == '2':
            print("\nCrew:")
            for m in reg.get_all_members():
                print(f"- {m.name} ({m.role}) | Skill: {m.skill_level} | Status: {m.status}")
                
        elif choice == '3':
            try:
                race.create_race("r1", "Quarter Mile Sprint", difficulty=2, prize=2000)
                race.enter_race("r1", reg.get_member("m1"), inv.cars["c1"])
                print("\nEntered Race! Resolving results...")
                
                # Automatically resolve for demo purposes
                race_data = race.races["r1"]
                results.record_race_outcome(race_data, winner_driver=reg.get_member("m1"))
                
                print("Race won! You earned $2000. Car took damage.")
            except ValueError as e:
                print(f"Error entering race: {e}")
                
        elif choice == '4':
            try:
                print("\nAttempting repair mission...")
                inv.spare_parts += 10 # Give them some parts for testing
                mission.plan_repair_mission("c1", [reg.get_member("m2")], parts_required=5)
                print("Car successfully repaired by Tej!")
            except ValueError as e:
                print(f"Error repairing car: {e}")
                
        elif choice == '5':
            print("Exiting StreetRace Manager.")
            sys.exit(0)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
