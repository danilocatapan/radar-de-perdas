from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_quality_page import build_html
from scripts.validate_repository import (
    EXPECTED_CSV_HEADERS,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self._create_valid_repository()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _create_valid_repository(self) -> None:
        fixture = "03/08/2026 09:00 - Prospect-001: Olá.\nContinuação.\n"
        self._write(
            "packages/test-fixtures/development/sample-lf.txt",
            fixture,
        )
        manifest = {
            "fixture": "development/sample-lf.txt",
            "set": "development",
            "compatibility": "compatible",
            "variant": "sample",
            "totalPhysicalLines": 2,
            "lineLedger": [
                {"line": 1, "classification": "MESSAGE_HEADER"},
                {"line": 2, "classification": "MESSAGE_CONTINUATION"},
            ],
            "messages": [],
            "expectedErrors": [],
        }
        self._write(
            "packages/test-fixtures/expected/sample-lf.expected.json",
            json.dumps(manifest, ensure_ascii=False),
        )
        coverage_header = EXPECTED_CSV_HEADERS[
            "packages/test-fixtures/coverage-matrix.csv"
        ]
        self._write(
            "packages/test-fixtures/coverage-matrix.csv",
            ",".join(coverage_header)
            + "\nCOV-001,LF,true,development/sample-lf.txt,"
            "COVERED_SYNTHETIC,PENDING,\n",
        )
        time_header = EXPECTED_CSV_HEADERS["docs/PILOT-TIME-LOG.csv"]
        self._write("docs/PILOT-TIME-LOG.csv", ",".join(time_header) + "\n")
        discovery_header = EXPECTED_CSV_HEADERS["docs/R1A-DISCOVERY-LOG.csv"]
        self._write(
            "docs/R1A-DISCOVERY-LOG.csv",
            ",".join(discovery_header) + "\n",
        )
        self._write("docs/guide.md", "# Guia\n")
        self._write("README.md", "[Guia](docs/guide.md)\n")

    def _validate(self):
        return validate_repository(self.root, run_git=False)

    def assert_validation_fails_with(self, expected_code: str) -> None:
        report, errors = self._validate()
        self.assertEqual("fail", report["status"])
        self.assertTrue(
            any(error.startswith(expected_code) for error in errors),
            f"{expected_code} não encontrado em {errors}",
        )

    def test_valid_repository_passes(self) -> None:
        report, errors = self._validate()
        self.assertEqual("pass", report["status"])
        self.assertEqual([], errors)
        self.assertEqual(1, report["counts"]["coveredSyntheticCases"])

    def test_generated_artifacts_are_outside_repository_validation(self) -> None:
        synthetic_token = "ghp_" + "not_a_real_token_value"
        self._write("artifacts/synthetic-demo/findings.csv", "not,a,valid,row\n1\n")
        self._write("artifacts/synthetic-demo/local-output.txt", synthetic_token)

        report, errors = self._validate()

        self.assertEqual("pass", report["status"])
        self.assertEqual([], errors)
        self.assertEqual(3, report["counts"]["csvFiles"])

    def test_invalid_json_fails(self) -> None:
        self._write(
            "packages/test-fixtures/configs/invalid.json",
            "{",
        )
        self.assert_validation_fails_with("JSON_INVALIDO")

    def test_expected_json_with_non_object_root_fails_cleanly(self) -> None:
        self._write(
            "packages/test-fixtures/expected/sample-lf.expected.json",
            "[]",
        )
        self.assert_validation_fails_with("JSON_RAIZ_INVALIDA")

    def test_missing_fixture_reference_fails(self) -> None:
        manifest_path = (
            self.root
            / "packages/test-fixtures/expected/sample-lf.expected.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["fixture"] = "development/missing.txt"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_validation_fails_with("FIXTURE_NAO_ENCONTRADA")

    def test_physical_line_count_mismatch_fails(self) -> None:
        manifest_path = (
            self.root
            / "packages/test-fixtures/expected/sample-lf.expected.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["totalPhysicalLines"] = 3
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_validation_fails_with("TOTAL_LINHAS_DIVERGENTE")

    def test_incomplete_ledger_fails(self) -> None:
        manifest_path = (
            self.root
            / "packages/test-fixtures/expected/sample-lf.expected.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["lineLedger"] = manifest["lineLedger"][:1]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_validation_fails_with("LEDGER_TAMANHO_DIVERGENTE")

    def test_non_contiguous_ledger_fails(self) -> None:
        manifest_path = (
            self.root
            / "packages/test-fixtures/expected/sample-lf.expected.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["lineLedger"][1]["line"] = 3
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_validation_fails_with("LEDGER_SEQUENCIA_INVALIDA")

    def test_malformed_csv_fails(self) -> None:
        coverage = self.root / "packages/test-fixtures/coverage-matrix.csv"
        coverage.write_text(
            ",".join(EXPECTED_CSV_HEADERS[coverage.relative_to(self.root).as_posix()])
            + "\nCOV-001,linha-incompleta\n",
            encoding="utf-8",
        )
        self.assert_validation_fails_with("CSV_LARGURA_INVALIDA")

    def test_required_csv_missing_fails(self) -> None:
        (self.root / "docs/R1A-DISCOVERY-LOG.csv").unlink()
        self.assert_validation_fails_with("CSV_OBRIGATORIO_AUSENTE")

    def test_broken_markdown_link_fails(self) -> None:
        self._write("README.md", "[Ausente](docs/ausente.md)\n")
        self.assert_validation_fails_with("LINK_LOCAL_QUEBRADO")

    def test_private_path_fails_without_reading_content(self) -> None:
        self._write(
            "packages/test-fixtures/validation-private/holdout.txt",
            "conteúdo que não deve ser processado",
        )
        self.assert_validation_fails_with("CAMINHO_PRIVADO")

    def test_secret_pattern_fails_without_echoing_secret(self) -> None:
        secret = "github_pat_" + "A" * 24
        self._write("docs/leak.txt", secret)
        report, errors = self._validate()
        self.assertEqual("fail", report["status"])
        self.assertTrue(
            any(error.startswith("CONTEUDO_SENSIVEL_TOKEN_GITHUB") for error in errors)
        )
        self.assertNotIn(secret, "\n".join(errors))

    def test_high_confidence_email_fails(self) -> None:
        synthetic_email = "pessoa.real" + "@" + "example.com"
        self._write("docs/contact.txt", synthetic_email)
        self.assert_validation_fails_with("CONTEUDO_SENSIVEL_EMAIL")


class R1ADiscoveryDocumentationTests(unittest.TestCase):
    def test_synthetic_list_is_short_and_hides_internal_states(self) -> None:
        content = (ROOT / "docs/R1A-SYNTHETIC-LIST.md").read_text(encoding="utf-8")
        items = [
            line
            for line in content.splitlines()
            if line.startswith("## ")
        ]

        self.assertIn("Você tem serviços para destravar", content)
        self.assertGreaterEqual(len(items), 1)
        self.assertLessEqual(len(items), 5)
        self.assertEqual(len(items), content.count("Motivo:"))
        self.assertEqual(len(items), content.count("Próxima ação:"))
        for internal_code in (
            "NEEDS_RESPONSE",
            "NEEDS_QUOTE",
            "FOLLOWUP_DUE",
            "PROMISED_RETURN_DUE",
            "OUT_OF_SCOPE_CANDIDATE",
        ):
            self.assertNotIn(internal_code, content)

    def test_r1a_gate_uses_providers_as_the_unit(self) -> None:
        content = " ".join(
            (ROOT / "docs/R1A-DISCOVERY.md").read_text(encoding="utf-8").split()
        )

        self.assertIn("Pelo menos 4 de 5 têm uma oportunidade candidata", content)
        self.assertIn("Pelo menos 3 de 5 confirmam pelo menos uma", content)
        self.assertIn("Pelo menos 3 de 5 executam pelo menos uma ação relevante", content)
        self.assertIn("Pelo menos 3 de 5 querem receber novamente", content)
        self.assertIn("não representam evidência estatística", content)

    def test_vertical_selection_blocks_only_the_first_session(self) -> None:
        gates = (ROOT / "docs/GATE-STATUS.md").read_text(encoding="utf-8")
        checklist = (ROOT / "docs/DISCOVERY-SESSION-READY.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("`R1A_READY` | COMPLETE", gates)
        self.assertIn("`VERTICAL_SELECTION` | `PENDING_OWNER_SELECTION`", gates)
        self.assertIn("`FIRST_R1A_SESSION` | `BLOCKED`", gates)
        self.assertIn("[ ] VERTICAL_SELECTION=COMPLETE.", checklist)
        self.assertIn("[ ] Prestador pertence à vertical selecionada.", checklist)

    def test_discovery_log_covers_substitutes_and_economic_ranges(self) -> None:
        header = EXPECTED_CSV_HEADERS["docs/R1A-DISCOVERY-LOG.csv"]

        self.assertEqual("record_type", header[0])
        for field in (
            "current_tracking_method",
            "current_method_failure",
            "crm_experience",
            "crm_abandonment_reason",
            "substitute_sufficient",
            "problem_frequency",
            "last_stalled_opportunity_range",
            "weekly_commercial_contacts_range",
            "typical_ticket_range_brl",
            "stalled_cause",
        ):
            self.assertIn(field, header)

    def test_r1b_uses_real_payments_without_redundant_acceptance_gate(self) -> None:
        content = (ROOT / "docs/R1B-COMMERCIAL-EXPERIMENT.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("`BLOCKED_UNTIL_R1A_PASS`", content)
        self.assertIn("`MONTHLY_PRICE=R$49.90`", content)
        self.assertIn("| `0` | `STOP` |", content)
        self.assertIn("| `1` | `INSUFFICIENT_EVIDENCE` |", content)
        self.assertIn("| `>=2` | `COMMERCIAL_SIGNAL_TO_INVESTIGATE` |", content)
        self.assertIn("Um pagamento recebido já comprova o aceite", content)
        self.assertIn("não existe gate separado ou redundante", content)


class QualityPageTests(unittest.TestCase):
    def test_page_contains_only_aggregate_quality_information(self) -> None:
        report = {
            "schemaVersion": "radar.quality/v1",
            "generatedAtUtc": "2026-08-03T12:00:00Z",
            "status": "pass",
            "counts": {
                "jsonFiles": 7,
                "fixtureManifests": 6,
                "physicalLines": 21,
                "coveredSyntheticCases": 18,
                "pendingSyntheticCases": 2,
            },
            "checks": [
                {
                    "id": "json",
                    "label": "JSONs sintéticos",
                    "status": "pass",
                    "summary": "7 JSON(s) válido(s)",
                }
            ],
        }

        page = build_html(report)

        self.assertIn("Ambiente de validação; não é o produto; não envie dados.", page)
        self.assertIn("connect-src 'none'", page)
        self.assertNotIn("<script", page.lower())
        self.assertNotIn("messages", page)
        self.assertNotIn("packages/test-fixtures", page)

    def test_page_rejects_failed_report(self) -> None:
        with self.assertRaises(ValueError):
            build_html({"status": "fail"})


if __name__ == "__main__":
    unittest.main()
