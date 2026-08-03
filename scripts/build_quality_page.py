#!/usr/bin/env python3
"""Gera o painel público agregado de qualidade."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


COUNT_LABELS = {
    "jsonFiles": "JSONs validados",
    "fixtureManifests": "Manifestos de fixture",
    "physicalLines": "Linhas físicas contabilizadas",
    "coveredSyntheticCases": "Casos sintéticos cobertos",
    "pendingSyntheticCases": "Casos sintéticos pendentes",
}


def build_html(report: dict[str, Any]) -> str:
    if report.get("status") != "pass":
        raise ValueError("o painel só pode ser gerado a partir de validação verde")

    generated_at = html.escape(str(report.get("generatedAtUtc", "não informado")))
    counts = report.get("counts", {})
    checks = report.get("checks", [])

    cards = "\n".join(
        (
            '<div class="metric">'
            f'<span class="metric-value">{html.escape(str(counts.get(key, 0)))}</span>'
            f'<span class="metric-label">{html.escape(label)}</span>'
            "</div>"
        )
        for key, label in COUNT_LABELS.items()
    )
    check_items = "\n".join(
        (
            '<li class="check">'
            '<span class="check-mark" aria-hidden="true">✓</span>'
            "<span>"
            f"<strong>{html.escape(str(check.get('label', 'Check')))}</strong>"
            f"<small>{html.escape(str(check.get('summary', 'Aprovado')))}</small>"
            "</span>"
            "</li>"
        )
        for check in checks
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'">
  <meta name="referrer" content="no-referrer">
  <title>Radar de Perdas — Qualidade</title>
  <style>
    :root {{
      color-scheme: dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #08111f;
      color: #e8eef7;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at top, #17345a 0, #08111f 46%); }}
    main {{ width: min(980px, calc(100% - 32px)); margin: 0 auto; padding: 72px 0; }}
    .eyebrow {{ color: #7dd3fc; font-size: .78rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }}
    h1 {{ max-width: 720px; margin: 12px 0 16px; font-size: clamp(2.4rem, 7vw, 5.2rem); line-height: .98; letter-spacing: -.055em; }}
    .lead {{ max-width: 680px; color: #b7c4d6; font-size: 1.14rem; line-height: 1.65; }}
    .status {{ display: inline-flex; align-items: center; gap: 10px; margin: 24px 0 0; padding: 10px 14px; border: 1px solid #1f9d69; border-radius: 999px; background: #0c2d25; color: #86efac; font-weight: 750; }}
    .status-dot {{ width: 9px; height: 9px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 16px #4ade80; }}
    .notice {{ margin: 36px 0; padding: 18px 20px; border-left: 4px solid #fbbf24; border-radius: 8px; background: #2b2310; color: #fde68a; font-weight: 700; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin: 34px 0; }}
    .metric, .panel {{ border: 1px solid #24364f; border-radius: 16px; background: rgba(10, 23, 41, .86); box-shadow: 0 18px 50px rgba(0, 0, 0, .18); }}
    .metric {{ min-height: 130px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; }}
    .metric-value {{ font-size: 2.25rem; font-weight: 800; letter-spacing: -.04em; }}
    .metric-label {{ color: #9fb0c6; font-size: .9rem; line-height: 1.35; }}
    .panel {{ padding: 26px; }}
    h2 {{ margin: 0 0 18px; font-size: 1.25rem; }}
    ul {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 12px; }}
    .check {{ display: flex; align-items: flex-start; gap: 12px; padding: 13px 0; border-bottom: 1px solid #1b2b42; }}
    .check:last-child {{ border-bottom: 0; }}
    .check-mark {{ display: grid; place-items: center; flex: 0 0 26px; height: 26px; border-radius: 50%; background: #123c2c; color: #86efac; font-weight: 900; }}
    .check strong, .check small {{ display: block; }}
    .check small {{ margin-top: 3px; color: #91a3ba; }}
    footer {{ margin-top: 24px; color: #71839a; font-size: .83rem; }}
  </style>
</head>
<body>
  <main>
    <span class="eyebrow">Radar de Perdas</span>
    <h1>Painel público de qualidade</h1>
    <p class="lead">Evidência agregada da última validação aprovada na branch principal. Nenhum conteúdo de conversa ou dado operacional é publicado aqui.</p>
    <div class="status"><span class="status-dot"></span>Última validação verde</div>
    <aside class="notice">Ambiente de validação; não é o produto; não envie dados.</aside>
    <section class="metrics" aria-label="Métricas agregadas">
      {cards}
    </section>
    <section class="panel">
      <h2>Verificações executadas</h2>
      <ul>
        {check_items}
      </ul>
    </section>
    <footer>Relatório gerado em {generated_at}. O frontend funcional permanece bloqueado pelos gates do produto.</footer>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(build_html(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
