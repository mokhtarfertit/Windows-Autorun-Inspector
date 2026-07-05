from app.analysis.persistence_entry import PersistenceEntry
from app.storage.baseline_store import BaselineStore


def test_baseline_store_save_creates_file(tmp_path):
    """
    Test that save() creates a baseline JSON file.
    """
    baseline_path = tmp_path / "baseline.json"
    store = BaselineStore(str(baseline_path))

    entries = [
        PersistenceEntry(
            id="abc123",
            name="TestApp",
            source="Registry",
            command=r"C:\TestApp\app.exe",
            path=r"C:\TestApp\app.exe",
        )
    ]

    result = store.save(entries)

    assert result is True
    assert baseline_path.exists()


def test_baseline_store_load_returns_entries(tmp_path):
    """
    Test that load() returns PersistenceEntry objects from baseline file.
    """
    baseline_path = tmp_path / "baseline.json"
    store = BaselineStore(str(baseline_path))

    entries = [
        PersistenceEntry(
            id="abc123",
            name="TestApp",
            source="Registry",
            command=r"C:\TestApp\app.exe",
            path=r"C:\TestApp\app.exe",
            risk_score=30,
            risk_level="Medium",
            reasons=["Test reason"],
        )
    ]

    store.save(entries)

    loaded_entries = store.load()

    assert len(loaded_entries) == 1
    assert isinstance(loaded_entries[0], PersistenceEntry)
    assert loaded_entries[0].id == "abc123"
    assert loaded_entries[0].name == "TestApp"
    assert loaded_entries[0].risk_score == 30
    assert loaded_entries[0].risk_level == "Medium"
    assert loaded_entries[0].reasons == ["Test reason"]


def test_baseline_store_load_returns_empty_list_when_file_missing(tmp_path):
    """
    Test that load() returns empty list if baseline file does not exist.
    """
    baseline_path = tmp_path / "missing_baseline.json"
    store = BaselineStore(str(baseline_path))

    loaded_entries = store.load()

    assert loaded_entries == []


def test_baseline_store_exists_returns_true_when_file_exists(tmp_path):
    """
    Test that exists() returns True when baseline file exists.
    """
    baseline_path = tmp_path / "baseline.json"
    store = BaselineStore(str(baseline_path))

    entries = [PersistenceEntry(name="TestApp")]

    store.save(entries)

    assert store.exists() is True


def test_baseline_store_exists_returns_false_when_file_missing(tmp_path):
    """
    Test that exists() returns False when baseline file does not exist.
    """
    baseline_path = tmp_path / "missing_baseline.json"
    store = BaselineStore(str(baseline_path))

    assert store.exists() is False


def test_baseline_store_load_returns_empty_list_for_invalid_json(tmp_path):
    """
    Test that invalid JSON does not crash load().
    """
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text("not valid json", encoding="utf-8")

    store = BaselineStore(str(baseline_path))

    loaded_entries = store.load()

    assert loaded_entries == []