from app.collectors.tasks_collector import TaskCollector


def test_parse_task_output_returns_task_entries():
    """
    Test that TaskCollector converts PowerShell JSON output
    into persistence entry dictionaries.
    """
    collector = TaskCollector()

    fake_output = """
    [
        {
            "TaskName": "TestTask",
            "TaskPath": "\\\\",
            "State": 3
        }
    ]
    """

    entries = collector.parse_task_output(fake_output)

    assert len(entries) == 1
    assert entries[0]["name"] == "TestTask"
    assert entries[0]["path"] == "\\"
    assert entries[0]["source"] == "Scheduled Task"
    assert entries[0]["state"] == 3
    assert entries[0]["mitre_technique"] == "T1053.005"


def test_parse_task_output_returns_empty_list_when_output_empty():
    """
    Test that empty PowerShell output returns an empty list.
    """
    collector = TaskCollector()

    entries = collector.parse_task_output("")

    assert entries == []


def test_parse_task_output_returns_empty_list_when_json_invalid():
    """
    Test that invalid JSON does not crash the collector.
    """
    collector = TaskCollector()

    entries = collector.parse_task_output("not valid json")

    assert entries == []


def test_collect_uses_powershell_runner(monkeypatch):
    """
    Test collect() without running real PowerShell.

    We replace powershell_runner.run() with a fake function
    that returns controlled JSON output.
    """
    collector = TaskCollector()

    def fake_run(command):
        return """
        {
            "TaskName": "FakeTask",
            "TaskPath": "\\\\Microsoft\\\\",
            "State": 3
        }
        """

    monkeypatch.setattr(collector.powershell_runner, "run", fake_run)

    entries = collector.collect()

    assert len(entries) == 1
    assert entries[0]["name"] == "FakeTask"
    assert entries[0]["path"] == "\\Microsoft\\"