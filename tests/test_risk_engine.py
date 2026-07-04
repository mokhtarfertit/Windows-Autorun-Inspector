from app.analysis.persistence_entry import PersistenceEntry
from app.analysis.risk_engine import RiskEngine


def test_classify_risk_returns_low():
    """
    Test that score below 20 is Low risk.
    """
    engine = RiskEngine()

    assert engine.classify_risk(0) == "Low"
    assert engine.classify_risk(19) == "Low"


def test_classify_risk_returns_medium():
    """
    Test that score from 20 to 49 is Medium risk.
    """
    engine = RiskEngine()

    assert engine.classify_risk(20) == "Medium"
    assert engine.classify_risk(49) == "Medium"


def test_classify_risk_returns_high():
    """
    Test that score from 50 to 79 is High risk.
    """
    engine = RiskEngine()

    assert engine.classify_risk(50) == "High"
    assert engine.classify_risk(79) == "High"


def test_classify_risk_returns_critical():
    """
    Test that score 80 or higher is Critical risk.
    """
    engine = RiskEngine()

    assert engine.classify_risk(80) == "Critical"
    assert engine.classify_risk(100) == "Critical"


def test_missing_path_rule_adds_score_and_reason():
    """
    Test that missing path increases risk score.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="NoPathEntry",
        command="",
        path="",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 20
    assert analyzed_entry.risk_level == "Medium"
    assert "Entry does not have an executable path" in analyzed_entry.reasons


def test_user_writable_path_rule_adds_score_and_reason():
    """
    Test that Temp or AppData path increases risk score.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="AppDataEntry",
        command=r"C:\Users\mokht\AppData\bad.exe",
        path=r"C:\Users\mokht\AppData\bad.exe",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 30
    assert analyzed_entry.risk_level == "Medium"
    assert "Entry runs from Temp or AppData directory" in analyzed_entry.reasons


def test_suspicious_command_rule_adds_score_and_reason():
    """
    Test that suspicious command interpreter increases risk score.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="PowerShellEntry",
        command="powershell.exe -NoProfile",
        path="powershell.exe",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 30
    assert analyzed_entry.risk_level == "Medium"
    assert "Entry uses suspicious command interpreter" in analyzed_entry.reasons


def test_script_file_rule_adds_score_and_reason():
    """
    Test that script file extension increases risk score.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="ScriptEntry",
        command=r"C:\Scripts\start.ps1",
        path=r"C:\Scripts\start.ps1",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 25
    assert analyzed_entry.risk_level == "Medium"
    assert "Entry runs a script file from autorun location" in analyzed_entry.reasons


def test_powershell_options_rule_adds_score_and_reason():
    """
    Test that suspicious PowerShell options increase risk score.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="BypassEntry",
        command="powershell.exe -ExecutionPolicy Bypass",
        path="powershell.exe",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 70
    assert analyzed_entry.risk_level == "High"
    assert "Entry uses suspicious command interpreter" in analyzed_entry.reasons
    assert "Entry uses suspicious PowerShell options" in analyzed_entry.reasons


def test_entry_can_match_multiple_rules():
    """
    Test that one entry can match several risk rules.
    """
    engine = RiskEngine()

    entry = PersistenceEntry(
        name="BadEntry",
        command=r"powershell.exe -ExecutionPolicy Bypass C:\Users\mokht\AppData\bad.ps1",
        path=r"C:\Users\mokht\AppData\bad.ps1",
    )

    analyzed_entry = engine.analyze_entry(entry)

    assert analyzed_entry.risk_score == 125
    assert analyzed_entry.risk_level == "Critical"
    assert len(analyzed_entry.reasons) == 4


def test_analyze_returns_list_of_analyzed_entries():
    """
    Test that analyze() processes a list of entries.
    """
    engine = RiskEngine()

    entries = [
        PersistenceEntry(name="SafeEntry", command=r"C:\Program Files\App\app.exe", path=r"C:\Program Files\App\app.exe"),
        PersistenceEntry(name="BadEntry", command="cmd.exe /c test", path="cmd.exe"),
    ]

    analyzed_entries = engine.analyze(entries)

    assert len(analyzed_entries) == 2
    assert analyzed_entries[0].risk_level == "Low"
    assert analyzed_entries[1].risk_score == 30
    assert analyzed_entries[1].risk_level == "Medium"