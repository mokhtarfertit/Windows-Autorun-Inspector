from app.analysis.persistence_entry import PersistenceEntry
from app.analysis.scan_result import ScanResult


def test_scan_result_default_values():
    """
    Test that ScanResult has safe default values.
    """
    result = ScanResult()

    assert result.scan_time == ""
    assert result.total_entries == 0
    assert result.low_count == 0
    assert result.medium_count == 0
    assert result.high_count == 0
    assert result.critical_count == 0
    assert result.entries == []
    assert result.status == "success"


def test_scan_result_calculate_counts():
    """
    Test that ScanResult calculates risk counters from entries.
    """
    entries = [
        PersistenceEntry(name="LowApp", risk_level="Low"),
        PersistenceEntry(name="MediumApp", risk_level="Medium"),
        PersistenceEntry(name="HighApp", risk_level="High"),
        PersistenceEntry(name="CriticalApp", risk_level="Critical"),
        PersistenceEntry(name="AnotherLowApp", risk_level="Low"),
    ]

    result = ScanResult(entries=entries)

    result.calculate_counts()

    assert result.total_entries == 5
    assert result.low_count == 2
    assert result.medium_count == 1
    assert result.high_count == 1
    assert result.critical_count == 1


def test_scan_result_to_dict():
    """
    Test that ScanResult can be converted to a dictionary.
    """
    entry = PersistenceEntry(
        id="abc123",
        name="TestApp",
        source="Registry",
        risk_level="High",
    )

    result = ScanResult(
        scan_time="2026-07-03T10:00:00+00:00",
        entries=[entry],
        status="success",
    )

    result.calculate_counts()

    data = result.to_dict()

    assert data["scan_time"] == "2026-07-03T10:00:00+00:00"
    assert data["total_entries"] == 1
    assert data["high_count"] == 1
    assert data["status"] == "success"
    assert data["entries"][0]["id"] == "abc123"
    assert data["entries"][0]["name"] == "TestApp"


def test_scan_result_entries_are_not_shared():
    """
    Test that each ScanResult has its own entries list.
    """
    first_result = ScanResult()
    second_result = ScanResult()

    first_result.entries.append(PersistenceEntry(name="TestApp"))

    assert len(first_result.entries) == 1
    assert second_result.entries == []