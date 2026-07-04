from dataclasses import dataclass
from typing import Callable

from app.analysis.persistence_entry import PersistenceEntry


@dataclass
class RiskRule:
    """Represents one risk detection rule."""

    name: str
    description: str
    score: int
    check_function: Callable[[PersistenceEntry], bool]

    def check(self, entry: PersistenceEntry) -> bool:
        """Check if the rule matches a persistence entry."""
        return self.check_function(entry)