import csv
import json

from app.analysis.persistence_entry import PersistenceEntry
from app.analysis.scan_result import ScanResult
from app.reports.report_generator import ReportGenerator


def create_sample_scan_result():
    """
    Create a sample ScanResult used by report tests.
    """
    entry = PersistenceEntry(
        id="abc123",
        name="TestApp",
        entry_type="Registry Run Key",
        source="Registry",
        command=r"C:\TestApp\app.exe",
        path=r"C:\TestApp\app.exe",
        risk_score=30,
        risk_level="Medium",
        reasons=["Test reason"],
    )

    result = ScanResult(
        scan_time="2026-07-07T10:00:00+00:00",
        entries=[entry],
        status="success",
    )

    result.calculate_counts()

    return result


def test_report_generator_creates_output_directory(tmp_path):
    """
    Test that ReportGenerator creates the output directory.
    """
    output_dir = tmp_path / "reports"

    generator = ReportGenerator(str(output_dir))

    assert output_dir.exists()
    assert output_dir.is_dir()


def test_export_json_creates_json_file(tmp_path):
    """
    Test that export_json() creates a JSON report file.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_json(result)

    assert report_path != ""
    assert (output_dir / "scan_result.json").exists()


def test_export_json_contains_scan_result_data(tmp_path):
    """
    Test that JSON report contains scan result data.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_json(result)

    with open(report_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["scan_time"] == "2026-07-07T10:00:00+00:00"
    assert data["total_entries"] == 1
    assert data["medium_count"] == 1
    assert data["entries"][0]["name"] == "TestApp"
    assert data["entries"][0]["risk_level"] == "Medium"


def test_export_csv_creates_csv_file(tmp_path):
    """
    Test that export_csv() creates a CSV report file.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_csv(result)

    assert report_path != ""
    assert (output_dir / "scan_result.csv").exists()


def test_export_csv_contains_entry_data(tmp_path):
    """
    Test that CSV report contains entry data.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_csv(result)

    with open(report_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["name"] == "TestApp"
    assert rows[0]["source"] == "Registry"
    assert rows[0]["risk_score"] == "30"
    assert rows[0]["risk_level"] == "Medium"
    assert rows[0]["reasons"] == "Test reason"


def test_export_html_creates_html_file(tmp_path):
    """
    Test that export_html() creates an HTML report file.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_html(result)

    assert report_path != ""
    assert (output_dir / "scan_result.html").exists()


def test_export_html_contains_entry_data(tmp_path):
    """
    Test that HTML report contains entry data.
    """
    output_dir = tmp_path / "reports"
    generator = ReportGenerator(str(output_dir))
    result = create_sample_scan_result()

    report_path = generator.export_html(result)

    with open(report_path, "r", encoding="utf-8") as file:
        html = file.read()

    assert "Windows Autorun Inspector Report" in html
    assert "TestApp" in html
    assert "Registry" in html
    assert "Medium" in html
    assert "Test reason" in html