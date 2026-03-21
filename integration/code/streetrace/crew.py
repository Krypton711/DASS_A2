# integration/code/streetrace/crew.py
from .models import CrewMember

class CrewManagementModule:
    VALID_ROLES = ["driver", "mechanic", "strategist", "lookout"]

    def assign_role(self, member: CrewMember, role: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        member.role = role

    def update_skill(self, member: CrewMember, skill_change: int):
        member.skill_level = max(1, member.skill_level + skill_change)

    def get_available_members_by_role(self, members: list, role: str) -> list:
        return [m for m in members if m.role == role and m.status == "available"]
