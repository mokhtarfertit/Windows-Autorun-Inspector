import subprocess
import json

from app.collectors.base_collector import BaseCollector

class TaskCollector(BaseCollector):
    """Scan Windows Scheduled Tasks for autorun entries."""

    def __init__(self):
        super().__init__(source_name="Scheduled Task", mitre_technique="T1053.005")
        self.powershell_command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get_scheduledTask | Select-object TaskName, TaskPath, State | convertTo-Json ",
        ]

    def collect(self):
        output = self.run_powershell_command()
        return self.parse_task_output(output)
    
    def run_powershell_command(self):
        try:
            result = subprocess.run(
                self.powershell_command,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return ""
            
            return result.stdout
        except FileNotFoundError:
            return ""
        
    def parse_tak_output(self,output):
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
            task_path = task.get("task_path","")
            state = task.get("State", "")
        
            entries.append(
                {
                    "name": task_name,
                    "command": "",
                    "path": task_path,
                    "source": self.source_name,
                    "state": state,
                    "mitre_technique": self.mitre_technique,
                }
            )
        
        return entries

            