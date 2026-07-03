from app.analysis.persistence_entry import PersistenceEntry


def test_persistence_entry_default_values():
    """
    Test that PersistenceEntry has safe default values.
    """
    entry = PersistenceEntry()

    assert entry.id == ""
    assert entry.name == ""
    assert entry.entry_type == ""
    assert entry.source == ""
    assert entry.command == ""
    assert entry.path == ""
    assert entry.timestamp == ""
    assert entry.publisher == ""
    assert entry.sha256 == ""
    assert entry.mitre_technique == ""
    assert entry.risk_score == 0
    assert entry.risk_level == "Low"
    assert entry.reasons == []


def test_persistence_entry_custom_values():
    """
    Test that PersistenceEntry stores values passed to it.
    """
    entry = PersistenceEntry(
        id="abc123",
        name="TestApp",
        entry_type="Registry Run Key",
        source="Registry",
        command=r"C:\Program Files\TestApp\app.exe",
        path=r"C:\Program Files\TestApp\app.exe",
        timestamp="2026-07-03T10:00:00+00:00",
        publisher="Test Publisher",
        sha256="fakehash",
        mitre_technique="T1547.001",
        risk_score=50,
        risk_level="Medium",
        reasons=["Runs from autorun registry key"],
    )

    assert entry.id == "abc123"
    assert entry.name == "TestApp"
    assert entry.entry_type == "Registry Run Key"
    assert entry.source == "Registry"
    assert entry.command == r"C:\Program Files\TestApp\app.exe"
    assert entry.path == r"C:\Program Files\TestApp\app.exe"
    assert entry.timestamp == "2026-07-03T10:00:00+00:00"
    assert entry.publisher == "Test Publisher"
    assert entry.sha256 == "fakehash"
    assert entry.mitre_technique == "T1547.001"
    assert entry.risk_score == 50
    assert entry.risk_level == "Medium"
    assert entry.reasons == ["Runs from autorun registry key"]


def test_persistence_entry_to_dict():
    """
    Test that PersistenceEntry can be converted to a dictionary.
    """
    entry = PersistenceEntry(
        id="abc123",
        name="TestApp",
        source="Registry",
        command=r"C:\Program Files\TestApp\app.exe",
        risk_score=50,
        risk_level="Medium",
        reasons=["Test reason"],
    )

    data = entry.to_dict()

    assert data["id"] == "abc123"
    assert data["name"] == "TestApp"
    assert data["source"] == "Registry"
    assert data["command"] == r"C:\Program Files\TestApp\app.exe"
    assert data["risk_score"] == 50
    assert data["risk_level"] == "Medium"
    assert data["reasons"] == ["Test reason"]


def test_persistence_entry_reasons_are_not_shared():
    """
    Test that each PersistenceEntry has its own reasons list.

    This is important because reasons is a list.
    One entry's reasons should not affect another entry.
    """
    first_entry = PersistenceEntry()
    second_entry = PersistenceEntry()

    first_entry.reasons.append("First reason")

    assert first_entry.reasons == ["First reason"]
    assert second_entry.reasons == []