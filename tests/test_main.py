from app.analysis.persistence_entry import PersistenceEntry
from app.analysis.scan_result import ScanResult
from app import main as app_main


class FakePersistenceEngine:
    """
    Fake engine used to test CLI without running real collectors.
    """

    def scan(self):
        entry = PersistenceEntry(
            name="TestApp",
            risk_level="Medium",
        )

        result = ScanResult(
            scan_time="2026-07-07T10:00:00+00:00",
            entries=[entry],
            status="success",
        )

        result.calculate_counts()

        return result

    def create_baseline(self):
        return True

    def compare_with_baseline(self):
        return {
            "new_entries": [PersistenceEntry(name="NewApp")],
            "removed_entries": [],
            "modified_entries": [],
        }

    def generate_report(self, result, report_format="json"):
        return f"reports/scan_result.{report_format}"


def test_main_prints_usage_when_no_command(monkeypatch, capsys):
    """
    Test that CLI prints usage when no command is provided.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main"])

    app_main.main()

    captured = capsys.readouterr()

    assert "Windows Autorun Inspector" in captured.out
    assert "python -m app.main scan" in captured.out


def test_main_scan_command(monkeypatch, capsys):
    """
    Test scan command prints scan summary.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "scan"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "Scan time: 2026-07-07T10:00:00+00:00" in captured.out
    assert "Total entries: 1" in captured.out
    assert "Medium: 1" in captured.out


def test_main_create_baseline_command(monkeypatch, capsys):
    """
    Test create-baseline command.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "create-baseline"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "Baseline created successfully" in captured.out


def test_main_compare_command(monkeypatch, capsys):
    """
    Test compare command.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "compare"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "New entries: 1" in captured.out
    assert "Removed entries: 0" in captured.out
    assert "Modified entries: 0" in captured.out


def test_main_report_json_command(monkeypatch, capsys):
    """
    Test report-json command.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "report-json"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "JSON report: reports/scan_result.json" in captured.out


def test_main_report_csv_command(monkeypatch, capsys):
    """
    Test report-csv command.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "report-csv"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "CSV report: reports/scan_result.csv" in captured.out


def test_main_report_html_command(monkeypatch, capsys):
    """
    Test report-html command.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "report-html"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "HTML report: reports/scan_result.html" in captured.out


def test_main_unknown_command_prints_usage(monkeypatch, capsys):
    """
    Test unknown command prints usage.
    """
    monkeypatch.setattr(app_main.sys, "argv", ["app.main", "unknown"])
    monkeypatch.setattr(app_main, "PersistenceEngine", FakePersistenceEngine)

    app_main.main()

    captured = capsys.readouterr()

    assert "Windows Autorun Inspector" in captured.out
    assert "Usage:" in captured.out