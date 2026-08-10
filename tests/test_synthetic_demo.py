from __future__ import annotations

import copy
import csv
import html
import json
import re
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


CUSTOMER_FAQ_PATH = ROOT / "docs" / "CUSTOMER-FAQ.md"
PILOT_BASELINE_PATH = ROOT / "docs" / "PILOT-BASELINE.md"


def visible_text(page: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", page)
    return " ".join(html.unescape(without_tags).split())


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
        scenario["chats"][0]["evidence"] = "<script>alert('x')</script>"
        summary = validate_scenario(scenario)
        page = build_html(scenario, build_result(scenario, summary))

        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("default-src 'none'", page)
        self.assertIn(NOTICE, page)
        self.assertNotIn("http://", page)
        self.assertNotIn("https://", page)

    def test_html_uses_commercial_language_in_the_approved_order(self) -> None:
        summary = validate_scenario(self.scenario)
        page = build_html(self.scenario, build_result(self.scenario, summary))
        text = visible_text(page)

        labels = [
            "Resposta acima do tempo esperado",
            "Cliente ficou sem resposta",
            "Resposta dentro da meta",
            "Não foi possível confirmar a resposta",
            "Conversa fora da análise",
        ]
        for label in labels:
            self.assertIn(label, text)

        ordered_sections = [
            "Veja onde solicitações comerciais demoraram ou terminaram sem resposta humana útil nesta amostra.",
            "O que você ganha com o serviço",
            "Resultado da amostra",
            "Evidências da amostra",
            "O que merece ação agora",
            "Como funciona com o seu WhatsApp",
            "Limitações",
        ]
        positions = [text.index(section) for section in ordered_sections]
        self.assertEqual(positions, sorted(positions))

        self.assertIn(
            "1 de 2 solicitações avaliáveis recebeu resposta acima da meta", text
        )
        self.assertIn(
            "1 de 3 solicitações elegíveis terminou sem resposta humana útil", text
        )
        self.assertIn("1 caso não permitiu confirmar se houve resposta", text)
        self.assertIn("1 conversa ficou fora da análise", text)
        self.assertNotIn("clientes ficaram sem resposta", text.lower())

    def test_html_answers_the_three_commercial_invariants(self) -> None:
        summary = validate_scenario(self.scenario)
        page = build_html(self.scenario, build_result(self.scenario, summary))
        text = visible_text(page)

        questions = [
            "Dá para fazer isso no meu WhatsApp?",
            "Você consegue descobrir quantos ficaram sem resposta?",
            "Como você faria isso com minhas conversas?",
        ]
        for question in questions:
            self.assertIn(question, text)

        required_controls = [
            "não existe integração direta",
            "20 a 50 chats individuais",
            "mídia USB criptografada",
            "senha transmitida por canal separado",
            "armazenamento local protegido",
            "manual e offline",
            "fora do Git e de pastas sincronizadas",
            "sem IA ou serviços de nuvem",
            "retenção acordada",
        ]
        for control in required_controls:
            self.assertIn(control, text)

        self.assertIn(
            "Isso não cobre todos os clientes nem todo o seu WhatsApp", text
        )
        self.assertIn("permanecem inconclusivos e separados do total", text)

    def test_html_hides_internal_tokens_but_structured_results_keep_them(self) -> None:
        summary = validate_scenario(self.scenario)
        result = build_result(self.scenario, summary)
        page = build_html(self.scenario, result)

        internal_tokens = [
            "LP-001",
            "LP-002",
            "NO_FINDING_SLA_BOUNDARY",
            "UNVERIFIABLE_RESPONSE",
            "OUT_OF_SCOPE",
            "CORRIGIR_AGORA",
            "radar.demo/v1",
            "AUDIT-METHOD-v0.1",
        ]
        for token in internal_tokens:
            self.assertNotIn(token, page)

        self.assertEqual(result["schemaVersion"], "radar.demo/v1")
        self.assertEqual(result["methodologyVersion"], "AUDIT-METHOD-v0.1")
        self.assertEqual(
            {item["classification"] for item in result["reviewedCases"]},
            {
                "LP-001",
                "LP-002",
                "NO_FINDING_SLA_BOUNDARY",
                "UNVERIFIABLE_RESPONSE",
                "OUT_OF_SCOPE",
            },
        )

    def test_html_limits_consequences_to_verifiable_facts(self) -> None:
        summary = validate_scenario(self.scenario)
        page = build_html(self.scenario, build_result(self.scenario, summary))
        text = visible_text(page)

        consequences = [
            "5 minutos acima da meta definida de 15 minutos",
            "O ciclo analisado terminou sem resposta humana útil para esta solicitação elegível",
            "exatamente na meta definida de 15 minutos",
            "o caso permanece inconclusivo",
            "excluída dos denominadores comerciais",
        ]
        for consequence in consequences:
            self.assertIn(consequence, text)

        self.assertIn(
            "Demora ou ausência de resposta não demonstra venda perdida, receita perdida, redução de conversão ou qualquer impacto financeiro",
            text,
        )

    def test_customer_faq_is_canonical_and_keeps_pilot_evaluation_separate(
        self,
    ) -> None:
        faq = CUSTOMER_FAQ_PATH.read_text(encoding="utf-8")
        baseline = PILOT_BASELINE_PATH.read_text(encoding="utf-8")
        normalized_faq = " ".join(faq.split())
        normalized_baseline = " ".join(baseline.split())

        commercial_questions = [
            "Dá para fazer isso no meu WhatsApp?",
            "Você consegue descobrir quantos ficaram sem resposta?",
            "Como você faria isso com minhas conversas?",
        ]
        for question in commercial_questions:
            self.assertIn(question, normalized_faq)

        faq_controls = [
            "não existe integração direta",
            "20 a 50 chats individuais",
            "mídia USB criptografada",
            "senha transmitida por canal separado",
            "armazenamento local protegido",
            "manualmente e offline",
            "retenção acordada",
            "descartar os dados",
        ]
        for control in faq_controls:
            self.assertIn(control, normalized_faq)

        evaluation_questions = [
            "Qual foi o objetivo da auditoria?",
            "Quais foram os principais achados?",
            "Qual ação possui maior prioridade?",
            "Qual limitação impede interpretar os achados como vendas perdidas?",
            "Qual é o próximo passo recomendado?",
        ]
        for question in evaluation_questions:
            self.assertIn(question, normalized_baseline)
            self.assertNotIn(question, normalized_faq)
        self.assertIn(
            "pelo menos quatro respostas corretas em cinco", normalized_baseline
        )

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
