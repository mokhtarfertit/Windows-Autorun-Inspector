from app.analysis.persistence_entry import PersistenceEntry
from app.analysis.risk_rule import RiskRule

class RiskEngine:
    """Analyze persistence entries and assign risk score, level, and reasons."""
    def __init__(self):
        """Create risk rules used by the engine."""
        self.rules = [
            RiskRule(
                name="Missing executable path",
                description="Entry does not have an executable path",
                score = 20,
                check_function= self.is_missing_path,
            ),
            RiskRule(
                name="User-writable directory",
                description="Entry runs from temp or AppData directory",
                score=30,
                check_function= self.is_user_wrtiable_path,
            ),
            RiskRule(
                name="Suspicious command interpreter",
                description="Entry uses suspicious command interpreter",
                score=30,
                check_function=self.uses_suspicious_command,
            ),
            RiskRule(
                name="Suspicous PowerShell options",
                description="Entry uses suspicious PowerShell options",
                score=40,
                check_function=self.uses_suspicious_powershell_options,
            ),
        ]


    def analyze(self, entries: list[PersistenceEntry]) -> list[PersistenceEntry]:
        """Anaylze a list of persistence entries."""

        for entry in entries:
            self.analyze_entry(entry)

        return entries
    
    def analyze_entry(self, entry: PersistenceEntry) -> PersistenceEntry:
        """Analyze one persistence entry"""
        entry.risk_score = 0
        entry.reasons = []

        for rule in self.rules:
            if rule.check(entry):
                entry.risk_score += rule.score
                entry.reasons.append(rule.description)

        entry.risk_level = self.classify_risk(entry.risk_score)

        return entry

    def classify_risk(self, score: int) -> str:
        """Convert risk score into risk level."""
        if score >= 80:
            return "Critical"

        if score >= 50:
            return "High"

        if score >= 20:
            return "Medium"

        return "Low"
    
    def is_missing_path(self, entry: PersistenceEntry) -> bool:
        """Check if the entry has no executable path."""
        return entry.path == ""
    
    def is_user_wrtiable_path(self, entry: PersistenceEntry) -> bool:
        """check if the entry runs from a user-writable directory."""
        path = entry.path.lower()

        return "temp" in path or "appdata" in path
    
    def uses_suspicious_command(self, entry: PersistenceEntry) -> bool:
        """check if the entry uses a suspicious command interpreter."""

        command = entry.command.lower()

        suspicious_commands = [
            "powershell",
            "cmd.exe",
            "wscript",
            "cscript",
            "mshta",
            "regsvr32",
            "rundll32",
        ]

        for suspicious_command in suspicious_commands:
            if suspicious_command in command:
                return True
        return False
    
    def uses_script_file(self, entry: PersistenceEntry) -> bool:
        """check if the entry runs a script file."""

        path= entry.path.lower()

        suspicious_extensions = [
            ".ps1",
            ".vbs",
            ".js",
            ".bat",
            ".cmd",
        ]

        for extenstion in suspicious_extensions:
            if path.endswith(extenstion):
                return True
            
        return False
    
    def uses_suspicious_powershell_options(self,entry: PersistenceEntry) -> bool:
        """cehck if the entry sues suspicious PowerShell options."""
        command = entry.command.lower()

        return "executionpolicy bypass" in command or "-enc" in command
