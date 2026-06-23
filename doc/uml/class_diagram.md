# class diagram

```mermaid
classDiagram

    class BaseCollector {
        <<abstract>>
        #source_name: str
        #mitre_technique: str
        +collect() List~PersistenceEntry~
        +is_available() bool
    }

    class StartupCollector {
        -user_startup_path: str
        -system_startup_path: str
        +collect() List~PersistenceEntry~
        -scan_folder(path: str) List~PersistenceEntry~
    }

    class RegistryCollector {
        -registry_paths: List~str~
        +collect() List~PersistenceEntry~
        -read_run_key(path: str) List~PersistenceEntry~
        -get_key_last_modified_time(path: str) str
    }

    class TaskCollector {
        -powershell_command: str
        +collect() List~PersistenceEntry~
        -parse_task_output(output: str) List~PersistenceEntry~
    }

    class ServiceCollector {
        -powershell_command: str
        +collect() List~PersistenceEntry~
        -parse_service_output(output: str) List~PersistenceEntry~
    }

    class PersistenceEntry {
        +id: str
        +name: str
        +entry_type: str
        +source: str
        +command: str
        +path: str
        +timestamp: str
        +publisher: str
        +sha256: str
        +mitre_technique: str
        +risk_score: int
        +risk_level: str
        +reasons: List~str~
        +to_dict() dict
    }

    class ScanResult {
        +scan_time: str
        +total_entries: int
        +low_count: int
        +medium_count: int
        +high_count: int
        +critical_count: int
        +entries: List~PersistenceEntry~
        +status: str
        +to_dict() dict
    }

    class PersistenceEngine {
        -collectors: List~BaseCollector~
        -normalizer: Normalizer
        -risk_engine: RiskEngine
        -baseline_comparator: BaselineComparator
        -report_generator: ReportGenerator
        +scan() ScanResult
        +create_baseline() bool
        +compare_with_baseline() ScanResult
        +generate_report(result: ScanResult, format: str) str
    }

    class Normalizer {
        +normalize(entries: List~dict~) List~PersistenceEntry~
        -extract_path(command: str) str
        -generate_entry_id(entry: PersistenceEntry) str
    }

    class RiskEngine {
        -rules: List~RiskRule~
        +analyze(entries: List~PersistenceEntry~) List~PersistenceEntry~
        +calculate_score(entry: PersistenceEntry) int
        +classify_risk(score: int) str
    }

    class RiskRule {
        +name: str
        +description: str
        +score: int
        +check(entry: PersistenceEntry) bool
    }

    class BaselineComparator {
        -baseline_store: BaselineStore
        +compare(current: List~PersistenceEntry~) dict
        +detect_new_entries(current: List~PersistenceEntry~, baseline: List~PersistenceEntry~) List~PersistenceEntry~
        +detect_removed_entries(current: List~PersistenceEntry~, baseline: List~PersistenceEntry~) List~PersistenceEntry~
        +detect_modified_entries(current: List~PersistenceEntry~, baseline: List~PersistenceEntry~) List~PersistenceEntry~
    }

    class BaselineStore {
        -baseline_path: str
        +save(entries: List~PersistenceEntry~) bool
        +load() List~PersistenceEntry~
        +exists() bool
    }

    class ReportGenerator {
        -output_dir: str
        +export_json(result: ScanResult) str
        +export_csv(result: ScanResult) str
        +export_html(result: ScanResult) str
    }

    class PowerShellRunner {
        +run(command: str) str
    }

    class HashUtils {
        +calculate_sha256(path: str) str
    }

    BaseCollector <|-- StartupCollector
    BaseCollector <|-- RegistryCollector
    BaseCollector <|-- TaskCollector
    BaseCollector <|-- ServiceCollector

    PersistenceEngine --> BaseCollector
    PersistenceEngine --> Normalizer
    PersistenceEngine --> RiskEngine
    PersistenceEngine --> BaselineComparator
    PersistenceEngine --> ReportGenerator

    Normalizer --> PersistenceEntry
    RiskEngine --> RiskRule
    RiskEngine --> PersistenceEntry
    BaselineComparator --> BaselineStore
    BaselineComparator --> PersistenceEntry
    ReportGenerator --> ScanResult
    ScanResult --> PersistenceEntry

    TaskCollector --> PowerShellRunner
    ServiceCollector --> PowerShellRunner
    Normalizer --> HashUtils