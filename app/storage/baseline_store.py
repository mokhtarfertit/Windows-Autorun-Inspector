import json
from pathlib import Path

from app.analysis.persistence_entry import PersistenceEntry


class BaselineStore:
    """Save and load baseline persistence entries."""

    def __init__(self, baseline_path: str = "baseline.json"):
        self.baseline_path = Path(baseline_path)

    def save(self, entries: list[PersistenceEntry]) -> bool:
        """Save persistence entries to baseline JSON file."""
        try:
            data = [entry.to_dict() for entry in entries]

            with self.baseline_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return True

        except OSError:
            return False

    def load(self) -> list[PersistenceEntry]:
        """Load persistence entries from baseline JSON file."""
        if not self.exists():
            return []

        try:
            with self.baseline_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            entries = []

            for item in data:
                entries.append(PersistenceEntry(**item))

            return entries

        except (OSError, json.JSONDecodeError, TypeError):
            return []

    def exists(self) -> bool:
        """Check if baseline file exists."""
        return self.baseline_path.exists()