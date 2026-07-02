from pathlib import Path

from app.collectors.base_collector import BaseCollector
from app.utils.time_utils import timestamp_to_iso

class StartupCollector(BaseCollector):
    """Scan windows Startup folders for autorun files."""

    def __init__(self):
        super().__init__(source_name="Startup Folder", mitre_technique="T1547.001")
        # this for sepecific this user.
        self.user_startup_path = (
            Path.home()
            / "AppData"
            / "Roaming"
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs"
            / "Startup"
        )
        # this for take any user in this machine 
        self.system_startup_path = Path(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
        )
    def collect(self):
        entries = []

        entries.extend(self.scan_folder(self.user_startup_path))
        entries.extend(self.scan_folder(self.system_startup_path))

        return entries
    
    def scan_folder(self,folder_path):
        entries = []

        if not folder_path.exists():
            return entries
        
        for item in folder_path.iterdir():
            if item.is_file():
                entries.append(
                    {
                        "name":item.name,
                        "command": str(item),
                        "path": str(item),
                        "source": self.source_name,
                        "startup_folder": str(folder_path),
                        "timestamp": timestamp_to_iso(item.stat().st_mtime),
                        "mitre_technique":self.mitre_technique,
                    }
                )
        return entries