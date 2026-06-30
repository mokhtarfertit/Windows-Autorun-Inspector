import json
import subprocess

from app.collectors.base_collector import BaseCollector

class ServiceCollector(BaseCollector):
    """Scan windows services for autorun entries."""

    def __init__(self):
            super().__init__(
                source_name= "Windows Service",
                mitre_technique="T1543.003",
                )
            self.powershell_command = [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Service | Select-Object Name,DisplayName,State,StartMode,PathName | ConvertTo-Json",
            ]

    def collect(self):
            output = self.run_powershell_command()
            return self.parse_service_output(output)
        
    def run_powershell_command(self):
            try:
                result = subprocess.run(
                    self.powershell_command,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                # If it works, return the JSON text.
                if result.returncode != 0 :
                    return ""
                
                return result.stdout
            
            except FileNotFoundError:
                return ""
    # This converts PowerShell JSON text into Python dictionaries.     
    def parse_service_output(self,output):
            entries = []

            if not output:
                return entries
            
            try:
                services = json.load(output)
            except json.JSONDecodeError:
                return entries
            
            if isinstance(services, dict):
                services = [services]

            for service in services:
                name = service.get("Name", "")
                display_name = service.get("DisplayName", "")
                state = service.get("State", "")
                start_mode = service.get("StartMode", "")
                path_name = service.get("PathName", "")

                entries.append(
                    {
                        "name": name,
                        "display_name": display_name,
                        "command": path_name,
                        "path": path_name,
                        "source": self.source_name,
                        "state": state,
                        "start_mode": start_mode,
                        "mitre_technique": self.mitre_technique,
                    }
                )

            return entries

