# integration/code/streetrace/models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class CrewMember:
    id: str
    name: str
    role: str = ""
    skill_level: int = 1
    status: str = "available"  # available, busy, injured

@dataclass
class Car:
    id: str
    model: str
    performance_rating: int = 50
    condition: int = 100 # percentage

@dataclass
class Sponsor:
    id: str
    name: str
    required_reputation: int = 0
    payout_bonus: int = 0
