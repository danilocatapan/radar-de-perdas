#!/usr/bin/env python3
"""Gera a demonstração histórica da auditoria a partir de dados sintéticos.

A representação vigente do R1A é o Markdown mínimo em
docs/R1A-SYNTHETIC-LIST.md. Este gerador permanece apenas para preservar a
regressão do material anterior e não define a experiência atual do produto.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "packages" / "test-fixtures"
DEMO_FIXTURE_ROOT = FIXTURE_ROOT / "demo"
TECHNICAL_SCENARIO_PATH = DEMO_FIXTURE_ROOT / "synthetic-audit-demo.json"
SCENARIO_PATH = DEMO_FIXTURE_ROOT / "commercial-audit-demo.json"
NOTICE = (
    "Demonstração com dados e distribuição fictícios. As taxas servem apenas "
    "para mostrar o formato da auditoria; não representam dados de mercado, "
    "uma empresa real ou frequência esperada."
)
COMMERCIAL_LABELS = {
    "LP-001": "Resposta acima do tempo esperado",
    "LP-002": "Solicitação terminou sem resposta",
    "NO_FINDING_SLA_BOUNDARY": "Resposta dentro da meta",
    "NO_FINDING_WITHIN_TARGET": "Resposta dentro da meta",
    "UNVERIFIABLE_RESPONSE": "Não foi possível confirmar a resposta",
    "OUT_OF_SCOPE": "Conversa fora da análise",
}
COMMERCIAL_LIMITATIONS = [
    "Todos os chats, participantes, horários, resultados, distribuição e taxas desta demonstração são fictícios.",
    "As situações foram revisadas previamente por uma pessoa; esta página não recebe nem analisa conversas do cliente.",
    "Os resultados descrevem somente a amostra analisada e não representam todo o atendimento, todos os clientes ou todo o WhatsApp de uma empresa.",
    "Demora ou ausência de resposta não demonstra venda perdida, receita perdida, redução de conversão ou qualquer impacto financeiro.",
]
FINDING_FIELDS = [
    "finding_id",
    "type",
    "chat_id",
    "received_at",
    "response_at",
    "business_response_seconds",
    "sla_seconds",
    "priority",
    "recommendation",
]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _safe_demo_fixture(relative: str) -> Path:
    _require(isinstance(relative, str) and relative, "fixture ausente")
    candidate = (FIXTURE_ROOT / relative).resolve()
    try:
        candidate.relative_to(DEMO_FIXTURE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("fixture fora do diretório sintético de demonstração") from exc
    _require(candidate.is_file(), "fixture sintética não encontrada")
    return candidate


def load_scenario(path: Path = SCENARIO_PATH) -> dict[str, Any]:
    scenario = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(scenario, dict), "cenário deve ser um objeto JSON")
    return scenario


def summarize(chats: list[dict[str, Any]]) -> dict[str, int]:
    useful_times = [
        chat["businessResponseSeconds"]
        for chat in chats
        if isinstance(chat.get("businessResponseSeconds"), int)
        and chat.get("lp001Eligible") is True
    ]
    return {
        "chatsReceived": len(chats),
        "chatsAccepted": sum(chat.get("scopeStatus") == "ELIGIBLE" for chat in chats),
        "chatsExcluded": sum(chat.get("scopeStatus") == "OUT_OF_SCOPE" for chat in chats),
        "eligibleRequests": sum(
            int(chat.get("requestCount", 0))
            for chat in chats
            if chat.get("scopeStatus") == "ELIGIBLE"
        ),
        "lp001": sum(chat.get("classification") == "LP-001" for chat in chats),
        "lp001Denominator": sum(chat.get("lp001Eligible") is True for chat in chats),
        "lp002": sum(chat.get("classification") == "LP-002" for chat in chats),
        "lp002Denominator": sum(chat.get("lp002Eligible") is True for chat in chats),
        "withinTarget": sum(
            chat.get("classification")
            in {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}
            for chat in chats
        ),
        "unverifiableResponses": sum(
            chat.get("classification") == "UNVERIFIABLE_RESPONSE" for chat in chats
        ),
        "outOfScope": sum(chat.get("scopeStatus") == "OUT_OF_SCOPE" for chat in chats),
        "averageUsefulResponseSeconds": round(statistics.mean(useful_times)),
        "medianUsefulResponseSeconds": round(statistics.median(useful_times)),
    }


def validate_scenario(scenario: dict[str, Any]) -> dict[str, int]:
    _require(scenario.get("schemaVersion") == "radar.demo/v1", "schema de demo inválido")
    _require(
        scenario.get("analysisMode") == "SYNTHETIC_PRE_REVIEWED",
        "modo de análise inválido",
    )
    configuration = scenario.get("configuration")
    _require(isinstance(configuration, dict), "configuração ausente")
    _require(configuration.get("slaSeconds") == 900, "SLA sintético deve ser 900 segundos")

    chats = scenario.get("chats")
    _require(isinstance(chats, list) and chats, "chats ausentes")
    _require(all(isinstance(chat, dict) for chat in chats), "chat inválido")
    ids = [chat.get("chatId") for chat in chats]
    _require(all(isinstance(chat_id, str) and chat_id for chat_id in ids), "chatId inválido")
    _require(len(set(ids)) == len(ids), "chatId duplicado")

    classifications: dict[str, list[dict[str, Any]]] = {}
    for chat in chats:
        classification = chat.get("classification")
        _require(isinstance(classification, str), "classificação ausente")
        classifications.setdefault(classification, []).append(chat)

        received_at = datetime.fromisoformat(chat.get("receivedAt", ""))
        response_at_value = chat.get("validResponseAt")
        if response_at_value is not None:
            response_at = datetime.fromisoformat(response_at_value)
            _require(response_at >= received_at, "resposta anterior à solicitação")
            business_seconds = chat.get("businessResponseSeconds")
            if isinstance(business_seconds, int):
                _require(
                    int((response_at - received_at).total_seconds()) == business_seconds,
                    "tempo de resposta inconsistente com os timestamps",
                )

        if scenario.get("scenarioPurpose") == "COMMERCIAL_DEMO":
            if chat.get("representativeEvidence") is True:
                fixture = _safe_demo_fixture(chat.get("fixture"))
                fixture.read_text(encoding="utf-8")
            else:
                _require(chat.get("fixture") is None, "fixture só é permitida em evidência representativa")

    if scenario.get("scenarioPurpose") == "COMMERCIAL_DEMO":
        _validate_commercial_scenario(scenario, classifications)
    else:
        _validate_technical_scenario(scenario, classifications)

    actual_summary = summarize(chats)
    if scenario.get("scenarioPurpose") != "COMMERCIAL_DEMO":
        actual_summary.pop("withinTarget")
    _require(scenario.get("expectedSummary") == actual_summary, "resumo esperado inconsistente")
    limitations = scenario.get("limitations")
    _require(
        isinstance(limitations, list)
        and limitations
        and all(isinstance(item, str) and item for item in limitations),
        "limitações inválidas",
    )
    return actual_summary


def _validate_commercial_scenario(
    scenario: dict[str, Any], classifications: dict[str, list[dict[str, Any]]]
) -> None:
    chats = scenario["chats"]
    _require(20 <= len(chats) <= 30, "a demo comercial exige entre 20 e 30 chats")
    required = {
        "LP-001",
        "LP-002",
        "NO_FINDING_SLA_BOUNDARY",
        "NO_FINDING_WITHIN_TARGET",
        "UNVERIFIABLE_RESPONSE",
        "OUT_OF_SCOPE",
    }
    _require(set(classifications) == required, "conjunto comercial inválido")
    finding_ids = [chat["findingId"] for chat in chats if chat.get("findingId")]
    _require(len(finding_ids) == len(set(finding_ids)), "findingId duplicado")

    representatives = [chat for chat in chats if chat.get("representativeEvidence") is True]
    representative_categories = {
        "WITHIN_TARGET"
        if chat["classification"] in {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}
        else chat["classification"]
        for chat in representatives
    }
    _require(len(representatives) == 5, "a demo comercial exige cinco evidências representativas")
    _require(
        representative_categories
        == {"LP-001", "LP-002", "WITHIN_TARGET", "UNVERIFIABLE_RESPONSE", "OUT_OF_SCOPE"},
        "evidências representativas incompletas",
    )

    for chat in classifications["LP-001"]:
        _require(chat.get("businessResponseSeconds", 0) > 900, "resposta tardia deve superar a meta")
        _require(chat.get("findingId"), "resposta tardia deve possuir achado")
    for classification in {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}:
        for chat in classifications[classification]:
            _require(0 <= chat.get("businessResponseSeconds", -1) <= 900, "resposta dentro da meta inválida")
            _require(chat.get("findingId") is None, "resposta dentro da meta não pode gerar achado")
    for chat in classifications["LP-002"]:
        _require(chat.get("cycleClosed") is True, "ausência de resposta exige ciclo encerrado")
        _require(chat.get("validResponseAt") is None, "ausência de resposta não pode ter resposta útil")
        _require(chat.get("unverifiableResponseCount") == 0, "ausência confirmada não pode ter mídia pendente")
        _require(chat.get("findingId"), "ausência de resposta deve possuir achado")
    for chat in classifications["UNVERIFIABLE_RESPONSE"]:
        _require(chat.get("unverifiableResponseCount") == 1, "caso inconclusivo deve registrar evidência não verificável")
        _require(chat.get("findingId") is None, "caso inconclusivo não pode gerar achado")
    for chat in classifications["OUT_OF_SCOPE"]:
        _require(chat.get("requestCount") == 0, "conversa fora do escopo não entra nas solicitações elegíveis")


def _validate_technical_scenario(
    scenario: dict[str, Any], classifications: dict[str, list[dict[str, Any]]]
) -> None:
    chats = scenario["chats"]
    _require(len(chats) == 5, "a fixture técnica exige cinco chats")
    required = {
        "LP-001",
        "LP-002",
        "NO_FINDING_SLA_BOUNDARY",
        "UNVERIFIABLE_RESPONSE",
        "OUT_OF_SCOPE",
    }
    _require(set(classifications) == required, "conjunto de cenários demonstrativos inválido")
    for chat in chats:
        fixture = _safe_demo_fixture(chat.get("fixture"))
        fixture.read_text(encoding="utf-8")

    lp001 = classifications["LP-001"][0]
    _require(lp001.get("businessResponseSeconds") == 1200, "LP-001 deve usar 20 minutos")
    _require(lp001.get("findingId"), "LP-001 deve possuir achado")

    boundary = classifications["NO_FINDING_SLA_BOUNDARY"][0]
    _require(boundary.get("businessResponseSeconds") == 900, "fronteira deve usar 15 minutos")
    _require(boundary.get("findingId") is None, "fronteira exata não pode gerar achado")

    lp002 = classifications["LP-002"][0]
    _require(lp002.get("cycleClosed") is True, "LP-002 exige ciclo encerrado")
    _require(lp002.get("validResponseAt") is None, "LP-002 não pode ter resposta útil")
    _require(lp002.get("unverifiableResponseCount") == 0, "LP-002 não pode ter mídia pendente")

    unverifiable = classifications["UNVERIFIABLE_RESPONSE"][0]
    _require(unverifiable.get("unverifiableResponseCount") == 1, "mídia deve ser não verificável")
    _require(unverifiable.get("findingId") is None, "mídia não pode gerar LP-002 automático")

    out_of_scope = classifications["OUT_OF_SCOPE"][0]
    _require(out_of_scope.get("requestCount") == 0, "suporte não entra nas solicitações elegíveis")


def _percent(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "INCONCLUSIVE"
    return f"{(numerator / denominator) * 100:.1f}%"


def build_result(scenario: dict[str, Any], summary: dict[str, int]) -> dict[str, Any]:
    configuration = scenario["configuration"]
    findings = []
    for chat in scenario["chats"]:
        if chat.get("findingId") is None:
            continue
        findings.append(
            {
                "findingId": chat["findingId"],
                "type": chat["classification"],
                "chatId": chat["chatId"],
                "receivedAt": chat["receivedAt"],
                "responseAt": chat["validResponseAt"],
                "businessResponseSeconds": chat["businessResponseSeconds"],
                "slaSeconds": configuration["slaSeconds"],
                "priority": chat["priority"],
                "evidence": chat["evidence"],
                "recommendation": chat["recommendation"],
            }
        )

    return {
        "schemaVersion": "radar.demo/v1",
        "analysisMode": "SYNTHETIC_PRE_REVIEWED",
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "notice": NOTICE,
        "methodologyVersion": scenario["methodologyVersion"],
        "configuration": configuration,
        "summary": {
            **summary,
            "lp001Rate": _percent(summary["lp001"], summary["lp001Denominator"]),
            "lp002Rate": _percent(summary["lp002"], summary["lp002Denominator"]),
        },
        "findings": findings,
        "reviewedCases": [
            {
                "chatId": chat["chatId"],
                "fixture": chat.get("fixture"),
                "representativeEvidence": chat.get("representativeEvidence", False),
                "scopeStatus": chat["scopeStatus"],
                "classification": chat["classification"],
                "evidence": chat["evidence"],
                "recommendation": chat["recommendation"],
            }
            for chat in scenario["chats"]
        ],
        "limitations": scenario["limitations"],
    }


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _commercial_consequence(chat: dict[str, Any], sla_seconds: int) -> str:
    classification = chat["classification"]
    sla_minutes = sla_seconds // 60
    if classification == "LP-001":
        difference_minutes = (chat["businessResponseSeconds"] - sla_seconds) // 60
        return (
            "A resposta humana útil ocorreu "
            f"{difference_minutes} minutos acima da meta definida de "
            f"{sla_minutes} minutos."
        )
    if classification == "LP-002":
        return (
            "O ciclo analisado terminou sem resposta humana útil para esta "
            "solicitação elegível."
        )
    if classification in {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}:
        response_minutes = chat["businessResponseSeconds"] // 60
        return (
            f"A resposta humana útil ocorreu em {response_minutes} minutos, "
            f"dentro da meta definida de {sla_minutes} minutos."
        )
    if classification == "UNVERIFIABLE_RESPONSE":
        return (
            "A evidência disponível não permite confirmar se houve resposta "
            "humana útil; o caso permanece inconclusivo."
        )
    return (
        "A conversa foi excluída dos denominadores comerciais porque pertence "
        "ao atendimento de suporte."
    )


def _commercial_recommendation(chat: dict[str, Any]) -> str:
    if chat["classification"] == "LP-001":
        return (
            "Definir uma rotina de triagem das novas solicitações antes do "
            "limite de 15 minutos e atribuir um responsável pelo "
            "acompanhamento das pendências."
        )
    if chat["classification"] == "LP-002":
        return (
            "Adotar uma revisão diária das solicitações comerciais ainda sem "
            "resposta e atribuir explicitamente um responsável pelo retorno."
        )
    if chat["classification"] in {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}:
        return (
            "Manter a rotina atual e repetir a medição na próxima amostra."
        )
    return chat["recommendation"]


def _representative_chat(scenario: dict[str, Any], classifications: set[str]) -> dict[str, Any]:
    matches = [
        chat
        for chat in scenario["chats"]
        if chat.get("representativeEvidence") is True
        and chat["classification"] in classifications
    ]
    _require(len(matches) == 1, "evidência representativa ambígua")
    return matches[0]


def _representative_source(chat: dict[str, Any]) -> str:
    return _safe_demo_fixture(chat["fixture"]).read_text(encoding="utf-8").strip()


def build_html(scenario: dict[str, Any], result: dict[str, Any]) -> str:
    summary = result["summary"]
    cards = [
        (summary["chatsReceived"], "conversas fictícias revisadas", "neutral"),
        (summary["eligibleRequests"], "solicitações comerciais elegíveis", "neutral"),
        (
            f'{summary["lp001"]} de {summary["lp001Denominator"]}',
            "respostas avaliáveis ficaram acima da meta",
            "alert",
        ),
        (
            f'{summary["lp002"]} de {summary["lp002Denominator"]}',
            "solicitações elegíveis terminaram sem resposta humana útil",
            "alert",
        ),
        (
            summary["unverifiableResponses"],
            "casos permaneceram inconclusivos",
            "muted",
        ),
        (summary["outOfScope"], "conversas ficaram fora da análise", "muted"),
    ]
    card_html = "\n".join(
        f'<article class="metric metric--{kind}"><strong>{_escape(value)}</strong><span>{_escape(label)}</span></article>'
        for value, label, kind in cards
    )

    late = _representative_chat(scenario, {"LP-001"})
    unanswered = _representative_chat(scenario, {"LP-002"})
    within = _representative_chat(
        scenario, {"NO_FINDING_SLA_BOUNDARY", "NO_FINDING_WITHIN_TARGET"}
    )
    inconclusive = _representative_chat(scenario, {"UNVERIFIABLE_RESPONSE"})
    excluded = _representative_chat(scenario, {"OUT_OF_SCOPE"})
    sla_seconds = scenario["configuration"]["slaSeconds"]

    priority_articles = [
        (
            "Prioridade principal",
            unanswered,
            f'{summary["lp002"]} de {summary["lp002Denominator"]} solicitações elegíveis para esta análise encerraram o ciclo sem resposta humana útil.',
            "A revisão da amostra encontrou solicitações comerciais elegíveis cujo ciclo terminou sem resposta humana útil.",
            "A solicitação permaneceu pendente até o encerramento do ciclo usado na auditoria; isso confirma ausência de resposta útil na amostra, não perda de venda.",
            "Acompanhar quantas solicitações elegíveis continuam encerrando o ciclo sem resposta humana útil.",
        ),
        (
            "Segunda prioridade",
            late,
            f'{summary["lp001"]} de {summary["lp001Denominator"]} solicitações avaliáveis para tempo de resposta ficaram acima da meta definida.',
            "A revisão identificou respostas humanas úteis que chegaram depois da meta de 15 minutos.",
            _commercial_consequence(late, sla_seconds),
            "Repetir a medição e acompanhar a proporção de solicitações avaliáveis que continuam ultrapassando a meta.",
        ),
    ]
    priority_html = "\n".join(
        "<article class=\"priority-card\">"
        f"<span class=\"priority-rank\">{_escape(rank)}</span>"
        "<span class=\"field-label\">Situação encontrada</span>"
        f"<h3>{_escape(COMMERCIAL_LABELS[chat['classification']])}</h3>"
        f"<p>{_escape(situation)}</p>"
        "<div class=\"priority-grid\">"
        f"<div><h4>Resultado na amostra</h4><p class=\"result\">{_escape(result_text)}</p></div>"
        f"<div><h4>Evidência</h4><p>{_escape(chat['evidence'])}</p></div>"
        f"<div><h4>Consequência verificável</h4><p>{_escape(consequence)}</p></div>"
        f"<div><h4>Recomendação operacional</h4><p>{_escape(_commercial_recommendation(chat))}</p></div>"
        f"<div class=\"measure\"><h4>Como acompanhar a melhora</h4><p>{_escape(measurement)}</p></div>"
        "</div></article>"
        for rank, chat, result_text, situation, consequence, measurement in priority_articles
    )

    evidence_html = "\n".join(
        "<article class=\"evidence-card\">"
        f"<div><span class=\"tag\">{_escape(COMMERCIAL_LABELS[chat['classification']])}</span>"
        f"<p>{_escape(chat['evidence'])}</p>"
        "<p class=\"caption\">Trecho sintético selecionado para demonstrar como o achado é sustentado, sem expor toda a amostra.</p></div>"
        f"<pre aria-label=\"Trecho fictício da conversa\">{_escape(_representative_source(chat))}</pre>"
        "</article>"
        for chat in (unanswered, late)
    )

    recommendation_html = "\n".join(
        "<article class=\"action-card\">"
        f"<span>{_escape(COMMERCIAL_LABELS[chat['classification']])}</span>"
        f"<p>{_escape(_commercial_recommendation(chat))}</p>"
        "<small>Execução a cargo da operação do cliente; o Radar identifica, prioriza e recomenda.</small>"
        "</article>"
        for chat in (unanswered, late)
    )

    measurement_html = "\n".join(
        "<article class=\"measure-card\">"
        f"<h3>{_escape(title)}</h3><p>{_escape(description)}</p>"
        "<strong>Comparar sempre numerador, denominador e critérios equivalentes entre as amostras.</strong>"
        "</article>"
        for title, description in (
            (
                "Solicitações sem resposta útil",
                "Repetir a auditoria e contar quantas solicitações elegíveis ainda encerram o ciclo sem resposta humana útil.",
            ),
            (
                "Respostas acima da meta",
                "Repetir a auditoria e medir a proporção de solicitações avaliáveis que continuam acima dos 15 minutos definidos.",
            ),
        )
    )

    informational_html = "\n".join(
        "<article class=\"info-card\">"
        f"<span class=\"tag tag--muted\">{_escape(label)}</span>"
        f"<h4>Situação</h4><p>{_escape(situation)}</p>"
        f"<h4>Evidência</h4><p>{_escape(chat['evidence'])}</p>"
        f"<h4>Como o caso é tratado</h4><p>{_escape(treatment)}</p>"
        "</article>"
        for chat, label, situation, treatment in (
            (
                within,
                "Dentro da meta",
                f'{summary["withinTarget"]} respostas avaliáveis ocorreram dentro da meta definida.',
                "Permanece fora das prioridades por atraso e compõe o denominador da medição.",
            ),
            (
                inconclusive,
                "Inconclusivo",
                f'{summary["unverifiableResponses"]} casos não permitiram confirmar se houve resposta humana útil.',
                "Permanece separado dos achados confirmados e não é contado como ausência de resposta.",
            ),
            (
                excluded,
                "Fora da análise",
                f'{summary["outOfScope"]} conversas não continham solicitação comercial elegível.',
                "É excluída dos denominadores comerciais e não gera prioridade nesta auditoria.",
            ),
        )
    )

    limitation_items = "\n".join(
        f"<li>{_escape(item)}</li>" for item in COMMERCIAL_LIMITATIONS
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'">
  <meta name="referrer" content="no-referrer">
  <title>Radar de Perdas — demonstração comercial</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #07111f; color: #eef5ff; }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: radial-gradient(circle at top right, #164e63 0, #07111f 34%, #050b14 100%); }}
    main {{ width: min(1160px, calc(100% - 32px)); margin: auto; padding: 64px 0 88px; }}
    section {{ scroll-margin-top: 20px; }}
    .eyebrow {{ color: #67e8f9; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; font-size: .78rem; }}
    h1 {{ max-width: 820px; margin: 12px 0 18px; font-size: clamp(2.3rem, 6vw, 4.8rem); line-height: 1; letter-spacing: -.045em; }}
    h2 {{ margin: 64px 0 12px; font-size: clamp(1.7rem, 3vw, 2.45rem); letter-spacing: -.025em; }}
    h3 {{ font-size: 1.35rem; }}
    h4 {{ margin: 20px 0 4px; color: #93c5fd; font-size: .82rem; letter-spacing: .05em; text-transform: uppercase; }}
    .lead {{ max-width: 760px; color: #b8c7d9; font-size: 1.1rem; line-height: 1.65; }}
    .section-intro {{ max-width: 780px; margin: 0 0 24px; color: #9fb0c5; line-height: 1.65; }}
    .notice {{ margin: 28px 0; padding: 18px 20px; border: 1px solid #f59e0b; border-radius: 14px; background: #2b210c; color: #fde68a; font-weight: 750; }}
    .metric, .priority-card, .evidence-card, .action-card, .measure-card, .info-card, .panel, .faq {{ border: 1px solid #243a54; border-radius: 18px; background: rgba(8, 24, 42, .9); box-shadow: 0 18px 45px rgba(0, 0, 0, .16); }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .metric {{ min-height: 120px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }}
    .metric strong {{ font-size: 2.15rem; letter-spacing: -.04em; }}
    .metric span {{ margin-top: 12px; color: #b8c7d9; line-height: 1.45; }}
    .metric--alert {{ border-color: #f59e0b; background: linear-gradient(145deg, rgba(93, 45, 8, .72), rgba(8, 24, 42, .94)); }}
    .metric--alert strong {{ color: #fde68a; }}
    .metric--muted {{ opacity: .76; box-shadow: none; }}
    .priority-stack, .evidence-stack {{ display: grid; gap: 18px; }}
    .priority-card {{ padding: clamp(22px, 4vw, 34px); border-color: #b45309; background: linear-gradient(140deg, rgba(69, 31, 7, .83), rgba(8, 24, 42, .95) 45%); }}
    .priority-card h3 {{ margin: 8px 0 24px; font-size: clamp(1.55rem, 3vw, 2.2rem); }}
    .priority-rank {{ display: inline-block; color: #fde68a; font-size: .82rem; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }}
    .field-label {{ display: block; margin-top: 22px; color: #9db0c7; font-size: .75rem; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; }}
    .priority-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 28px; }}
    .priority-grid p {{ color: #d2dce8; line-height: 1.6; }}
    .priority-grid .result {{ color: #fff; font-weight: 750; }}
    .priority-grid .measure {{ grid-column: 1 / -1; padding: 6px 18px; border-left: 3px solid #22c55e; background: rgba(7, 35, 31, .65); }}
    .evidence-card {{ display: grid; grid-template-columns: minmax(260px, .8fr) minmax(320px, 1.2fr); gap: 24px; padding: 24px; }}
    .evidence-card p, .action-card p, .measure-card p, .info-card p {{ color: #c4d1e1; line-height: 1.6; }}
    .caption {{ font-size: .9rem; color: #8fa2b8 !important; }}
    .tag {{ display: inline-block; padding: 6px 9px; border-radius: 999px; background: #123c4a; color: #67e8f9; font-size: .72rem; font-weight: 800; }}
    .tag--muted {{ background: #1d2c3e; color: #b6c2d0; }}
    pre {{ margin: 0; padding: 16px; overflow: auto; border-radius: 12px; background: #030a12; color: #dbeafe; white-space: pre-wrap; line-height: 1.5; }}
    .action-grid, .measure-grid, .info-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
    .action-card, .measure-card, .info-card {{ padding: 24px; }}
    .action-card {{ border-left: 4px solid #22c55e; }}
    .action-card span {{ color: #86efac; font-size: .78rem; font-weight: 850; letter-spacing: .06em; text-transform: uppercase; }}
    .action-card small {{ display: block; color: #8fa2b8; line-height: 1.5; }}
    .measure-card strong {{ display: block; margin-top: 18px; color: #93c5fd; line-height: 1.5; }}
    .info-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    .info-card {{ opacity: .82; box-shadow: none; }}
    .panel {{ padding: 22px; overflow: auto; }}
    .faq-grid {{ display: grid; gap: 14px; }}
    .faq {{ padding: 22px; }}
    .faq h3 {{ margin: 0 0 10px; }}
    .faq p, .steps {{ color: #c4d1e1; line-height: 1.6; }}
    .steps {{ padding-left: 24px; }}
    li {{ margin: 10px 0; color: #c4d1e1; line-height: 1.5; }}
    .boundary {{ margin-top: 18px; padding: 16px 18px; border-radius: 12px; background: #0c2b2a; color: #a7f3d0; line-height: 1.55; }}
    @media (max-width: 760px) {{
      main {{ width: min(100% - 24px, 1120px); padding-top: 40px; }}
      .metrics, .priority-grid, .evidence-card, .action-grid, .measure-grid, .info-grid {{ grid-template-columns: 1fr; }}
      .priority-grid .measure {{ grid-column: auto; }}
      .metric {{ min-height: 104px; }}
      .priority-card, .evidence-card, .action-card, .measure-card, .info-card {{ padding: 20px; }}
    }}
  </style>
</head>
<body>
  <main>
    <span class="eyebrow">Radar de Perdas</span>
    <h1>Veja onde solicitações comerciais demoraram ou terminaram sem resposta humana útil nesta amostra.</h1>
    <p class="lead">O Radar identifica, quantifica e evidencia situações verificáveis, prioriza o que merece atenção e recomenda ações operacionais para a equipe executar.</p>
    <aside class="notice">{_escape(NOTICE)}</aside>

    <section id="proposta-de-valor" aria-labelledby="titulo-proposta">
      <h2 id="titulo-proposta">Proposta de valor</h2>
      <div class="panel">
      <ul>
        <li>Identificação dos problemas de atendimento confirmados dentro da amostra.</li>
        <li>Quantificação com denominadores claros, evidências mínimas e prioridades comparáveis.</li>
        <li>Recomendações operacionais e indicadores para verificar posteriormente se houve melhora.</li>
        <li>Separação rigorosa entre achados, casos inconclusivos e conversas fora da análise.</li>
      </ul>
      </div>
    </section>

    <section id="resumo-executivo" aria-labelledby="titulo-resumo">
      <h2 id="titulo-resumo">Resumo executivo da amostra</h2>
      <p class="section-intro">Os números descrevem somente esta amostra fictícia. Casos inconclusivos e conversas fora do escopo permanecem separados dos achados confirmados.</p>
      <div class="metrics">{card_html}</div>
    </section>

    <section id="problemas-prioritarios" aria-labelledby="titulo-problemas">
      <h2 id="titulo-problemas">Problemas que merecem atenção</h2>
      <p class="section-intro">Duas prioridades concentram a ação. Cada uma liga o resultado observado à evidência, à consequência que pode ser afirmada e a uma rotina operacional mensurável.</p>
      <div class="priority-stack">{priority_html}</div>
    </section>

    <section id="evidencias" aria-labelledby="titulo-evidencias">
      <h2 id="titulo-evidencias">Evidências representativas</h2>
      <p class="section-intro">A página mostra apenas os trechos necessários para demonstrar o rigor da auditoria. As métricas continuam derivadas dos 25 registros estruturados.</p>
      <div class="evidence-stack">{evidence_html}</div>
    </section>

    <section id="recomendacoes" aria-labelledby="titulo-recomendacoes">
      <h2 id="titulo-recomendacoes">Recomendações operacionais</h2>
      <p class="section-intro">O Radar recomenda ações; não implementa alertas, filas, mensagens ou integrações. A execução e a definição de responsáveis cabem à operação do cliente.</p>
      <div class="action-grid">{recommendation_html}</div>
      <div class="boundary"><strong>Fronteira de responsabilidade:</strong> identificar, quantificar, evidenciar, priorizar e recomendar fazem parte da auditoria. Executar as mudanças e acompanhar a rotina é responsabilidade do cliente.</div>
    </section>

    <section id="acompanhamento" aria-labelledby="titulo-acompanhamento">
      <h2 id="titulo-acompanhamento">Como acompanhar se houve melhora</h2>
      <p class="section-intro">Uma nova medição com critérios equivalentes permite observar a direção dos indicadores sem prometer causalidade ou resultado financeiro.</p>
      <div class="measure-grid">{measurement_html}</div>
    </section>

    <section id="whatsapp" aria-labelledby="titulo-whatsapp">
      <h2 id="titulo-whatsapp">Como funciona com o seu WhatsApp</h2>
      <p class="lead">O serviço atual é um piloto controlado, manual e offline. Ele não se conecta diretamente à sua conta.</p>
      <div class="faq-grid" aria-label="Perguntas comerciais frequentes">
      <article class="faq">
        <h3>Dá para fazer isso no meu WhatsApp?</h3>
        <p>Sim, por meio de um piloto controlado. Hoje não existe integração direta com a sua conta do WhatsApp. Depois da qualificação, da definição de período, expediente e meta, dos aceites e dos controles de privacidade, você exporta legitimamente apenas a amostra acordada de 20 a 50 chats individuais.</p>
      </article>
      <article class="faq">
        <h3>Você consegue descobrir quantos ficaram sem resposta?</h3>
        <p>Na amostra analisada e segundo os critérios definidos, contamos solicitações comerciais elegíveis que terminaram sem uma resposta humana útil. Isso não cobre todos os clientes nem todo o seu WhatsApp. Casos cuja resposta não pode ser confirmada permanecem inconclusivos e separados do total.</p>
      </article>
      <article class="faq">
        <h3>Como você faria isso com minhas conversas?</h3>
        <p>Depois da qualificação e dos aceites, você exporta somente a amostra delimitada. Os arquivos seguem em mídia USB criptografada, com a senha transmitida por canal separado, e ficam em armazenamento local protegido, fora do Git e de pastas sincronizadas. A análise é manual e offline, sem IA ou serviços de nuvem sobre as conversas reais; o relatório usa evidências mínimas redigidas ou pseudonimizadas, e os dados são descartados conforme a retenção acordada.</p>
      </article>
      </div>

      <div class="panel" aria-label="Etapas do piloto controlado">
      <h3>Etapas do piloto</h3>
      <ol class="steps">
        <li>Qualificamos a empresa e o tipo de conversa.</li>
        <li>Definimos período, expediente e meta de resposta.</li>
        <li>Formalizamos os aceites e concluímos os controles de privacidade antes de receber dados reais.</li>
        <li>Você exporta legitimamente somente a amostra acordada de 20 a 50 chats individuais.</li>
        <li>A transferência ocorre em mídia USB criptografada, com a senha enviada por canal separado.</li>
        <li>Os arquivos ficam em armazenamento local protegido, fora do Git e de pastas sincronizadas.</li>
        <li>A análise é manual e offline, sem IA ou serviços de nuvem sobre as conversas reais.</li>
        <li>Entregamos um relatório redigido ou pseudonimizado, apresentamos os resultados e descartamos os dados conforme a retenção acordada.</li>
      </ol>
      </div>
    </section>

    <section id="casos-sem-achado" aria-labelledby="titulo-casos-sem-achado">
      <h2 id="titulo-casos-sem-achado">Casos tratados sem gerar achado</h2>
      <p class="section-intro">Estes casos demonstram os limites da contagem e o motivo de nem toda conversa se transformar em problema confirmado.</p>
      <div class="info-grid">{informational_html}</div>
    </section>

    <section id="limitacoes" aria-labelledby="titulo-limitacoes">
      <h2 id="titulo-limitacoes">Limitações e privacidade</h2>
      <div class="panel"><ul>{limitation_items}</ul></div>
    </section>
  </main>
</body>
</html>
"""


def write_outputs(output_dir: Path, scenario: dict[str, Any]) -> dict[str, Path]:
    summary = validate_scenario(scenario)
    result = build_result(scenario, summary)
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "index.html"
    json_path = output_dir / "result.json"
    csv_path = output_dir / "findings.csv"

    html_path.write_text(build_html(scenario, result), encoding="utf-8")
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FINDING_FIELDS)
        writer.writeheader()
        for finding in result["findings"]:
            writer.writerow(
                {
                    "finding_id": finding["findingId"],
                    "type": finding["type"],
                    "chat_id": finding["chatId"],
                    "received_at": finding["receivedAt"],
                    "response_at": finding["responseAt"] or "",
                    "business_response_seconds": finding["businessResponseSeconds"] or "",
                    "sla_seconds": finding["slaSeconds"],
                    "priority": finding["priority"],
                    "recommendation": finding["recommendation"],
                }
            )
    return {"HTML": html_path, "JSON": json_path, "CSV": csv_path}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        outputs = write_outputs(args.output_dir, load_scenario())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        return 1

    print("STATUS=PASS")
    print("MODE=SYNTHETIC_PRE_REVIEWED")
    for label, path in outputs.items():
        print(f"{label}={path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
