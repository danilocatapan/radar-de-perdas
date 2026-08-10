#!/usr/bin/env python3
"""Gera uma demonstração visual a partir de resultados sintéticos pré-revisados."""

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
SCENARIO_PATH = DEMO_FIXTURE_ROOT / "synthetic-audit-demo.json"
NOTICE = (
    "Demonstração com dados fictícios. Não representa uma empresa real e não "
    "estima vendas perdidas."
)
COMMERCIAL_LABELS = {
    "LP-001": "Resposta acima do tempo esperado",
    "LP-002": "Cliente ficou sem resposta",
    "NO_FINDING_SLA_BOUNDARY": "Resposta dentro da meta",
    "UNVERIFIABLE_RESPONSE": "Não foi possível confirmar a resposta",
    "OUT_OF_SCOPE": "Conversa fora da análise",
}
COMMERCIAL_LIMITATIONS = [
    "Todos os chats, participantes, horários e resultados desta demonstração são fictícios.",
    "As situações apresentadas foram revisadas previamente por uma pessoa; a página não recebe nem analisa conversas do cliente.",
    "Os resultados descrevem somente esta pequena amostra e não representam todo o atendimento de uma empresa.",
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
    _require(isinstance(chats, list) and len(chats) == 5, "a demo exige cinco chats")
    _require(all(isinstance(chat, dict) for chat in chats), "chat inválido")
    ids = [chat.get("chatId") for chat in chats]
    _require(all(isinstance(chat_id, str) and chat_id for chat_id in ids), "chatId inválido")
    _require(len(set(ids)) == len(ids), "chatId duplicado")

    classifications: dict[str, dict[str, Any]] = {}
    for chat in chats:
        fixture = _safe_demo_fixture(chat.get("fixture"))
        fixture.read_text(encoding="utf-8")
        classification = chat.get("classification")
        _require(isinstance(classification, str), "classificação ausente")
        classifications[classification] = chat

    required = {
        "LP-001",
        "LP-002",
        "NO_FINDING_SLA_BOUNDARY",
        "UNVERIFIABLE_RESPONSE",
        "OUT_OF_SCOPE",
    }
    _require(set(classifications) == required, "conjunto de cenários demonstrativos inválido")

    lp001 = classifications["LP-001"]
    _require(lp001.get("businessResponseSeconds") == 1200, "LP-001 deve usar 20 minutos")
    _require(lp001.get("findingId"), "LP-001 deve possuir achado")

    boundary = classifications["NO_FINDING_SLA_BOUNDARY"]
    _require(boundary.get("businessResponseSeconds") == 900, "fronteira deve usar 15 minutos")
    _require(boundary.get("findingId") is None, "fronteira exata não pode gerar achado")

    lp002 = classifications["LP-002"]
    _require(lp002.get("cycleClosed") is True, "LP-002 exige ciclo encerrado")
    _require(lp002.get("validResponseAt") is None, "LP-002 não pode ter resposta útil")
    _require(lp002.get("unverifiableResponseCount") == 0, "LP-002 não pode ter mídia pendente")

    unverifiable = classifications["UNVERIFIABLE_RESPONSE"]
    _require(unverifiable.get("unverifiableResponseCount") == 1, "mídia deve ser não verificável")
    _require(unverifiable.get("findingId") is None, "mídia não pode gerar LP-002 automático")

    out_of_scope = classifications["OUT_OF_SCOPE"]
    _require(out_of_scope.get("requestCount") == 0, "suporte não entra nas solicitações elegíveis")

    actual_summary = summarize(chats)
    _require(scenario.get("expectedSummary") == actual_summary, "resumo esperado inconsistente")
    limitations = scenario.get("limitations")
    _require(
        isinstance(limitations, list)
        and limitations
        and all(isinstance(item, str) and item for item in limitations),
        "limitações inválidas",
    )
    return actual_summary


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
                "fixture": chat["fixture"],
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
    if classification == "NO_FINDING_SLA_BOUNDARY":
        return (
            "A resposta humana útil ocorreu exatamente na meta definida de "
            f"{sla_minutes} minutos e não gera prioridade por atraso."
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
            "Criar um alerta operacional antes de a solicitação ultrapassar a "
            "meta de 15 minutos."
        )
    if chat["classification"] == "NO_FINDING_SLA_BOUNDARY":
        return (
            "Manter o acompanhamento; o limite exato atende à meta e não exige "
            "ação por atraso."
        )
    return chat["recommendation"]


def build_html(scenario: dict[str, Any], result: dict[str, Any]) -> str:
    summary = result["summary"]
    cards = [
        (
            f'{summary["lp001"]} de {summary["lp001Denominator"]}',
            "solicitações avaliáveis recebeu resposta acima da meta",
        ),
        (
            f'{summary["lp002"]} de {summary["lp002Denominator"]}',
            "solicitações elegíveis terminou sem resposta humana útil",
        ),
        (
            summary["unverifiableResponses"],
            "caso não permitiu confirmar se houve resposta",
        ),
        (summary["outOfScope"], "conversa ficou fora da análise"),
    ]
    card_html = "\n".join(
        f'<article class="metric"><strong>{_escape(value)}</strong><span>{_escape(label)}</span></article>'
        for value, label in cards
    )

    chat_sections = []
    for index, chat in enumerate(scenario["chats"], start=1):
        fixture_path = _safe_demo_fixture(chat["fixture"])
        source = fixture_path.read_text(encoding="utf-8").strip()
        label = COMMERCIAL_LABELS[chat["classification"]]
        consequence = _commercial_consequence(
            chat, scenario["configuration"]["slaSeconds"]
        )
        recommendation = _commercial_recommendation(chat)
        chat_sections.append(
            "<article class=\"case\">"
            f"<div><span class=\"tag\">Caso {index} de {len(scenario['chats'])}</span>"
            "<span class=\"case-label\">Situação encontrada</span>"
            f"<h3>{_escape(label)}</h3>"
            f"<h4>Evidência</h4><p>{_escape(chat['evidence'])}</p>"
            f"<h4>Consequência verificável</h4><p>{_escape(consequence)}</p>"
            f"<p class=\"recommendation\"><strong>Próxima ação:</strong> {_escape(recommendation)}</p></div>"
            f"<pre aria-label=\"Trecho fictício da conversa\">{_escape(source)}</pre>"
            "</article>"
        )

    finding_recommendations = {
        chat["findingId"]: _commercial_recommendation(chat)
        for chat in scenario["chats"]
        if chat.get("findingId") is not None
    }
    finding_rows = "\n".join(
        "<tr>"
        f"<td>{_escape(COMMERCIAL_LABELS[item['type']])}</td>"
        "<td>Prioridade alta</td>"
        f"<td>{_escape(finding_recommendations[item['findingId']])}</td>"
        "</tr>"
        for item in result["findings"]
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
    body {{ margin: 0; background: radial-gradient(circle at top right, #164e63 0, #07111f 38%); }}
    main {{ width: min(1120px, calc(100% - 32px)); margin: auto; padding: 64px 0 88px; }}
    .eyebrow {{ color: #67e8f9; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; font-size: .78rem; }}
    h1 {{ max-width: 820px; margin: 12px 0 18px; font-size: clamp(2.3rem, 6vw, 4.8rem); line-height: 1; letter-spacing: -.045em; }}
    h2 {{ margin-top: 54px; }}
    h3 {{ font-size: 1.35rem; }}
    h4 {{ margin: 20px 0 4px; color: #93c5fd; font-size: .82rem; letter-spacing: .05em; text-transform: uppercase; }}
    .lead {{ max-width: 760px; color: #b8c7d9; font-size: 1.1rem; line-height: 1.65; }}
    .notice {{ margin: 28px 0; padding: 18px 20px; border: 1px solid #f59e0b; border-radius: 14px; background: #2b210c; color: #fde68a; font-weight: 750; }}
    .metric, .case, .panel, .faq {{ border: 1px solid #243a54; border-radius: 16px; background: rgba(8, 24, 42, .88); }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }}
    .metric {{ min-height: 120px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }}
    .metric strong {{ font-size: 2rem; }}
    .metric span {{ margin-top: 12px; color: #b8c7d9; line-height: 1.45; }}
    .case {{ display: grid; grid-template-columns: minmax(260px, .9fr) minmax(320px, 1.1fr); gap: 20px; padding: 22px; margin: 14px 0; }}
    .case h3 {{ margin: 10px 0; }}
    .case p {{ color: #c4d1e1; line-height: 1.55; }}
    .tag {{ display: inline-block; padding: 6px 9px; border-radius: 999px; background: #123c4a; color: #67e8f9; font-size: .72rem; font-weight: 800; }}
    .case-label {{ display: block; margin-top: 18px; color: #9db0c7; font-size: .78rem; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    pre {{ margin: 0; padding: 16px; overflow: auto; border-radius: 12px; background: #030a12; color: #dbeafe; white-space: pre-wrap; line-height: 1.5; }}
    .recommendation {{ border-left: 3px solid #22c55e; padding-left: 12px; }}
    .panel {{ padding: 22px; overflow: auto; }}
    .faq-grid {{ display: grid; gap: 14px; }}
    .faq {{ padding: 22px; }}
    .faq h3 {{ margin: 0 0 10px; }}
    .faq p, .steps {{ color: #c4d1e1; line-height: 1.6; }}
    .steps {{ padding-left: 24px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #243a54; vertical-align: top; }}
    th {{ color: #93c5fd; }}
    li {{ margin: 10px 0; color: #c4d1e1; line-height: 1.5; }}
    @media (max-width: 760px) {{
      main {{ width: min(100% - 24px, 1120px); padding-top: 40px; }}
      .case {{ grid-template-columns: 1fr; }}
      th, td {{ min-width: 150px; }}
    }}
  </style>
</head>
<body>
  <main>
    <span class="eyebrow">Radar de Perdas</span>
    <h1>Veja onde solicitações comerciais demoraram ou terminaram sem resposta humana útil nesta amostra.</h1>
    <p class="lead">O Radar de Perdas revisa uma amostra do atendimento comercial e transforma situações verificáveis em prioridades e ações de melhoria.</p>
    <aside class="notice">{_escape(NOTICE)}</aside>

    <h2>O que você ganha com o serviço</h2>
    <section class="panel">
      <ul>
        <li>Visibilidade sobre solicitações que receberam resposta depois da meta definida.</li>
        <li>Contagem de solicitações comerciais elegíveis que terminaram sem resposta humana útil dentro da amostra analisada.</li>
        <li>Separação entre situações acionáveis, casos inconclusivos e conversas fora da análise.</li>
        <li>Prioridades operacionais e recomendações ligadas a evidências revisadas.</li>
      </ul>
    </section>

    <h2>Resultado da amostra</h2>
    <p class="lead">Os números abaixo descrevem somente as conversas fictícias analisadas e mantêm separados os casos inconclusivos.</p>
    <section class="metrics">{card_html}</section>

    <h2>Evidências da amostra</h2>
    {''.join(chat_sections)}

    <h2>O que merece ação agora</h2>
    <section class="panel">
      <table>
        <thead><tr><th>Situação</th><th>Prioridade</th><th>Próxima ação</th></tr></thead>
        <tbody>{finding_rows}</tbody>
      </table>
    </section>

    <h2>Como funciona com o seu WhatsApp</h2>
    <p class="lead">O serviço atual é um piloto controlado e manual. Ele não se conecta diretamente à sua conta.</p>
    <section class="faq-grid" aria-label="Perguntas comerciais frequentes">
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
        <p>Depois da qualificação e dos aceites, você exporta somente a amostra delimitada. Os arquivos seguem em mídia USB criptografada, com a senha transmitida por canal separado, e ficam em armazenamento local protegido. A análise é manual e offline; o relatório usa evidências mínimas redigidas ou pseudonimizadas, e os dados são descartados conforme a retenção acordada.</p>
      </article>
    </section>

    <section class="panel" aria-label="Etapas do piloto controlado">
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
    </section>

    <h2>Limitações</h2>
    <section class="panel"><ul>{limitation_items}</ul></section>
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
