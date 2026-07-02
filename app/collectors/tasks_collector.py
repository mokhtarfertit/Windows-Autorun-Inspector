import json

from app.collectors.base_collector import BaseCollector
from app.utils.powershell_runner import PowerShellRunner

class TaskCollector(BaseCollector):
    """Scan Windows Scheduled Tasks for autorun entries."""

    def __init__(self):
        super().__init__(source_name="Scheduled Task", mitre_technique="T1053.005")
        self.powershell_runner = PowerShellRunner()
        self.powershell_command = "Get-ScheduledTask | Select-Object TaskName,TaskPath,State | ConvertTo-Json"

    def collect(self):
        output = self.powershell_runner.run(self.powershell_command)
        return self.parse_task_output(output)
    
        
    def parse_task_output(self,output):
        entries = []

        if not output:
            return entries
        
        try:
            tasks = json.loads(output)
        except json.JSONDecodeError:
            return entries
        
        if isinstance(tasks, dict):
            tasks = [tasks]

        for task in tasks:
            task_name = task.get("TaskName", "")
            task_path = task.get("TaskPath", "")
            state = task.get("State", "")
        
            entries.append(
                {
                    "name": task_name,
                    "command": "",
                    "path": task_path,
                    "source": self.source_name,
                    "state": state,
                    "timestamp": "",
                    "mitre_technique": self.mitre_technique,
                }
            )
        
        return entries

            