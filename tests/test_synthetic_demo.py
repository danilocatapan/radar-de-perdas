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
    TECHNICAL_SCENARIO_PATH,
    build_html,
    build_result,
    load_scenario,
    summarize,
    validate_scenario,
    write_outputs,
)


AGENTS_PATH = ROOT / "AGENTS.md"
CUSTOMER_FAQ_PATH = ROOT / "docs" / "CUSTOMER-FAQ.md"
PERSONA_PATH = ROOT / "docs" / "AGENT-PERSONA-USUARIO.md"
PILOT_BASELINE_PATH = ROOT / "docs" / "PILOT-BASELINE.md"


def visible_text(page: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", page)
    return " ".join(html.unescape(without_tags).split())


class SyntheticDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = load_scenario()
        self.summary = validate_scenario(self.scenario)

    def page(self) -> str:
        return build_html(self.scenario, build_result(self.scenario, self.summary))

    def test_commercial_scenario_has_25_plausible_chats_and_derived_metrics(self) -> None:
        self.assertEqual(
            self.summary,
            {
                "chatsReceived": 25,
                "chatsAccepted": 21,
                "chatsExcluded": 4,
                "eligibleRequests": 21,
                "lp001": 4,
                "lp001Denominator": 15,
                "lp002": 3,
                "lp002Denominator": 18,
                "withinTarget": 11,
                "unverifiableResponses": 3,
                "outOfScope": 4,
                "averageUsefulResponseSeconds": 888,
                "medianUsefulResponseSeconds": 720,
            },
        )
        classifications = [chat["classification"] for chat in self.scenario["chats"]]
        self.assertEqual(classifications.count("LP-001"), 4)
        self.assertEqual(classifications.count("LP-002"), 3)
        self.assertEqual(classifications.count("UNVERIFIABLE_RESPONSE"), 3)
        self.assertEqual(classifications.count("OUT_OF_SCOPE"), 4)

    def test_technical_five_case_fixture_remains_supported(self) -> None:
        technical = load_scenario(TECHNICAL_SCENARIO_PATH)
        summary = validate_scenario(technical)

        self.assertEqual(summary["chatsReceived"], 5)
        self.assertEqual(summary["lp001"], 1)
        self.assertEqual(summary["lp002"], 1)
        self.assertEqual(summary["unverifiableResponses"], 1)
        self.assertNotIn("withinTarget", summary)

    def test_commercial_scenario_requires_between_20_and_30_chats(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"] = scenario["chats"][:19]

        with self.assertRaisesRegex(ValueError, "entre 20 e 30 chats"):
            validate_scenario(scenario)

    def test_exactly_five_representative_categories_are_required(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["representativeEvidence"] = False
        scenario["chats"][0].pop("fixture")

        with self.assertRaisesRegex(ValueError, "cinco evidências representativas"):
            validate_scenario(scenario)

    def test_non_representative_chat_cannot_reference_fixture(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][1]["fixture"] = "demo/lp001-delayed-response.txt"

        with self.assertRaisesRegex(ValueError, "fixture só é permitida"):
            validate_scenario(scenario)

    def test_fixture_outside_demo_directory_is_rejected(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["fixture"] = "development/android-multiline-lf.txt"

        with self.assertRaisesRegex(ValueError, "fora do diretório sintético"):
            validate_scenario(scenario)

    def test_inconsistent_summary_is_rejected(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["expectedSummary"]["lp002"] = 4

        with self.assertRaisesRegex(ValueError, "resumo esperado inconsistente"):
            validate_scenario(scenario)

    def test_response_cannot_precede_request(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["validResponseAt"] = "2026-08-03T08:59:00-03:00"

        with self.assertRaisesRegex(ValueError, "resposta anterior"):
            validate_scenario(scenario)

    def test_business_response_time_must_match_timestamps(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["businessResponseSeconds"] = 1201

        with self.assertRaisesRegex(ValueError, "tempo de resposta inconsistente"):
            validate_scenario(scenario)

    def test_inconclusive_cases_never_become_findings(self) -> None:
        result = build_result(self.scenario, self.summary)
        findings = result["findings"]

        self.assertEqual(len(findings), 7)
        self.assertEqual({finding["type"] for finding in findings}, {"LP-001", "LP-002"})
        inconclusive_ids = {
            chat["chatId"]
            for chat in self.scenario["chats"]
            if chat["classification"] == "UNVERIFIABLE_RESPONSE"
        }
        self.assertTrue(inconclusive_ids.isdisjoint({finding["chatId"] for finding in findings}))

    def test_html_escapes_content_and_keeps_strict_offline_policy(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["chats"][0]["evidence"] = "<script>alert('x')</script>"
        summary = validate_scenario(scenario)
        page = build_html(scenario, build_result(scenario, summary))

        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("default-src 'none'", page)
        self.assertIn(NOTICE, visible_text(page))
        self.assertNotIn("http://", page)
        self.assertNotIn("https://", page)
        self.assertNotIn("<script", page)

    def test_html_uses_required_information_architecture(self) -> None:
        page = self.page()
        ordered_sections = [
            'id="proposta-de-valor"',
            'id="resumo-executivo"',
            'id="problemas-prioritarios"',
            'id="evidencias"',
            'id="recomendacoes"',
            'id="acompanhamento"',
            'id="whatsapp"',
            'id="casos-sem-achado"',
            'id="limitacoes"',
        ]
        positions = [page.index(section) for section in ordered_sections]
        self.assertEqual(positions, sorted(positions))

    def test_html_surfaces_derived_counts_and_only_two_priorities(self) -> None:
        text = visible_text(self.page())

        required_results = [
            "25 conversas fictícias revisadas",
            "21 solicitações comerciais elegíveis",
            "4 de 15 respostas avaliáveis ficaram acima da meta",
            "3 de 18 solicitações elegíveis terminaram sem resposta humana útil",
            "3 casos permaneceram inconclusivos",
            "4 conversas ficaram fora da análise",
        ]
        for result in required_results:
            self.assertIn(result, text)
        self.assertEqual(text.count("Situação encontrada"), 2)
        self.assertEqual(text.count("Resultado na amostra"), 2)
        self.assertEqual(text.count("Consequência verificável"), 2)
        self.assertEqual(text.count("Como acompanhar a melhora"), 2)

    def test_html_uses_operational_recommendations_and_responsibility_boundary(self) -> None:
        text = visible_text(self.page())

        self.assertIn("Recomendação operacional", text)
        self.assertNotIn("Próxima ação", text)
        self.assertNotIn("Criar um alerta operacional", text)
        self.assertIn("Definir uma rotina de triagem", text)
        self.assertIn("Adotar uma revisão diária", text)
        self.assertIn("Execução a cargo da operação do cliente", text)
        self.assertIn("não implementa alertas, filas, mensagens ou integrações", text)

    def test_html_hides_internal_tokens_but_structured_results_keep_them(self) -> None:
        result = build_result(self.scenario, self.summary)
        page = build_html(self.scenario, result)

        internal_tokens = [
            "LP-001",
            "LP-002",
            "NO_FINDING_SLA_BOUNDARY",
            "NO_FINDING_WITHIN_TARGET",
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
        self.assertIn("NO_FINDING_WITHIN_TARGET", {case["classification"] for case in result["reviewedCases"]})
        self.assertTrue(any(case["fixture"] is None for case in result["reviewedCases"]))

    def test_html_separates_informational_cases_from_confirmed_findings(self) -> None:
        text = visible_text(self.page())

        self.assertIn("11 respostas avaliáveis ocorreram dentro da meta", text)
        self.assertIn("Permanece separado dos achados confirmados", text)
        self.assertIn("É excluída dos denominadores comerciais", text)
        self.assertIn("não é contado como ausência de resposta", text)

    def test_html_states_synthetic_limits_without_financial_claims(self) -> None:
        text = visible_text(self.page())

        self.assertIn("distribuição e taxas desta demonstração são fictícios", text)
        self.assertIn("não representam dados de mercado", text)
        self.assertIn("não demonstra venda perdida, receita perdida, redução de conversão", text)
        self.assertNotIn("vendas que você perdeu", text.lower())

    def test_html_answers_the_three_commercial_invariants(self) -> None:
        text = visible_text(self.page())

        for question in (
            "Dá para fazer isso no meu WhatsApp?",
            "Você consegue descobrir quantos ficaram sem resposta?",
            "Como você faria isso com minhas conversas?",
        ):
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
        self.assertIn("Isso não cobre todos os clientes nem todo o seu WhatsApp", text)
        self.assertIn("permanecem inconclusivos e separados do total", text)

    def test_customer_faq_is_canonical_for_discovery(self) -> None:
        faq = " ".join(CUSTOMER_FAQ_PATH.read_text(encoding="utf-8").split())
        baseline = " ".join(PILOT_BASELINE_PATH.read_text(encoding="utf-8").split())

        discovery_questions = [
            "Dá para fazer isso no meu WhatsApp?",
            "O que vocês procuram?",
            "Vocês conseguem contar todos os clientes sem resposta?",
            "Como vocês usam minhas conversas?",
        ]
        for question in discovery_questions:
            self.assertIn(question, faq)

        self.assertIn("sem custódia, sem cópia e sem retenção", faq)
        self.assertIn("SUPERSEDED_FOR_CURRENT_R1A", baseline)

    def test_persona_gate_is_canonical_and_referenced_by_agents(self) -> None:
        agents = AGENTS_PATH.read_text(encoding="utf-8")
        persona = PERSONA_PATH.read_text(encoding="utf-8")

        self.assertIn("docs/AGENT-PERSONA-USUARIO.md", agents)
        self.assertIn("nota 9,0 não bloqueiam", agents)
        for field in (
            "mobile_readability=",
            "next_action_clarity=",
            "internal_codes_hidden=",
            "critical_failures=",
            "external_validation=",
            "USER_VISUAL_REVIEW_REQUIRED",
        ):
            self.assertIn(field, persona)

    def test_write_outputs_generates_html_json_and_seven_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outputs = write_outputs(Path(temporary), self.scenario)

            self.assertEqual(set(outputs), {"HTML", "JSON", "CSV"})
            self.assertTrue(all(path.is_file() for path in outputs.values()))
            result = json.loads(outputs["JSON"].read_text(encoding="utf-8"))
            self.assertEqual(result["schemaVersion"], "radar.demo/v1")
            self.assertEqual(result["analysisMode"], "SYNTHETIC_PRE_REVIEWED")
            self.assertEqual(len(result["findings"]), 7)
            with outputs["CSV"].open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 7)
            self.assertEqual({row["type"] for row in rows}, {"LP-001", "LP-002"})

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
