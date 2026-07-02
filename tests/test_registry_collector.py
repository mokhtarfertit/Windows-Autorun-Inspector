from app.collectors.registry_collector import RegistryCollector
from app.collectors import registry_collector


class FakeRegistryKey:
    """Fake registry key object used to simulate winreg.OpenKey context manager."""

    def __enter__(self):
        """Return fake key when used inside a with statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close fake key context without doing anything."""
        pass


def test_read_run_key_returns_registry_entries(monkeypatch):
    """
    Test that RegistryCollector can read one registry autorun entry.

    This test does not access the real Windows Registry.
    It replaces winreg functions with fake versions.
    """
    def fake_open_key(root_key, registry_path):
        return FakeRegistryKey()

    def fake_query_info_key(key):
        # Index 2 is the registry key last modified time.
        return (0, 1, 132537600000000000)

    def fake_enum_value(key, index):
        # First value exists.
        if index == 0:
            return ("TestApp", r"C:\Program Files\TestApp\app.exe", 1)

        # OSError tells the collector there are no more values.
        raise OSError

    monkeypatch.setattr(registry_collector.winreg, "OpenKey", fake_open_key)
    monkeypatch.setattr(registry_collector.winreg, "QueryInfoKey", fake_query_info_key)
    monkeypatch.setattr(registry_collector.winreg, "EnumValue", fake_enum_value)

    collector = RegistryCollector()

    entries = collector.read_run_key(
        registry_collector.winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
    )

    assert len(entries) == 1
    assert entries[0]["name"] == "TestApp"
    assert entries[0]["command"] == r"C:\Program Files\TestApp\app.exe"
    assert entries[0]["source"] == "Registry"
    assert entries[0]["registry_path"] == r"Software\Microsoft\Windows\CurrentVersion\Run"
    assert entries[0]["value_type"] == 1
    assert entries[0]["timestamp"] != ""


def test_read_run_key_returns_empty_list_when_key_missing(monkeypatch):
    """
    Test that missing registry keys are handled safely.

    If a Run key does not exist, the collector should return an empty list,
    not crash.
    """
    def fake_open_key(root_key, registry_path):
        raise FileNotFoundError

    monkeypatch.setattr(registry_collector.winreg, "OpenKey", fake_open_key)

    collector = RegistryCollector()

    entries = collector.read_run_key(
        registry_collector.winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
    )

    assert entries == []


def test_read_run_key_returns_empty_list_when_permission_denied(monkeypatch):
    """
    Test that permission errors are handled safely.

    Some registry keys may require administrator access.
    If access is denied, the collector should return an empty list.
    """
    def fake_open_key(root_key, registry_path):
        raise PermissionError

    monkeypatch.setattr(registry_collector.winreg, "OpenKey", fake_open_key)

    collector = RegistryCollector()

    entries = collector.read_run_key(
        registry_collector.winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
    )

    assert entries == []