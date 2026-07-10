# Windows Autorun Inspector

Windows Autorun Inspector is a defensive cybersecurity tool for analyzing Windows persistence mechanisms. It helps identify autorun entries that may be abused by malware to maintain access after reboot, login, or service restart.

The tool scans common Windows persistence locations, normalizes the results, applies risk rules, compares findings against a baseline, and generates reports for investigation.

## Why This Tool Matters

Persistence is one of the most common techniques used by malware and threat actors. Windows provides many legitimate auto-start mechanisms, but those same mechanisms can be abused for malicious persistence.

Manual inspection is slow and error-prone, especially when a system contains many legitimate startup programs, scheduled tasks, and services.

Windows Autorun Inspector helps analysts quickly answer

- What programs start automatically
- Which autorun entries are new
- Which entries changed since the last trusted baseline
- Which entries look suspicious
- What persistence technique may be involved

## Detection Coverage

The tool currently inspects

 Area  Description  MITRE ATT&CK 
---------
 Registry Run Keys  Checks common Run and RunOnce autorun keys  T1547.001 
 Startup Folders  Checks user and system Startup folders  T1547.001 
 Scheduled Tasks  Checks Windows scheduled task persistence  T1053.005 
 Windows Services  Checks services configured to run automatically  T1543.003 

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
- Provides a CLI command `cyberpersist`
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
The main workflow
Collect autorun entries from Registry, Startup folders, Scheduled Tasks, and Services.
Normalize all entries into a common PersistenceEntry structure.
Extract file paths and calculate hashes when possible.
Apply risk rules to detect suspicious indicators.
Save or compare against a trusted baseline.
Generate investigation reports.
Usage
After installation, run
cyberpersist --help
Run a full scan
cyberpersist scan
Create a baseline
cyberpersist create-baseline
Compare current system state with the baseline
cyberpersist compare
Generate reports
cyberpersist report-json
cyberpersist report-csv
cyberpersist report-html
Example Investigation Workflow
Create a clean baseline on a trusted system state
cyberpersist create-baseline
Later, run a new scan and compare
cyberpersist compare
Generate an HTML report
cyberpersist report-html
Review entries with high risk scores, suspicious paths, script execution, or changed hashes.
Risk Analysis
The risk engine checks for suspicious indicators such as
Missing executable path
Execution from user-writable directories such as Temp or AppData
Suspicious command interpreters
Script-based autorun entries
Suspicious PowerShell options
Each matching rule increases the entry risk score.
Risk levels
Score	Level
0-19	Low
20-49	Medium
50-79	High
80+	Critical

Reports
The tool can generate
JSON report for structured analysis
CSV report for spreadsheet review
HTML report for readable investigation output
Example
cyberpersist report-html
Installation For Users
Download the Windows installer from the project release page
CyberPersist-Setup.exe
Install it, then run the tool from Command Prompt or PowerShell
cyberpersist scan
Some checks may require Administrator privileges for complete visibility.
Installation For Developers
Clone the repository
git clone httpsgithub.commokhtarfertitWindows-Autorun-Inspector.git
cd Windows-Autorun-Inspector
Install in editable mode
pip install -e .
Install development dependencies
pip install -e .[dev]
Run directly without installing
python -m app.main scan
Project Structure
WAI
├── app
│   ├── main.py
│   ├── analysis
│   │   ├── baseline_comparator.py
│   │   ├── normalizer.py
│   │   ├── persistence_entry.py
│   │   ├── risk_engine.py
│   │   ├── risk_rule.py
│   │   └── scan_result.py
│   ├── collectors
│   │   ├── base_collector.py
│   │   ├── registry_collector.py
│   │   ├── services_collector.py
│   │   ├── startup_collector.py
│   │   └── tasks_collector.py
│   ├── core
│   │   └── persistence_engine.py
│   ├── reports
│   │   └── report_generator.py
│   ├── storage
│   │   └── baseline_store.py
│   └── utils
│       ├── hash_utils.py
│       ├── powershell_runner.py
│       └── time_utils.py
├── tests
├── testing_manually
├── doc
├── installer
│   └── cyberpersist.iss
├── main.py
├── pyproject.toml
├── requirements.txt
├── build_exe.bat
├── build_installer.bat
├── pytest.ini
└── README.md
Testing
Run all tests
python -m pytest tests
Run one test file
python -m pytest teststest_risk_engine.py
Manual testing scripts are available in
testing_manually
Build From Source
Build the Windows executable
build_exe.bat
Output
distcyberpersistcyberpersist.exe
Build the Windows installer
build_installer.bat
Output
dist-installerCyberPersist-Setup.exe
Generated build files should not be committed to the repository. Release binaries should be uploaded to GitHub Releases.
Repository Hygiene
Do not commit generated files such as
__pycache__
build
dist
dist-installer
.egg-info
.pyc
baseline.json
Disclaimer
This project is intended for defensive security, education, and incident response support only. It does not remove persistence entries or modify the system. It only collects, analyzes, compares, and reports autorun data.
```