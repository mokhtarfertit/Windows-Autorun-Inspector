# Project Structure

This document describes the recommended project structure for Windows Autorun Inspector.

The structure follows the UML class diagram and keeps the implementation simple for the first version.

---

## Folder Structure

```text
Windows-Autorun-Inspector/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|
|   |-- collectors/
|   |   |-- __init__.py
|   |   |-- base_collector.py
|   |   |-- registry_collector.py
|   |   |-- startup_collector.py
|   |   |-- tasks_collector.py
|   |   |-- services_collector.py
|
|   |-- utils/
|   |   |-- __init__.py
|   |   |-- powershell_runner.py
|   |   |-- hash_utils.py
|   |   |-- time_utils.py
|
|   |-- analysis/
|   |   |-- __init__.py
|   |   |-- persistence_entry.py
|   |   |-- scan_result.py
|   |   |-- risk_rule.py
|   |   |-- normalizer.py
|   |   |-- risk_engine.py
|   |   |-- baseline_comparator.py
|
|   |-- storage/
|   |   |-- __init__.py
|   |   |-- baseline_store.py
|
|   |-- reports/
|   |   |-- __init__.py
|   |   |-- report_generator.py
|
|   |-- core/
|   |   |-- __init__.py
|   |   |-- persistence_engine.py
|
|-- tests/
|-- testing_manually/
|-- doc/
|-- reports/
|-- README.md
|-- requirements.txt
|-- pytest.ini
|-- .gitignore
|-- LICENSE