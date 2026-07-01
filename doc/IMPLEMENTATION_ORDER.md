# Implementation Order

This document explains the recommended order to implement the Windows Autorun Inspector project, including when to do manual testing and unit testing.

## 1. Project Foundation

### Implement

- `app/collectors/base_collector.py`
- `app/utils/powershell_runner.py`
- `app/utils/time_utils.py`
- `app/utils/hash_utils.py`

### Goal

Create shared helper classes used by the rest of the project.

### Manual Testing

- Test `PowerShellRunner` with a simple PowerShell command.
- Example command: `Get-Date`

### Unit Testing

- Test that `PowerShellRunner.run()` returns output when command succeeds.
- Test that it returns an empty string when command fails.

---

## 2. Collectors

### Implement

- `app/collectors/registry_collector.py`
- `app/collectors/startup_collector.py`
- `app/collectors/tasks_collector.py`
- `app/collectors/services_collector.py`

### Goal

Collect raw autorun data from Windows persistence locations.

### Manual Testing

Test each collector separately:

- Registry Collector: verify it finds Registry Run and RunOnce entries.
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

## 3. Data Models

### Implement

- `app/models.py`

Classes:

- `PersistenceEntry`
- `ScanResult`

### Goal

Create standard objects for collected entries and scan results.

### Manual Testing

- Create one `PersistenceEntry` manually.
- Print `to_dict()` and verify the output.

### Unit Testing

Test:

- Object creation.
- Default values.
- `to_dict()` output.
- Risk fields such as `risk_score`, `risk_level`, and `reasons`.

---

## 4. Normalizer

### Implement

- `app/analysis/normalizer.py`

### Goal

Convert raw dictionaries from collectors into `PersistenceEntry` objects.

### Manual Testing

- Pass sample collector output to the normalizer.
- Verify that entries have the same final structure.

### Unit Testing

Test:

- Path extraction from command strings.
- Entry ID generation.
- Missing fields.
- Normalization of registry, startup folder, task, and service entries.

---

## 5. Risk Rules

### Implement

- `app/analysis/rules.py`
- `app/analysis/risk_engine.py`

### Goal

Detect suspicious autorun entries and calculate risk score.

### Manual Testing

Create fake suspicious entries, for example:

- Command from `Temp`
- Unknown executable path
- Suspicious script file
- Missing path
- PowerShell command

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

### Goal

Save and load trusted baseline entries from JSON.

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

- `app/analysis/baseline_compare.py`

### Goal

Compare current scan results with baseline.

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

## 8. Core Engine

### Implement

- `app/core/engine.py`

### Goal

Connect all project parts together.

Workflow:

1. Run collectors.
2. Normalize entries.
3. Analyze risk.
4. Compare with baseline.
5. Return `ScanResult`.

### Manual Testing

Run a complete scan from one script.

Verify:

- Entries are collected.
- Entries are normalized.
- Risk score is applied.
- Scan summary is correct.

### Unit Testing

Use fake collectors and fake entries.

Test:

- Engine calls collectors.
- Engine returns `ScanResult`.
- Engine handles empty collector output.
- Engine handles collector errors safely.

---

## 9. Reports

### Implement

- `app/reports/json_report.py`
- `app/reports/csv_report.py`
- `app/reports/html_report.py`

### Goal

Export scan results in different formats.

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

## 10. CLI

### Implement

- `app/cli/commands.py`
- `app/main.py`

### Goal

Allow the user to run the tool from terminal.

Example commands:

- `scan`
- `create-baseline`
- `compare`
- `export-report`

### Manual Testing

Run each CLI command manually.

Example:

```powershell
python -m app.main scan
python -m app.main create-baseline
python -m app.main compare