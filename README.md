# Windows Autorun Inspector

Windows Autorun Inspector is a defensive cybersecurity tool for analyzing Windows persistence mechanisms. It helps identify autorun entries that may be abused by malware to maintain access after reboot, login, or service restart.

The tool scans common Windows persistence locations, normalizes the results, applies risk rules, compares findings against a baseline, and generates reports for investigation.

## Why This Tool Matters

Persistence is one of the most common techniques used by malware and threat actors. Windows provides many legitimate auto-start mechanisms, but those same mechanisms can be abused for malicious persistence.

Manual inspection is slow and error-prone, especially when a system contains many legitimate startup programs, scheduled tasks, and services.

Windows Autorun Inspector helps analysts quickly answer:

- What programs start automatically?
- Which autorun entries are new?
- Which entries changed since the last trusted baseline?
- Which entries look suspicious?
- What persistence technique may be involved?

## Detection Coverage

The tool currently inspects:

| Area | Description | MITRE ATT&CK |
|---|---|---|
| Registry Run Keys | Checks common Run and RunOnce autorun keys | T1547.001 |
| Startup Folders | Checks user and system Startup folders | T1547.001 |
| Scheduled Tasks | Checks Windows scheduled task persistence | T1053.005 |
| Windows Services | Checks services configured to run automatically | T1543.003 |

## Key Features

- Collects Windows autorun entries from multiple persistence locations
- Normalizes different sources into one shared persistence entry format
- Calculates SHA-256 hashes for executable paths
- Extracts executable paths from command strings
- Applies suspicious-pattern risk rules
- Assigns risk score and risk level to each entry
- Creates a trusted baseline
- Compares current scan results with saved baseline
- Detects new, removed, and modified persistence entries
- Generates JSON, CSV, and HTML reports
- Provides a CLI command: `cyberpersist`
- Supports Windows executable and installer packaging

## How It Works

```text
Collectors
    ↓
Normalizer
    ↓
Risk Engine
    ↓
Baseline Comparator
    ↓
Report Generator
```

The main workflow:

1. Collect autorun entries from Registry, Startup folders, Scheduled Tasks, and Services.
2. Normalize all entries into a common `PersistenceEntry` structure.
3. Extract file paths and calculate hashes when possible.
4. Apply risk rules to detect suspicious indicators.
5. Save or compare against a trusted baseline.
6. Generate investigation reports.

## Usage

After installation, run:

```powershell
cyberpersist --help
```

Run a full scan:

```powershell
cyberpersist scan
```

Create a baseline:

```powershell
cyberpersist create-baseline
```

Compare current system state with the baseline:

```powershell
cyberpersist compare
```

Generate reports:

```powershell
cyberpersist report-json
cyberpersist report-csv
cyberpersist report-html
```

## Example Investigation Workflow

1. Create a clean baseline on a trusted system state:

```powershell
cyberpersist create-baseline
```

2. Later, run a new scan and compare:

```powershell
cyberpersist compare
```

3. Generate an HTML report:

```powershell
cyberpersist report-html
```

4. Review entries with high risk scores, suspicious paths, script execution, or changed hashes.

## Risk Analysis

The risk engine checks for suspicious indicators such as:

- Missing executable path
- Execution from user-writable directories such as Temp or AppData
- Suspicious command interpreters
- Script-based autorun entries
- Suspicious PowerShell options

Each matching rule increases the entry risk score.

Risk levels:

| Score | Level |
|---|---|
| 0-19 | Low |
| 20-49 | Medium |
| 50-79 | High |
| 80+ | Critical |

## Reports

The tool can generate:

- JSON report for structured analysis
- CSV report for spreadsheet review
- HTML report for readable investigation output

Example:

```powershell
cyberpersist report-html
```

## Installation For Users

Download the Windows installer from the project release page:

```text
CyberPersist-Setup.exe
```

Install it, then run the tool from Command Prompt or PowerShell:

```powershell
cyberpersist scan
```

Some checks may require Administrator privileges for complete visibility.

## Installation For Developers

Clone the repository:

```powershell
git clone https://github.com/mokhtarfertit/Windows-Autorun-Inspector.git
cd Windows-Autorun-Inspector
```

Install in editable mode:

```powershell
pip install -e .
```

Install development dependencies:

```powershell
pip install -e ".[dev]"
```

Run directly without installing:

```powershell
python -m app.main scan
```

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
├── doc/
├── installer/
│   └── cyberpersist.iss
├── main.py
├── pyproject.toml
├── requirements.txt
├── build_exe.bat
├── build_installer.bat
├── pytest.ini
└── README.md
```

## Testing

Run all tests:

```powershell
python -m pytest tests
```

Run one test file:

```powershell
python -m pytest tests\test_risk_engine.py
```

Manual testing scripts are available in:

```text
testing_manually/
```

## Build From Source

Build the Windows executable:

```powershell
build_exe.bat
```

Output:

```text
dist\cyberpersist\cyberpersist.exe
```

Build the Windows installer:

```powershell
build_installer.bat
```

Output:

```text
dist-installer\CyberPersist-Setup.exe
```

Generated build files should not be committed to the repository. Release binaries should be uploaded to GitHub Releases.

## Repository Hygiene

Do not commit generated files such as:

```text
__pycache__/
build/
dist/
dist-installer/
*.egg-info/
*.pyc
baseline.json
```

## Disclaimer

This project is intended for defensive security, education, and incident response support only. It does not remove persistence entries or modify the system. It only collects, analyzes, compares, and reports autorun data.