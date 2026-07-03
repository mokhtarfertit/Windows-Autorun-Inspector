# Implementation Order

This document explains the recommended order to implement the Windows Autorun Inspector project.

The order follows the UML class diagram. The goal is to build the project from the lowest-level helpers first, then collectors, then analysis, baseline comparison, reporting, and finally the main engine.

---

## 1. Project Foundation

### Implement

- `app/collectors/base_collector.py`
- `app/utils/powershell_runner.py`
- `app/utils/time_utils.py`
- `app/utils/hash_utils.py`

### UML Classes

- `BaseCollector`
- `PowerShellRunner`
- `HashUtils`

### Goal

Create shared base classes and helper utilities used by the rest of the project.

### Manual Testing

- Test `PowerShellRunner` with a simple PowerShell command.
- Test `time_utils.py` by converting timestamps.
- Test `hash_utils.py` with a real file path.

### Unit Testing

- Test `PowerShellRunner.run()` with mocked `subprocess.run`.
- Test timestamp conversion functions.
- Test SHA-256 hash calculation.
- Test behavior when file path does not exist.

---

## 2. Collectors

### Implement

- `app/collectors/registry_collector.py`
- `app/collectors/startup_collector.py`
- `app/collectors/tasks_collector.py`
- `app/collectors/services_collector.py`

### UML Classes

- `RegistryCollector`
- `StartupCollector`
- `TaskCollector`
- `ServiceCollector`

### Goal

Collect raw autorun data from Windows persistence locations.

### Manual Testing

Test each collector separately:

- Registry Collector: verify it finds Registry `Run` and `RunOnce` entries.
- Startup Collector: verify it scans user and system Startup folders.
- Task Collector: verify it returns Scheduled Tasks.
- Service Collector: verify it returns Windows Services.

Manual testing is important here because collectors interact with the real Windows system.

### Unit Testing

Use mocked data instead of real Windows data.

Recommended tests:

- Registry Collector: mock `winreg`.
- Startup Collector: use temporary folders and test files.
- Task Collector: mock `PowerShellRunner`.
- Service Collector: mock `PowerShellRunner`.

---

## 3. Shared Data Classes

### Implement

Recommended structure:

- `app/entities/persistence_entry.py`
- `app/entities/scan_result.py`
- `app/rules/risk_rule.py`

Alternative simple structure:

- `app/entities.py`

### UML Classes

- `PersistenceEntry`
- `ScanResult`
- `RiskRule`

### Goal

Create standard objects used across the project.

`PersistenceEntry` represents one autorun item.

`ScanResult` represents the full result of one scan.

`RiskRule` represents one detection rule used by the risk engine.

### Manual Testing

- Create one `PersistenceEntry` manually.
- Print `to_dict()` and verify the output.
- Create one `ScanResult` manually.
- Verify scan counters such as total, low, medium, high, and critical.

### Unit Testing

Test:

- Object creation.
- Default values.
- `to_dict()` output.
- Risk fields:
  - `risk_score`
  - `risk_level`
  - `reasons`

---

## 4. Normalizer

### Implement

- `app/analysis/normalizer.py`

### UML Class

- `Normalizer`

### Goal

Convert raw dictionaries from collectors into clean `PersistenceEntry` objects.

Collectors may return different fields. The normalizer gives all entries one standard structure.

### Manual Testing

- Pass sample collector output to the normalizer.
- Verify that entries have the same final structure.
- Verify that command paths are extracted correctly.

### Unit Testing

Test:

- Path extraction from command strings.
- Entry ID generation.
- Missing fields.
- Normalization of:
  - Registry entries
  - Startup folder entries
  - Scheduled task entries
  - Service entries

---

## 5. Risk Analysis

### Implement

- `app/analysis/risk_engine.py`
- `app/rules/risk_rule.py`

### UML Classes

- `RiskEngine`
- `RiskRule`

### Goal

Detect suspicious autorun entries and calculate risk score.

### Manual Testing

Create fake suspicious entries, for example:

- Command from `Temp`
- Unknown executable path
- Suspicious script file
- Missing path
- PowerShell command
- Obfuscated command

Verify that the risk score increases.

### Unit Testing

Test:

- Each risk rule separately.
- Risk score calculation.
- Risk level classification:
  - Low
  - Medium
  - High
  - Critical

---

## 6. Baseline Storage

### Implement

- `app/storage/baseline_store.py`

### UML Class

- `BaselineStore`

### Goal

Save and load trusted baseline entries from JSON.

The baseline is the known-good autorun state of the system.

### Manual Testing

- Save a baseline file.
- Open the JSON file and verify the content.
- Load the baseline again.

### Unit Testing

Test:

- Save baseline.
- Load baseline.
- Check if baseline exists.
- Behavior when baseline file does not exist.
- Invalid JSON handling.

---

## 7. Baseline Comparison

### Implement

- `app/analysis/baseline_comparator.py`

### UML Class

- `BaselineComparator`

### Goal

Compare current scan results with the saved baseline.

Detect:

- New entries
- Removed entries
- Modified entries

### Manual Testing

Create a small baseline and current list manually.

Verify:

- New entry is detected.
- Removed entry is detected.
- Modified command/path is detected.

### Unit Testing

Test:

- `detect_new_entries()`
- `detect_removed_entries()`
- `detect_modified_entries()`
- Full `compare()` result.

---

## 8. Report Generation

### Implement

- `app/reports/report_generator.py`

### UML Class

- `ReportGenerator`

### Goal

Export scan results in different formats.

Supported formats:

- JSON
- CSV
- HTML

### Manual Testing

Generate reports and open them:

- JSON report
- CSV report
- HTML report

Verify that the data is readable and correct.

### Unit Testing

Test:

- Report file creation.
- Correct fields in JSON.
- Correct rows in CSV.
- HTML contains entry names and risk levels.

---

## 9. Core Engine

### Implement

- `app/core/persistence_engine.py`

### UML Class

- `PersistenceEngine`

### Goal

Connect all project parts together.

Workflow:

1. Run collectors.
2. Normalize entries.
3. Analyze risk.
4. Compare with baseline.
5. Generate report.
6. Return `ScanResult`.

### Manual Testing

Run a complete scan from one script.

Verify:

- Entries are collected.
- Entries are normalized.
- Risk score is applied.
- Baseline comparison works.
- Scan summary is correct.

### Unit Testing

Use fake collectors and fake entries.

Test:

- Engine calls collectors.
- Engine returns `ScanResult`.
- Engine handles empty collector output.
- Engine handles collector errors safely.

---

## 10. CLI Entry Point

### Implement

- `app/main.py`

Optional later:

- `app/cli/commands.py`

### Goal

Allow the user to run the tool from terminal.

Example commands:

```powershell
python -m app.main scan
python -m app.main create-baseline
python -m app.main compare
python -m app.main export-report