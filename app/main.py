import sys

from app.core.persistence_engine import PersistenceEngine

def print_usage():
    """Print available CLI commands."""
    print("Windows Autorun Inspector")
    print("")
    print("Usage:")
    print("  python -m app.main scan")
    print("  python -m app.main create-baseline")
    print("  python -m app.main compare")
    print("  python -m app.main report-json")
    print("  python -m app.main report-csv")
    print("  python -m app.main report-html")

def print_scan_summary(result):
    """Print scan result summary."""
    print(f"Scan time: {result.scan_time}")
    print(f"Total entries: {result.total_entries}")
    print(f"Low: {result.low_count}")
    print(f"Medium: {result.medium_count}")
    print(f"High: {result.high_count}")
    print(f"Critical: {result.critical_count}")

def main():
    """Run command line interface."""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]
    engine = PersistenceEngine()

    if command == "scan":
        result = engine.scan()
        print_scan_summary(result)
        return

    if command == "create-baseline":
        saved = engine.create_baseline()

        if saved:
            print("Baseline created successfully")
        else:
            print("Failed to create baseline")

        return

    if command == "compare":
        comparison = engine.compare_with_baseline()

        print(f"New entries: {len(comparison['new_entries'])}")
        print(f"Removed entries: {len(comparison['removed_entries'])}")
        print(f"Modified entries: {len(comparison['modified_entries'])}")
        return

    if command == "report-json":
        result = engine.scan()
        report_path = engine.generate_report(result, "json")
        print(f"JSON report: {report_path}")
        return

    if command == "report-csv":
        result = engine.scan()
        report_path = engine.generate_report(result, "csv")
        print(f"CSV report: {report_path}")
        return

    if command == "report-html":
        result = engine.scan()
        report_path = engine.generate_report(result, "html")
        print(f"HTML report: {report_path}")
        return

    print_usage()

if __name__ == "__main__":
    main()