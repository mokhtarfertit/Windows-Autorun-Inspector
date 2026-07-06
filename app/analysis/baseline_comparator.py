from app.analysis.persistence_entry import PersistenceEntry

class BaseLIneComparator:
    """Compare current persistence entries with baseline entries."""

    def compare(self,
                current_entries: list[PersistenceEntry],
                  baseline_entries: list[PersistenceEntry],
    ) -> dict:
        """Compare current entries with baseline entries."""
        return {
            "new_entries": self.detect_new_entries(current_entries, baseline_entries),
            "removed_entries": self.detect_removed_entries(current_entries, baseline_entries),
            "modified_entries": self.detect_modified_entries(current_entries,baseline_entries),
        }
    
    def detect_new_entries(
            self,
            current_entries: list[PersistenceEntry],
            baseline_entries: list[PersistenceEntry],         
    ) -> list[PersistenceEntry]:
        """ Detect entries that exist now but not in baseline."""
        baseline_ids = {entry.id for entry in baseline_entries}

        return [
            entry 
            for entry in current_entries
            if entry.id not in baseline_ids
        ]
    
    def detect_removed_entries(
            self,
            current_entries: list[PersistenceEntry],
            baseline_entries: list[PersistenceEntry],
    ) -> list[PersistenceEntry]:
        """Detect entries taht existed in baseline but not now."""
        current_ids = {entry.id for entry in current_entries}

        return [
            entry 
            for entry in baseline_entries
            if entry.id not in current_ids
        ]
    
    def detect_modified_entries(
            self,
            current_entries: list[PersistenceEntry],
            baseline_entries: list[PersistenceEntry],
    ) -> list[dict]:
        """Detect entries that exist in both lists but changed."""
        baseline_by_id ={
            entry.id: entry 
            for entry in baseline_entries
        }

        modified_entries = []

        for current_entry in current_entries:
            baseline_entry = baseline_by_id.get(current_entries.id)

            if baseline_entry and self.is_modified(current_entries, baseline_entry):
                modified_entries.append(
                    {
                        "current": current_entry,
                        "baseline": baseline_entry
                    }
                )
        return modified_entries
    
    def is_modified(
            self,
            current_entry: PersistenceEntry,
            baseline_entry: PersistenceEntry,
    ) -> bool:
        """check if and entry changed compared with baseline"""
        return (
            current_entry.command != baseline_entry.command
            or current_entry.path != baseline_entry.path
            or current_entry.sha256 != baseline_entry.sha256
        )
