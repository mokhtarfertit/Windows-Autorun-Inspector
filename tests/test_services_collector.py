from app.collectors.services_collector import ServiceCollector


def test_parse_service_output_returns_service_entries():
    """
    Test that ServiceCollector converts PowerShell JSON output
    into persistence entry dictionaries.
    """
    collector = ServiceCollector()

    fake_output = """
    [
        {
            "Name": "TestService",
            "DisplayName": "Test Service",
            "State": "Running",
            "StartMode": "Auto",
            "PathName": "C:\\\\Program Files\\\\TestService\\\\service.exe"
        }
    ]
    """

    entries = collector.parse_service_output(fake_output)

    assert len(entries) == 1
    assert entries[0]["name"] == "TestService"
    assert entries[0]["display_name"] == "Test Service"
    assert entries[0]["command"] == "C:\\Program Files\\TestService\\service.exe"
    assert entries[0]["path"] == "C:\\Program Files\\TestService\\service.exe"
    assert entries[0]["source"] == "Windows Service"
    assert entries[0]["state"] == "Running"
    assert entries[0]["start_mode"] == "Auto"
    assert entries[0]["mitre_technique"] == "T1543.003"


def test_parse_service_output_returns_empty_list_when_output_empty():
    """
    Test that empty PowerShell output returns an empty list.
    """
    collector = ServiceCollector()

    entries = collector.parse_service_output("")

    assert entries == []


def test_parse_service_output_returns_empty_list_when_json_invalid():
    """
    Test that invalid JSON does not crash the collector.
    """
    collector = ServiceCollector()

    entries = collector.parse_service_output("not valid json")

    assert entries == []


def test_collect_uses_powershell_runner(monkeypatch):
    """
    Test collect() without running real PowerShell.

    We replace powershell_runner.run() with a fake function
    that returns controlled JSON output.
    """
    collector = ServiceCollector()

    def fake_run(command):
        return """
        {
            "Name": "FakeService",
            "DisplayName": "Fake Service",
            "State": "Stopped",
            "StartMode": "Manual",
            "PathName": "C:\\\\Fake\\\\service.exe"
        }
        """

    monkeypatch.setattr(collector.powershell_runner, "run", fake_run)

    entries = collector.collect()

    assert len(entries) == 1
    assert entries[0]["name"] == "FakeService"
    assert entries[0]["display_name"] == "Fake Service"
    assert entries[0]["path"] == "C:\\Fake\\service.exe"