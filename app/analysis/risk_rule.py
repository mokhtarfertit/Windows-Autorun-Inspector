from dataclasses import dataclass

from app.analysis.persistence_entry import PersistenceEntry


@dataclass
class RiskRule:
    """Represents one risk detection rule."""

    name: str
    description: str
    score: int

    def check(self, entry: PersistenceEntry) -> bool:
        """Check if the rule matches a persistence entry."""
        return False