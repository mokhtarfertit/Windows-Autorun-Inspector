import winreg
from datetime import datetime, timedelta, timezone

from app.collectors.base_collector import BaseCollector


class RegistryCollector:
    """""to scan Windows Registry autorun locations and return the programs 
    that start automatically when Windows starts or when the user logs in."""""
    def __init__(self):
        super().__init__(source_name = "Registry",mitre_technique="T1060 /T1547.001")
        self.registry_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        ]
    
    def collect(self):
        entries = []

        for root_key, registry_path in self.registry_paths:
            entries.extend(self.read_run_key(root_key, registry_path))

        return entries
    
    def read_run_key(self, root_key, registry_path):
        entries = []

        try:
            # opens one registry autorun location.
            with winreg.OpenKey(root_key, registry_path) as key:
                index = 0
                timestamp = self.get_key_last_modified(root_key, registry_path)

                while True:
                    try:
                        name, command, value_type = winreg.EnumValue(key, index)

                        entries.append(
                            {
                                "name": name,
                                "command": command,
                                "source": "Registry",
                                "registry_path": registry_path,
                                "value_type": value_type,
                                "timestamp": timestamp,
                            }
                        )

                        index += 1

                    except OSError:
                        break

        except FileNotFoundError:
            pass
        except PermissionError:
            pass

        return entries
    
    def get_key_last_modified(self, root_key, registry_path):
        try:
            with winreg.OpenKey(root_key,registry_path) as key:
                key_info = winreg.QueryInfoKey(key)
                last_modified = key_info[2]

                windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
                modified_time = windows_epoch + timedelta(microseconds=last_modified/ 10)

                return modified_time.isoformat()
            
        except FileNotFoundError:
            return ""
        except PermissionError:
            return ""
        