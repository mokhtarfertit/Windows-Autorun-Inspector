from app.analysis.baseline_comparator import BaseLineComparator
from app.analysis.normalizer import Normalizer
from app.analysis.risk_engine import RiskEngine
from app.analysis.scan_result import ScanResult
from app.collectors.registry_collector import RegistryCollector
from app.collectors.services_collector import ServiceCollector
from app.collectors.startup_collector import StartupCollector
from app.collectors.tasks_collector import TaskCollector
from app.reports.report_generator import ReportGenerator
from app.storage.baseline_store import BaselineStore
from app.utils.time_utils import now_iso

class PersistenceEngine:
    """Coordinate collectors, analysis, baseline comparison, and reports."""

    def __init__(self):
        self.collectors = [
            RegistryCollector(),
            StartupCollector(),
            TaskCollector(),
            ServiceCollector(),
        ]

        self.normalizer = Normalizer()
        self.risk_engine = RiskEngine()
        self.baseline_store = BaselineStore()
        self.baseline_comparator = BaseLineComparator()
        self.report_generator = ReportGenerator()

    def scan(self) -> ScanResult:
        """Run collectors , normalize entries, anaylze risk , and return scan result ."""
        raw_entries = []

        for collector in self.collectors:
            if collector.is_available():
                try :
                    raw_entries.extend(collector.collect())
                except Exception:
                    continue

        normalized_entries = self.normalizer.normalize(raw_entries)
        analyzed_entries = self.risk_engine.analyze(normalized_entries)

        result = ScanResult(
            scan_time=now_iso(),
            entries=analyzed_entries,
            status="success",
        )

        result.calculate_counts()

        return result
    
    def create_baseline(self) -> bool:
        """Run a scan and save it as baseline."""
        result = self.scan()

        return self.baseline_store.save(result.entries)
    
    def compare_with_baseline(self) -> dict:
        """Run a scan and compare it with saved baseline."""

        current_result = self.scan()
        baseline_entries = self.baseline_store.load()

        return self.baseline_comparator.compare(
            current_result.entries,
            baseline_entries,
        )
    
    def generate_report(self, result: ScanResult, report_format: str ="json") -> str:
        """Generate a report from scan result."""
        if report_format == "json":
            return self.report_generator.export_json(result)

        if report_format == "csv":
            return self.report_generator.export_csv(result)

        if report_format == "html":
            return self.report_generator.export_html(result)

        return ""