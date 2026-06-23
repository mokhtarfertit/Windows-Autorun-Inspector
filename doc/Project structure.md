
# Project Structure

```text
Windows autorun inspector/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── engine.py
│   │
│   ├── cli/
│   │   └── commands.py
│   │
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── results_table.py
│   │   └── details_panel.py
│   │
│   ├── collectors/
│   │   ├── startup_collector.py
│   │   ├── registry_collector.py
│   │   ├── tasks_collector.py
│   │   └── services_collector.py
│   │
│   ├── analysis/
│   │   ├── normalizer.py
│   │   ├── risk_engine.py
│   │   ├── baseline_compare.py
│   │   └── rules.py
│   │
│   ├── reports/
│   │   ├── json_report.py
│   │   ├── csv_report.py
│   │   └── html_report.py
│   │
│   ├── storage/
│   │   ├── baseline_store.py
│   │   └── history_store.py
│   │
│   └── utils/
│       ├── powershell_runner.py
│       ├── hash_utils.py
│       └── time_utils.py
│
├── tests/
├── docs/
├── reports/
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

```