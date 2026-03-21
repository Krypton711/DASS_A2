# integration/code/streetrace/sponsorship.py
from .models import Sponsor

class SponsorshipModule:
    def __init__(self):
        self.sponsors = []
        self.active_sponsor = None
        self.reputation = 0
        
    def add_sponsor(self, sponsor: Sponsor):
        self.sponsors.append(sponsor)
        
    def sign_sponsor(self, sponsor_id: str):
        sponsor = next((s for s in self.sponsors if s.id == sponsor_id), None)
        if not sponsor:
            raise ValueError("Sponsor not found.")
        if self.reputation < sponsor.required_reputation:
            raise ValueError("Reputation too low for this sponsor.")
        self.active_sponsor = sponsor
        
    def get_race_bonus(self) -> int:
        return self.active_sponsor.payout_bonus if self.active_sponsor else 0

    def update_reputation(self, won: bool):
        self.reputation += 10 if won else -5
