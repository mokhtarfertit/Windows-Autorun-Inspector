# Windows Autorun Inspector

Windows Autorun Inspector is a defensive cybersecurity tool for analyzing common Windows persistence locations. It helps students, analysts, and incident responders inspect autorun entries, calculate risk, compare the current system state with a saved baseline, and generate reports.

The packaged CLI command is:

```powershell
cyberpersist
```

## Purpose

Windows includes many legitimate auto-start mechanisms, such as Registry Run keys, Startup folders, Scheduled Tasks, and Windows Services. Malware can abuse these same locations to maintain persistence after reboot or user login.

This tool scans those locations, normalizes the collected data, applies risk rules, and produces reports that make suspicious persistence entries easier to review.

## Features

- Registry Run and RunOnce key collection
- Startup folder collection
- Scheduled Tasks collection
- Windows Services collection
- Normalized persistence entry model
- SHA-256 hash calculation for executable paths
- Timestamp support
- Risk scoring and risk levels
- Baseline creation
- Baseline comparison
- Detection of new, removed, and modified entries
- JSON, CSV, and HTML report generation
- CLI support through `cyberpersist`
- Windows executable build support with PyInstaller
- Installer preparation support with Inno Setup

## Project Structure

```text
WAI/
├── app/
│   ├── main.py
│   ├── analysis/
│   │   ├── baseline_comparator.py
│   │   ├── normalizer.py
│   │   ├── persistence_entry.py
│   │   ├── risk_engine.py
│   │   ├── risk_rule.py
│   │   └── scan_result.py
│   ├── collectors/
│   │   ├── base_collector.py
│   │   ├── registry_collector.py
│   │   ├── services_collector.py
│   │   ├── startup_collector.py
│   │   └── tasks_collector.py
│   ├── core/
│   │   └── persistence_engine.py
│   ├── reports/
│   │   └── report_generator.py
│   ├── storage/
│   │   └── baseline_store.py
│   └── utils/
│       ├── hash_utils.py
│       ├── powershell_runner.py
│       └── time_utils.py
├── tests/
├── testing_manually/
├── doc/
├── main.py
├── pyproject.toml
├── requirements.txt
├── build_exe.bat
├── pytest.ini
└── README.md
```

## How It Works

```text
CLI command
    ↓
app/main.py
    ↓
PersistenceEngine
    ↓
Collectors
    ↓
Normalizer
    ↓
RiskEngine
    ↓
BaselineComparator / ReportGenerator
```

The main engine coordinates the full workflow:

1. Run collectors.
2. Normalize raw collector dictionaries into `PersistenceEntry` objects.
3. Analyze entries with risk rules.
4. Build a `ScanResult`.
5. Save baselines or generate reports when requested.

## CLI Commands

Run from the project root:

```powershell
python -m app.main --help
```

After installing the package locally:

```powershell
cyberpersist --help
```

Available commands:

```powershell
cyberpersist scan
cyberpersist create-baseline
cyberpersist compare
cyberpersist report-json
cyberpersist report-csv
cyberpersist report-html
```

## Developer Installation

Use Python 3.10 or newer.

```powershell
cd "C:\Users\mokht\OneDrive\Desktop\Windows Autorun Inspector\WAI"
pip install -e .
```

For development and testing:

```powershell
pip install -e ".[dev]"
```

Then test the CLI:

```powershell
cyberpersist --help
cyberpersist scan
```

## Run Without Installing

You can also run the project directly:

```powershell
python -m app.main scan
python -m app.main create-baseline
python -m app.main compare
python -m app.main report-json
python -m app.main report-csv
python -m app.main report-html
```

## Baseline Usage

Create a trusted baseline:

```powershell
cyberpersist create-baseline
```

Compare the current system with the saved baseline:

```powershell
cyberpersist compare
```

The baseline is stored as JSON and is used to detect:

- New entries
- Removed entries
- Modified entries

## Reports

Generate reports with:

```powershell
cyberpersist report-json
cyberpersist report-csv
cyberpersist report-html
```

Report files
```