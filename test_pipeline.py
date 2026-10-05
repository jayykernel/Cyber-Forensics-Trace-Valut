import os
import sys
import json
import unittest

from forensic_engine.integrity import build_integrity_ledger, calculate_sha256
from forensic_engine.extractors.fs_extractor import parse_mft_timeline
from forensic_engine.extractors.auth_extractor import parse_auth_logs
from forensic_engine.extractors.browser_extractor import parse_browser_artefacts
from forensic_engine.extractors.email_extractor import parse_eml_files
from forensic_engine.extractors.network_extractor import parse_network_logs
from forensic_engine.timeline import generate_unified_timeline
from forensic_engine.correlator import build_attack_chain
from forensic_engine.incident_analyzer import analyze_incident
from forensic_engine.report_generator import generate_markdown_report, generate_html_report

class TestTraceVaultForensicsPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_dir = r"C:\dev\Trace-Valut"
        cls.evidence_dir = os.path.join(cls.base_dir, "evidence")
        cls.reports_dir = os.path.join(cls.base_dir, "reports")
        os.makedirs(cls.reports_dir, exist_ok=True)

    def test_01_evidence_files_exist(self):
        """Verify that all multi-modal evidence directories and files exist."""
        required_paths = [
            os.path.join(self.evidence_dir, "filesystem", "victim_project", "drone_nav_core.py"),
            os.path.join(self.evidence_dir, "filesystem", "victim_project", "neural_weights_v4.bin"),
            os.path.join(self.evidence_dir, "filesystem", "victim_project", "dataset_lidar_final.parquet"),
            os.path.join(self.evidence_dir, "filesystem", "victim_project", "project_final_report.docx"),
            os.path.join(self.evidence_dir, "filesystem", "mft_timeline.csv"),
            os.path.join(self.evidence_dir, "filesystem", "deleted_staging", "project_backup_v2.zip.deleted.meta"),
            os.path.join(self.evidence_dir, "auth_logs", "Security_EventLogs.json"),
            os.path.join(self.evidence_dir, "auth_logs", "system_registry.json"),
            os.path.join(self.evidence_dir, "browser", "chrome_history.sqlite"),
            os.path.join(self.evidence_dir, "browser", "chrome_cache_metadata.json"),
            os.path.join(self.evidence_dir, "email", "exfil_notification.eml"),
            os.path.join(self.evidence_dir, "network", "netflow_connections.csv"),
            os.path.join(self.evidence_dir, "network", "pcap_dns_http_summary.json"),
        ]
        for p in required_paths:
            self.assertTrue(os.path.exists(p), f"Missing evidence file: {p}")

    def test_02_cryptographic_integrity_hashing(self):
        """Verify SHA-256 calculation and ledger generation without altering originals."""
        ledger_path = os.path.join(self.reports_dir, "integrity_ledger.json")
        ledger = build_integrity_ledger(self.evidence_dir, ledger_path)
        self.assertGreaterEqual(len(ledger), 10)
        self.assertTrue(os.path.exists(ledger_path))

        # Verify valid SHA-256 hex string lengths
        for fpath, data in ledger.items():
            self.assertEqual(len(data["sha256"]), 64)
            self.assertGreater(data["size_bytes"], 0)

    def _get_all_events(self):
        all_events = []
        fs_path = os.path.join(self.evidence_dir, "filesystem", "mft_timeline.csv")
        all_events.extend(parse_mft_timeline(fs_path))

        sec_logs_path = os.path.join(self.evidence_dir, "auth_logs", "Security_EventLogs.json")
        reg_path = os.path.join(self.evidence_dir, "auth_logs", "system_registry.json")
        all_events.extend(parse_auth_logs(sec_logs_path, reg_path))

        sqlite_path = os.path.join(self.evidence_dir, "browser", "chrome_history.sqlite")
        cache_path = os.path.join(self.evidence_dir, "browser", "chrome_cache_metadata.json")
        all_events.extend(parse_browser_artefacts(sqlite_path, cache_path))

        eml_dir = os.path.join(self.evidence_dir, "email")
        all_events.extend(parse_eml_files(eml_dir))

        netflow_path = os.path.join(self.evidence_dir, "network", "netflow_connections.csv")
        pcap_path = os.path.join(self.evidence_dir, "network", "pcap_dns_http_summary.json")
        all_events.extend(parse_network_logs(netflow_path, pcap_path))

        return all_events

    def test_03_multi_modal_extractors(self):
        """Verify all extraction parsers extract structured records with timestamps."""
        events = self._get_all_events()
        self.assertGreater(len(events), 0)

    def test_04_unified_timeline(self):
        """Verify chronological sorting and suspicious event tagging."""
        all_events = self._get_all_events()
        timeline = generate_unified_timeline(all_events)
        self.assertGreater(len(timeline), 15)

        # Check chronological order
        timestamps = [e.get("timestamp") for e in timeline if e.get("timestamp")]
        self.assertEqual(timestamps, sorted(timestamps))

        # Check suspicious events exist
        suspicious = [e for e in timeline if e.get("is_suspicious")]
        self.assertGreater(len(suspicious), 5)

    def test_05_attack_chain_correlation(self):
        """Verify 7-stage attack chain reconstruction."""
        all_events = self._get_all_events()
        timeline = generate_unified_timeline(all_events)
        chain = build_attack_chain(timeline)
        self.assertEqual(len(chain), 7)
        self.assertEqual(chain[0]["stage"], 1)
        self.assertEqual(chain[6]["stage"], 7)

    def test_06_incident_analysis_and_attribution(self):
        """Verify definitive answers to the 6 core case questions and suspect attribution."""
        ledger = build_integrity_ledger(self.evidence_dir)
        all_events = self._get_all_events()
        timeline = generate_unified_timeline(all_events)
        chain = build_attack_chain(timeline)

        analysis = analyze_incident(ledger, timeline, chain)

        # Verify 6 core answers exist
        answers = analysis["answers"]
        self.assertIn("1_what_files_accessed", answers)
        self.assertIn("2_when_did_activity_occur", answers)
        self.assertIn("3_how_accessed", answers)
        self.assertIn("4_how_exfiltrated", answers)
        self.assertIn("5_who_source", answers)
        self.assertIn("6_evidence_supporting_conclusion", answers)

        # Verify suspect
        self.assertEqual(analysis["suspect_info"]["name"], "David Vance")
        self.assertEqual(analysis["suspect_info"]["account"], "dvance")
        self.assertEqual(analysis["confidence_assessment"]["level"], "HIGH")

    def test_07_report_generation(self):
        """Verify Markdown and HTML report generation."""
        ledger = build_integrity_ledger(self.evidence_dir)
        all_events = self._get_all_events()
        timeline = generate_unified_timeline(all_events)
        chain = build_attack_chain(timeline)
        analysis = analyze_incident(ledger, timeline, chain)

        md_path = os.path.join(self.reports_dir, "FORENSIC_INVESTIGATION_REPORT.md")
        html_path = os.path.join(self.reports_dir, "Forensic_Report.html")

        md_content = generate_markdown_report(ledger, timeline, chain, analysis, md_path)
        html_content = generate_html_report(ledger, timeline, chain, analysis, html_path)

        self.assertTrue(os.path.exists(md_path))
        self.assertTrue(os.path.exists(html_path))
        self.assertIn("David Vance", md_content)
        self.assertIn("David Vance", html_content)
        self.assertIn("dropfile.to", md_content)
        self.assertIn("dropfile.to", html_content)

if __name__ == "__main__":
    unittest.main()
