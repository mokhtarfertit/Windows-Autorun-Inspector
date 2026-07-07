import csv
import json 
from html import escape
from pathlib import Path

from app.analysis.scan_result import ScanResult

class ReportGenerator:
    """Generate reports from scan results."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_json(self, result: ScanResult, filename: str ="scan_result.json") -> str:
        """Export scan result to JSON file."""
        report_path = self.output_dir /filename

        try:
            with report_path.open("w", encoding="utf-8") as file:
                json.dump(result.to_dict(), file, indent=4)

            return str(report_path)
        except OSError:
            return ""
        
    def export_csv(sefl, result: ScanResult, filename: str = "scan_result.csv") -> str:
        """Export scan result entries to CSV file."""

        report_path = self.output_dir /filename

        fieldnames = [
            "id",
            "name",
            "entry_type",
            "source",
            "command",
            "path",
            "timestamp",
            "publisher",
            "sha256",
            "mitre_technique",
            "risk_score",
            "risk_level",
            "reasons",
        ]

        try:
            with report_path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames = fieldnames)
                writer.writeheader()

                for entry in result.entries:
                    row = entry.to_dict()
                    row["reasons"] = "; ".join(entry.reasons)
                    writer.writerow(row)

                return str(report_path)
        except OSError:
            return ""
        
    def export_html(self, result: ScanResult, filename: str = "scan_result.html") -> str:
        """Export scan result to a simple HTML report."""
        report_path = self.output_dir / filename

        try:
            html_content = self.build_html(result)

            with report_path.open("w", encoding="utf-8") as file:
                file.write(html_content)

            return str(report_path)

        except OSError:
            return ""

    def build_html(self, result: ScanResult) -> str:
        """Build HTML content for scan result."""
        rows = ""

        for entry in result.entries:
            reasons = "; ".join(entry.reasons)

            rows += f"""
            <tr>
                <td>{escape(entry.name)}</td>
                <td>{escape(entry.source)}</td>
                <td>{escape(entry.path)}</td>
                <td>{entry.risk_score}</td>
                <td>{escape(entry.risk_level)}</td>
                <td>{escape(reasons)}</td>
            </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Windows Autorun Inspector Report</title>
        </head>
        <body>
            <h1>Windows Autorun Inspector Report</h1>

            <p>Total entries: {result.total_entries}</p>
            <p>Low: {result.low_count}</p>
            <p>Medium: {result.medium_count}</p>
            <p>High: {result.high_count}</p>
            <p>Critical: {result.critical_count}</p>
            <p>Status: {escape(result.status)}</p>

            <table border="1">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Source</th>
                        <th>Path</th>
                        <th>Risk Score</th>
                        <th>Risk Level</th>
                        <th>Reasons</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """