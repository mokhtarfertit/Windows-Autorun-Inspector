from app.analysis.persistence_entry import PersistenceEntry

class RiskEnginge:
    """Analyze persistence entries and assign risk score, level, and reasons."""

    def analyze(self, entries: list[PersistenceEntry]) -> list[PersistenceEntry]:
        """Anaylze a list of persistence entries."""

        for entry in entries:
            self.analyze_entry(entry)

        return entries
    
    def analyze_entry(self, entry: PersistenceEntry) -> PersistenceEntry:
        """Analyze one persistence entry"""

        entry.risk_score = self.calculate_score(entry)
        entry.risk_level = self.classify_risk(entry.risk_score)

        return entry

    def calculate_score(self, entry: PersistenceEntry) -> int:
        """Calculate risk score for one persistence entry."""

        score = 0
        entry.reasons = []

        command = entry.command.lower()
        path = entry.path.lower()

        if not path:
            score += 20
            entry.reasons.append("Missing executable path")

        if "temp" in path or "appdata" in path:
            score += 30
            entry.reasons.append("Runs from user-writabel directory")

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
                score += 30
                entry.reasons.append("Uses suspicious command interpreter")
                break

        suspicious_extensions = [
            ".ps1",
            ".vbs",
            ".js",
            ".bat",
            ".cmd",
        ]

        for extension in suspicious_extensions:
            if path.endswith(extension):
                score += 25
                entry.reasons.append("Runs script file from autorun location")
                break

        if "executionpolicy bypass" in command or "-enc" in command:
            score += 40
            entry.reasons.append("Uses suspicious PowerShell options")

        return score

    def classify_risk(self, score: int) -> str:
        """Convert risk score into risk level."""
        if score >= 80:
            return "Critical"

        if score >= 50:
            return "High"

        if score >= 20:
            return "Medium"

        return "Low"