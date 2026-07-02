import json

from app.collectors.base_collector import BaseCollector
from app.utils.powershell_runner import PowerShellRunner

class ServiceCollector(BaseCollector):
    """Scan windows services for autorun entries."""

    def __init__(self):
            super().__init__(
                source_name= "Windows Service",
                mitre_technique="T1543.003"
                )
            self.powershell_runner = PowerShellRunner()
            self.powershell_command ="Get-CimInstance Win32_Service | Select-Object Name,DisplayName,State,StartMode,PathName | ConvertTo-Json"
            

    def collect(self):
            output = self.powershell_runner.run(self.powershell_command)
            return self.parse_service_output(output)
        
    
    # This converts PowerShell JSON text into Python dictionaries.     
    def parse_service_output(self,output):
            entries = []

            if not output:
                return entries
            
            try:
                services = json.loads(output)
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
                        "timestamp": "",
                        "mitre_technique": self.mitre_technique,
                    }
                )

            return entries

