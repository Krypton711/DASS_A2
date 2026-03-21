import pytest
from streetrace.models import CrewMember, Car, Sponsor
from streetrace.registration import RegistrationModule
from streetrace.crew import CrewManagementModule
from streetrace.inventory import InventoryModule
from streetrace.race import RaceManagementModule
from streetrace.results import ResultsModule
from streetrace.mission import MissionPlanningModule
from streetrace.sponsorship import SponsorshipModule
from streetrace.heat import HeatTrackingModule

def setup_system():
    reg = RegistrationModule()
    crew = CrewManagementModule()
    inv = InventoryModule(initial_cash=1000)
    race = RaceManagementModule()
    results = ResultsModule(inventory=inv, crew_manager=crew)
    mission = MissionPlanningModule(inventory=inv)
    sponsor = SponsorshipModule()
    heat = HeatTrackingModule()
    return reg, crew, inv, race, results, mission, sponsor, heat

def test_integration_register_and_race():
    """Registering a driver and then entering the driver into a race."""
    reg, crew, inv, race, results, mission, sponsor, heat = setup_system()
    
    # 1. Register Member
    member = reg.register_member("m1", "Dominic")
    assert member.name == "Dominic"
    
    # 2. Assign Role
    crew.assign_role(member, "driver")
    assert member.role == "driver"
    
    # 3. Add Car to Inventory
    car = Car(id="c1", model="Charger R/T")
    inv.add_car(car)
    
    # 4. Create and Enter Race
    race.create_race("r1", "Downtown Sprint", difficulty=3, prize=5000)
    race.enter_race("r1", member, car)
    
    # Verify driver is busy and car is entered
    assert member.status == "busy"
    assert len(race.races["r1"]["participants"]) == 1

def test_integration_invalid_race_entry():
    """Attempting to enter a race without a registered driver."""
    reg, crew, inv, race, _, _, _, _ = setup_system()
    
    # Register member but assign wrong role
    member = reg.register_member("m1", "Tej")
    crew.assign_role(member, "mechanic")
    
    car = Car(id="c1", model="Skyline")
    inv.add_car(car)
    race.create_race("r1", "Bridge Run", difficulty=2, prize=2000)
    
    # Should fail as mechanic cannot drive
    with pytest.raises(ValueError, match="Only drivers can be entered into a race."):
        race.enter_race("r1", member, car)

def test_integration_race_results_flow():
    """Completing a race and verifying results and prize money update the inventory."""
    reg, crew, inv, race, results, _, sponsor, _ = setup_system()
    
    member = reg.register_member("m1", "Brian")
    crew.assign_role(member, "driver")
    car = Car(id="c1", model="Supra")
    inv.add_car(car)
    
    race.create_race("r1", "Quarter Mile", difficulty=1, prize=10000)
    race.enter_race("r1", member, car)
    
    # Add a sponsor bonus
    sp = Sponsor(id="s1", name="Nos", required_reputation=0, payout_bonus=2000)
    sponsor.add_sponsor(sp)
    sponsor.sign_sponsor("s1")
    
    initial_cash = inv.cash_balance
    initial_skill = member.skill_level
    
    # Complete race
    race_data = race.races["r1"]
    results.record_race_outcome(race_data, winner_driver=member, sponsor_bonus=sponsor.get_race_bonus())
    
    # Verify Inventory updated (Initial + Prize + Sponsor)
    assert inv.cash_balance == initial_cash + 10000 + 2000
    
    # Verify Driver freed and skill increased
    assert member.status == "available"
    assert member.skill_level > initial_skill
    
    # Verify Car took damage
    assert car.condition < 100

def test_integration_mission_planning_roles():
    """Assigning a mission and ensuring correct crew roles are validated."""
    reg, crew, inv, _, _, mission, _, _ = setup_system()
    
    inv.spare_parts = 10
    car = Car(id="c1", model="Evo", condition=50)
    inv.add_car(car)
    
    # Create mechanic
    mech = reg.register_member("m2", "Letty")
    crew.assign_role(mech, "mechanic")
    
    # Execute repair mission properly
    mission.plan_repair_mission("c1", [mech], parts_required=5)
    
    assert car.condition == 100
    assert inv.spare_parts == 5
    assert mech.skill_level == 2 # Skill increases after repairing

def test_integration_heat_and_lookout():
    """Testing Heat generation and reduction with lookouts over multiple modules."""
    reg, crew, _, _, _, _, _, heat = setup_system()
    
    heat.add_heat_from_race(difficulty=10)
    assert heat.heat_level == 50
    assert heat.is_busted() is False
    
    # Add more heat to push over threshold
    heat.add_heat_from_race(difficulty=10) # Level -> 100
    assert heat.is_busted() is True
        
    # Use lookout to reduce heat
    lookout = reg.register_member("m3", "Roman")
    crew.assign_role(lookout, "lookout")
    lookout.skill_level = 5 # Level 5 lookout
    
    heat.reduce_heat_with_lookout(lookout.skill_level)
    assert heat.heat_level == 50 # 100 - (5 * 10) = 50
    
    # Now safe
    assert heat.is_busted() is False
