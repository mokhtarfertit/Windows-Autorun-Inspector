import hashlib

from app.analysis.persistence_entry import PersistenceEntry
from app.utils.hash_utils import calculate_sha256

class Normalizer:
    """Convert raw collector dictionaries into PersistenceEntry Objects."""

    def normalize(self,entries: list[dict]) -> list[PersistenceEntry]:
        """Noramlize a list of raw collector entries """

        normalized_entries = []

        for entry in entries:
            normalized_entries.append(self.normalize_entry(entry))

        return normalized_entries
    
    def normalize_entry(self, entry: dict) -> PersistenceEntry:
        """Noramize one raw collector entry."""
        name = entry.get("name", "")
        source = entry.get("source", "")
        command = entry.get("command", "")
        path = entry.get("path", "")

        if not path:
            path = self.extract_path(command)

        persistence_entry = PersistenceEntry(
            name=name,
            entry_type= self.get_entry_type(entry),
            source=source,
            command=command,
            path=path,
            timestamp=entry.get("timestamp", ""),
            sha256=calculate_sha256(path),
            mitre_technique= entry.get("mitre_technique", ""),
        )

        persistence_entry.id = self.generate_entry_id(persistence_entry)

        return persistence_entry
    
    def extract_path