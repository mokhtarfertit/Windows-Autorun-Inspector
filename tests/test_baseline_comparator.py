from app.analysis.baseline_comparator import BaseLineComparator
from app.analysis.persistence_entry import PersistenceEntry


def test_detect_new_entries():
    """
    Test entries that exist in current scan but not in baseline.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(id="1", name="OneDrive"),
    ]

    current_entries = [
        PersistenceEntry(id="1", name="OneDrive"),
        PersistenceEntry(id="2", name="BadTask"),
    ]

    new_entries = comparator.detect_new_entries(current_entries, baseline_entries)

    assert len(new_entries) == 1
    assert new_entries[0].id == "2"
    assert new_entries[0].name == "BadTask"


def test_detect_removed_entries():
    """
    Test entries that exist in baseline but not in current scan.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(id="1", name="OneDrive"),
        PersistenceEntry(id="2", name="OldUpdater"),
    ]

    current_entries = [
        PersistenceEntry(id="1", name="OneDrive"),
    ]

    removed_entries = comparator.detect_removed_entries(current_entries, baseline_entries)

    assert len(removed_entries) == 1
    assert removed_entries[0].id == "2"
    assert removed_entries[0].name == "OldUpdater"


def test_detect_modified_entries_when_command_changed():
    """
    Test modified entry when command changes.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(
            id="1",
            name="OneDrive",
            command=r"C:\Program Files\OneDrive\OneDrive.exe",
            path=r"C:\Program Files\OneDrive\OneDrive.exe",
            sha256="hash1",
        )
    ]

    current_entries = [
        PersistenceEntry(
            id="1",
            name="OneDrive",
            command=r"C:\Users\mokht\AppData\bad.exe",
            path=r"C:\Program Files\OneDrive\OneDrive.exe",
            sha256="hash1",
        )
    ]

    modified_entries = comparator.detect_modified_entries(current_entries, baseline_entries)

    assert len(modified_entries) == 1
    assert modified_entries[0]["current"].command == r"C:\Users\mokht\AppData\bad.exe"
    assert modified_entries[0]["baseline"].command == r"C:\Program Files\OneDrive\OneDrive.exe"


def test_detect_modified_entries_when_path_changed():
    """
    Test modified entry when executable path changes.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(id="1", name="App", path=r"C:\Program Files\App\app.exe")
    ]

    current_entries = [
        PersistenceEntry(id="1", name="App", path=r"C:\Users\mokht\AppData\app.exe")
    ]

    modified_entries = comparator.detect_modified_entries(current_entries, baseline_entries)

    assert len(modified_entries) == 1


def test_detect_modified_entries_when_hash_changed():
    """
    Test modified entry when SHA-256 hash changes.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(id="1", name="App", sha256="oldhash")
    ]

    current_entries = [
        PersistenceEntry(id="1", name="App", sha256="newhash")
    ]

    modified_entries = comparator.detect_modified_entries(current_entries, baseline_entries)

    assert len(modified_entries) == 1


def test_detect_modified_entries_returns_empty_when_same():
    """
    Test no modified entries when command, path, and hash are the same.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(
            id="1",
            name="App",
            command=r"C:\App\app.exe",
            path=r"C:\App\app.exe",
            sha256="samehash",
        )
    ]

    current_entries = [
        PersistenceEntry(
            id="1",
            name="App",
            command=r"C:\App\app.exe",
            path=r"C:\App\app.exe",
            sha256="samehash",
        )
    ]

    modified_entries = comparator.detect_modified_entries(current_entries, baseline_entries)

    assert modified_entries == []


def test_compare_returns_all_comparison_results():
    """
    Test full comparison result contains new, removed, and modified entries.
    """
    comparator = BaseLineComparator()

    baseline_entries = [
        PersistenceEntry(id="1", name="OneDrive", command="old"),
        PersistenceEntry(id="2", name="RemovedApp"),
    ]

    current_entries = [
        PersistenceEntry(id="1", name="OneDrive", command="new"),
        PersistenceEntry(id="3", name="NewApp"),
    ]

    result = comparator.compare(current_entries, baseline_entries)

    assert len(result["new_entries"]) == 1
    assert result["new_entries"][0].id == "3"

    assert len(result["removed_entries"]) == 1
    assert result["removed_entries"][0].id == "2"

    assert len(result["modified_entries"]) == 1
    assert result["modified_entries"][0]["current"].id == "1"