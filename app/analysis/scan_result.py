from dataclasses import dataclass, field

from app.analysis.persistence_entry import PersistenceEntry


@dataclass
class ScanResult:
    """Represents the result of one full autorun scan."""

    scan_time: str = ""
    total_entries: int = 0
    low_count: int = 0
    medium_count: int = 0
    high_count: int = 0
    critical_count: int = 0
    entries: list[PersistenceEntry] = field(default_factory=list)
    status: str = "success"

    def calculate_counts(self):
        """Calculate total entries and risk level counters."""
        self.total_entries = len(self.entries)
        self.low_count = 0
        self.medium_count = 0
        self.high_count = 0
        self.critical_count = 0

        for entry in self.entries:
            if entry.risk_level == "Low":
                self.low_count += 1
            elif entry.risk_level == "Medium":
                self.medium_count += 1
            elif entry.risk_level == "High":
                self.high_count += 1
            elif entry.risk_level == "Critical":
                self.critical_count += 1

    def to_dict(self):
        """Convert the scan result object to a dictionary."""
        return {
            "scan_time": self.scan_time,
            "total_entries": self.total_entries,
            "low_count": self.low_count,
            "medium_count": self.medium_count,
            "high_count": self.high_count,
            "critical_count": self.critical_count,
            "entries": [entry.to_dict() for entry in self.entries],
            "status": self.status,
        }