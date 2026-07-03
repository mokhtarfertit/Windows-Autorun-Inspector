from app.analysis.normalizer import Normalizer
from app.analysis.persistence_entry import PersistenceEntry


def test_normalize_entry_converts_raw_dict_to_persistence_entry():
    """
    Test that one raw collector dictionary becomes one PersistenceEntry.
    """
    normalizer = Normalizer()

    raw_entry = {
        "name": "TestApp",
        "source": "Registry",
        "command": r"C:\Program Files\TestApp\app.exe",
        "timestamp": "2026-07-03T10:00:00+00:00",
        "mitre_technique": "T1547.001",
    }

    entry = normalizer.normalize_entry(raw_entry)

    assert isinstance(entry, PersistenceEntry)
    assert entry.name == "TestApp"
    assert entry.source == "Registry"
    assert entry.command == r"C:\Program Files\TestApp\app.exe"
    assert entry.path == r"C:\Program Files\TestApp\app.exe"
    assert entry.timestamp == "2026-07-03T10:00:00+00:00"
    assert entry.mitre_technique == "T1547.001"
    assert entry.entry_type == "Registry Run Key"
    assert entry.id != ""


def test_normalize_converts_list_of_raw_entries():
    """
    Test that normalize() converts a list of raw dictionaries.
    """
    normalizer = Normalizer()

    raw_entries = [
        {
            "name": "App1",
            "source": "Registry",
            "command": r"C:\App1\app.exe",
        },
        {
            "name": "App2",
            "source": "Startup Folder",
            "path": r"C:\Startup\App2.lnk",
        },
    ]

    entries = normalizer.normalize(raw_entries)

    assert len(entries) == 2
    assert entries[0].name == "App1"
    assert entries[1].name == "App2"
    assert entries[0].entry_type == "Registry Run Key"
    assert entries[1].entry_type == "Startup Folder"


def test_extract_path_from_quoted_command():
    """
    Test extracting path from a quoted command with arguments.
    """
    normalizer = Normalizer()

    path = normalizer.extract_path(
        r'"C:\Program Files\TestApp\app.exe" --start'
    )

    assert path == r"C:\Program Files\TestApp\app.exe"


def test_extract_path_from_unquoted_command_with_arguments():
    """
    Test extracting path from an unquoted command with arguments.
    """
    normalizer = Normalizer()

    path = normalizer.extract_path(
        r"C:\Windows\System32\cmd.exe /c test"
    )

    assert path == r"C:\Windows\System32\cmd.exe"


def test_extract_path_returns_empty_string_when_command_empty():
    """
    Test that empty command returns empty path.
    """
    normalizer = Normalizer()

    assert normalizer.extract_path("") == ""


def test_generate_entry_id_is_stable():
    """
    Test that the same entry always gets the same ID.
    """
    normalizer = Normalizer()

    raw_entry = {
        "name": "TestApp",
        "source": "Registry",
        "command": r"C:\TestApp\app.exe",
    }

    first_entry = normalizer.normalize_entry(raw_entry)
    second_entry = normalizer.normalize_entry(raw_entry)

    assert first_entry.id == second_entry.id


def test_get_entry_type_returns_unknown_for_unknown_source():
    """
    Test that unknown source returns Unknown entry type.
    """
    normalizer = Normalizer()

    raw_entry = {
        "name": "UnknownApp",
        "source": "Something Else",
        "command": r"C:\Unknown\app.exe",
    }

    entry = normalizer.normalize_entry(raw_entry)

    assert entry.entry_type == "Unknown"