import argparse

from app.core.persistence_engine import PersistenceEngine

def print_scan_summary(result):
    """Print scan result summary."""
    print(f"Scan time: {result.scan_time}")
    print(f"Total entries: {result.total_entries}")
    print(f"Low: {result.low_count}")
    print(f"Medium: {result.medium_count}")
    print(f"High: {result.high_count}")
    print(f"Critical: {result.critical_count}")

def build_parser():
    """build command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="cyberpersist",
        description="Windows persistence anaylsis tool",

    )


    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("scan", help="Run full persistence")
    subparsers.add_parser("create-baseline", help="Create baseline from current scan")
    subparsers.add_parser("compare", help="Compare current scan with saved baseline")
    subparsers.add_parser("report-json", help="Generate JSON scan report")
    subparsers.add_parser("report-csv", help="Generate CSV scan report")
    subparsers.add_parser("report-html", help="Generate HTML scan report")

    return parser


def main():
    """Run command line interface."""
    parser = build_parser()
    args = parser.parse_args()

    command = args.command
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