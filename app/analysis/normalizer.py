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
    
    def extract_path(self,command: str) -> str:
        """Extract executable apth from a command string."""

        if not command:
            return ""
        
        command = command.strip()

        if command.startswith('"'):
            end_quote_index = command.find('"', 1)

            if end_quote_index != -1:
                return command[1:end_quote_index]
            
        executable_extensions = [".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".Ink"]
        lower_command = command.lower()

        for extension in executable_extensions:
            extension_index = lower_command.find(extension)

            if extension_index != -1:
                return command[: extension_index + len(extension)].strip()
            
        return command.split()[0]
    
    def generate_entry_id(self, entry: PersistenceEntry) -> str:
        """ Generate a stable unique ID for a persistence entry"""
        raw_id = f"{entry.source}|{entry.name}|{entry.path}|{entry.command}"
        return hashlib.sha256(raw_id.lower().encode("utf-8")).hexdigest()
    
    def get_entry_type(self, entry: dict) -> str:
        """Return a readable entry type based on collector source."""

        source = entry.get("source", "")


        if source =="Registry":
            return "Registry Run Key"
        
        if source == "Startup Folder":
            return "Startup Folder"
        
        if source == "Scheduled Task":
            return "Scheduled Task"
        
        if source == "Windows Service":
            return "Windows Service"
        
        return "Unknown"