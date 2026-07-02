from app.collectors.startup_collector import StartupCollector


def test_startup_collector_reads_startup_files(tmp_path):
    """
    Test that StartupCollector finds files inside startup folders.

    We do not use the real Windows Startup folder.
    tmp_path creates a fake temporary folder for the test.
    """
    user_startup = tmp_path / "user_startup"
    system_startup = tmp_path / "system_startup"

    user_startup.mkdir()
    system_startup.mkdir()

    test_file = user_startup / "TestApp.lnk"
    test_file.write_text("fake shortcut content")

    collector = StartupCollector()

    collector.user_startup_path = user_startup
    collector.system_startup_path = system_startup

    entries = collector.collect()

    assert len(entries) == 1
    assert entries[0]["name"] == "TestApp.lnk"
    assert entries[0]["path"] == str(test_file)
    assert entries[0]["source"] == "Startup Folder"
    assert entries[0]["timestamp"] != ""


def test_startup_collector_returns_empty_list_when_folder_missing(tmp_path):
    """
    Test that StartupCollector does not crash if startup folder does not exist.
    """
    missing_user_startup = tmp_path / "missing_user_startup"
    missing_system_startup = tmp_path / "missing_system_startup"

    collector = StartupCollector()

    collector.user_startup_path = missing_user_startup
    collector.system_startup_path = missing_system_startup

    entries = collector.collect()

    assert entries == []