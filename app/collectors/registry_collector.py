import winreg


class RegistryCollector:
    """""to scan Windows Registry autorun locations and return the programs 
    that start automatically when Windows starts or when the user logs in."""""
    def __init__(self):
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
            with winreg.OpenKey(root_key, registry_path) as key:
                index = 0

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