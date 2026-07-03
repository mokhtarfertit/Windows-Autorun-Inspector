from dataclasses import dataclass, field

@dataclass
class PersistenceEntry:
    """Represents one windows autorun persistence entry."""

    id: str = ""
    name: str = ""
    entry_type: str = ""
    source: str = ""
    command: str = ""
    path: str = ""
    timestamp: str = ""
    publisher: str = ""
    sha256: str = ""
    mitre_technique: str = ""
    risk_score: int = 0
    risk_level: str = "Low"
    reasons: list[str] = field(default_factory=list)

    def to_dict(self):
        """Convert the persistence entry object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "entry_type": self.entry_type,
            "source": self.source,
            "command": self.command,
            "path": self.path,
            "timestamp": self.timestamp,
            "publisher": self.publisher,
            "sha256": self.sha256,
            "mitre_technique": self.mitre_technique,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "reasons": self.reasons,
        }