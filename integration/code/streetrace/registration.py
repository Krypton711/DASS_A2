# integration/code/streetrace/registration.py
from .models import CrewMember

class RegistrationModule:
    def __init__(self):
        self.members = {}

    def register_member(self, member_id: str, name: str) -> CrewMember:
        if member_id in self.members:
            raise ValueError(f"Member with ID {member_id} already exists.")
        
        member = CrewMember(id=member_id, name=name)
        self.members[member_id] = member
        return member

    def get_member(self, member_id: str) -> CrewMember:
        if member_id not in self.members:
            raise ValueError("Member not found.")
        return self.members[member_id]
    
    def get_all_members(self) -> list:
        return list(self.members.values())
