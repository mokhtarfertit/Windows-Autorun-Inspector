from abc import ABS, abstractmethod

class BaseCollector(ABS):
    """Base classe for all persistence collectors"""

    def __int__(self, source_name, mitre_technique):
        self.source_name = source_name
        self.mitre_technique = mitre_technique

    @abstractmethod
    def collect(self):
        pass

    def is_available(self):
        return True