import subprocess

class PowerShellRunner:
    """Run PowerShell commands and return command output."""

    def run(self, command):
        try :
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    command,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return ""
            
            return result.stdout
        except FileNotFoundError:
            return ""
