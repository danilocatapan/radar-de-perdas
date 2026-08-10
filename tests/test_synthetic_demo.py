from __future__ import annotations

import copy
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.run_synthetic_demo import (
    NOTICE,
    ROOT,
    build_html,
    build_result,
    load_scenario,
    summarize,
    validate_scenario,
    write_outputs,
)


class SyntheticDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = load_scenario()

    def test_scenario_has_the_five_reviewed_cases(self) -> None:
        summary = validate_scenario(self.scenario)

        self.assertEqual(summary["chatsReceived"], 5)
        self.assertEqual(summary["chatsAccepted"], 4)
        self.assertEqual(summary["chatsExcluded"], 1)
        self.assertEqual(summary["eligibleRequests"], 4)
        self.assertEqual(summary["lp001"], 1)
        self.assertEqual(summary["lp002"], 1)
        self.assertEqual(summary["unverifiableResponses"], 1)

    def test_boundary_media_and_support_do_not_become_findings(self) -> None:
        validate_scenario(self.scenario)
        result = build_result(self.scenario, summarize(self.scenario["chats"]))

        finding_types = {finding["type"] for finding in result["findings"]}
        self.assertEqual(finding_types, {"LP-001", "LP-002"})
        classifications = {
            item["classification"] for item in result["reviewedCases"]
        }
        self.assertIn("NO_FINDING_SLA_BOUNDARY", classifications)
        self.assertIn("UNVERIFIABLE_RESPONSE", classifications)
        self.assertIn("OUT_OF_SCOPE", classifications)

    def test_inconsistent_summary_is_rejected(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["expectedSummary"]["lp002"] = 2

        with self.assertRaisesRegex(ValueError, "resumo esperado inconsistente"):
            validate_scenario(scenario)

    def test_fixture_outside_demo_directory_is_rejected(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["fixture"] = "development/android-multiline-lf.txt"

        with self.assertRaisesRegex(ValueError, "fora do diretório sintético"):
            validate_scenario(scenario)

    def test_html_escapes_scenario_content_and_has_offline_policy(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["title"] = "<script>alert('x')</script>"
        summary = validate_scenario(scenario)
        page = build_html(scenario, build_result(scenario, summary))

        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("default-src 'none'", page)
        self.assertIn(NOTICE, page)
        self.assertNotIn("http://", page)
        self.assertNotIn("https://", page)

    def test_write_outputs_generates_html_json_and_two_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outputs = write_outputs(Path(temporary), self.scenario)

            self.assertEqual(set(outputs), {"HTML", "JSON", "CSV"})
            self.assertTrue(all(path.is_file() for path in outputs.values()))
            result = json.loads(outputs["JSON"].read_text(encoding="utf-8"))
            self.assertEqual(result["schemaVersion"], "radar.demo/v1")
            self.assertEqual(result["analysisMode"], "SYNTHETIC_PRE_REVIEWED")
            self.assertEqual(len(result["findings"]), 2)
            with outputs["CSV"].open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([row["type"] for row in rows], ["LP-001", "LP-002"])

    def test_cli_accepts_only_output_directory_and_returns_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_synthetic_demo.py"),
                    "--output-dir",
                    temporary,
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            rejected = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_synthetic_demo.py"),
                    "--input",
                    "conversation.txt",
                    "--output-dir",
                    temporary,
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("STATUS=PASS", completed.stdout)
        self.assertIn("MODE=SYNTHETIC_PRE_REVIEWED", completed.stdout)
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("unrecognized arguments: --input", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
