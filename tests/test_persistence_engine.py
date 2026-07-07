from app.analysis.scan_result import ScanResult
from app.core.persistence_engine import PersistenceEngine


class FakeCollector:
    """
    Fake collector used to test PersistenceEngine without touching Windows.
    """

    def __init__(self, entries=None, available=True):
        self.entries = entries or []
        self.available = available

    def is_available(self):
        return self.available

    def collect(self):
        return self.entries


class BrokenCollector:
    """
    Fake collector that raises an error.
    Used to verify the engine continues safely.
    """

    def is_available(self):
        return True

    def collect(self):
        raise RuntimeError("Collector failed")


def test_scan_returns_scan_result():
    """
    Test that scan() returns a ScanResult.
    """
    engine = PersistenceEngine()

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "TestApp",
                    "source": "Registry",
                    "command": r"C:\TestApp\app.exe",
                    "path": r"C:\TestApp\app.exe",
                }
            ]
        )
    ]

    result = engine.scan()

    assert isinstance(result, ScanResult)
    assert result.status == "success"


def test_scan_collects_normalizes_and_analyzes_entries():
    """
    Test that scan() runs collection, normalization, and risk analysis.
    """
    engine = PersistenceEngine()

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "BadEntry",
                    "source": "Registry",
                    "command": r"powershell.exe -ExecutionPolicy Bypass",
                    "path": "powershell.exe",
                }
            ]
        )
    ]

    result = engine.scan()

    assert result.total_entries == 1
    assert result.entries[0].name == "BadEntry"
    assert result.entries[0].risk_score == 70
    assert result.entries[0].risk_level == "High"


def test_scan_skips_unavailable_collectors():
    """
    Test that unavailable collectors are ignored.
    """
    engine = PersistenceEngine()

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "ShouldNotAppear",
                    "source": "Registry",
                    "command": r"C:\App\app.exe",
                    "path": r"C:\App\app.exe",
                }
            ],
            available=False,
        )
    ]

    result = engine.scan()

    assert result.total_entries == 0
    assert result.entries == []


def test_scan_continues_when_collector_fails():
    """
    Test that one broken collector does not stop the full scan.
    """
    engine = PersistenceEngine()

    engine.collectors = [
        BrokenCollector(),
        FakeCollector(
            entries=[
                {
                    "name": "GoodEntry",
                    "source": "Registry",
                    "command": r"C:\Good\good.exe",
                    "path": r"C:\Good\good.exe",
                }
            ]
        ),
    ]

    result = engine.scan()

    assert result.total_entries == 1
    assert result.entries[0].name == "GoodEntry"


def test_create_baseline_saves_entries(tmp_path):
    """
    Test that create_baseline() scans and saves baseline entries.
    """
    engine = PersistenceEngine()

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "BaselineApp",
                    "source": "Registry",
                    "command": r"C:\Baseline\app.exe",
                    "path": r"C:\Baseline\app.exe",
                }
            ]
        )
    ]

    baseline_path = tmp_path / "baseline.json"
    engine.baseline_store.baseline_path = baseline_path

    result = engine.create_baseline()

    assert result is True
    assert baseline_path.exists()


def test_compare_with_baseline_returns_comparison(tmp_path):
    """
    Test that compare_with_baseline() compares current scan with saved baseline.
    """
    engine = PersistenceEngine()

    baseline_path = tmp_path / "baseline.json"
    engine.baseline_store.baseline_path = baseline_path

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "OldApp",
                    "source": "Registry",
                    "command": r"C:\Old\old.exe",
                    "path": r"C:\Old\old.exe",
                }
            ]
        )
    ]

    engine.create_baseline()

    engine.collectors = [
        FakeCollector(
            entries=[
                {
                    "name": "OldApp",
                    "source": "Registry",
                    "command": r"C:\Old\old.exe",
                    "path": r"C:\Old\old.exe",
                },
                {
                    "name": "NewApp",
                    "source": "Registry",
                    "command": r"C:\New\new.exe",
                    "path": r"C:\New\new.exe",
                },
            ]
        )
    ]

    comparison = engine.compare_with_baseline()

    assert len(comparison["new_entries"]) == 1
    assert comparison["new_entries"][0].name == "NewApp"


def test_generate_report_returns_report_path(tmp_path):
    """
    Test that generate_report() creates a report file.
    """
    engine = PersistenceEngine()

    engine.report_generator.output_dir = tmp_path

    result = ScanResult(status="success")

    report_path = engine.generate_report(result, "json")

    assert report_path != ""
    assert (tmp_path / "scan_result.json").exists()


def test_generate_report_returns_empty_string_for_unknown_format():
    """
    Test that unknown report format returns empty string.
    """
    engine = PersistenceEngine()

    result = ScanResult(status="success")

    report_path = engine.generate_report(result, "xml")

    assert report_path == ""