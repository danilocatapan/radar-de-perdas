#!/usr/bin/env python3
"""Valida documentos e fixtures sintéticas do Radar de Perdas."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit


EXPECTED_CSV_HEADERS = {
    "packages/test-fixtures/coverage-matrix.csv": [
        "case_id",
        "case",
        "required",
        "synthetic_fixture",
        "current_status",
        "real_corpus_status",
        "reviewer_notes",
    ],
    "docs/PILOT-TIME-LOG.csv": [
        "pilot_id",
        "mode",
        "activity",
        "started_at",
        "ended_at",
        "elapsed_seconds",
        "excluded_pause_seconds",
        "active_seconds",
        "notes",
    ],
    "docs/R1A-DISCOVERY-LOG.csv": [
        "record_type",
        "session_code",
        "opportunity_code",
        "state",
        "priority",
        "provider_confirmed_relevant",
        "provider_confirmed_forgotten",
        "recommended_action",
        "action_executed",
        "conversation_reactivated",
        "service_confirmed",
        "recurring_interest",
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
        "provider_active_seconds",
        "operator_active_seconds",
        "operator_travel_seconds",
        "candidate_type",
        "candidate_frequency",
        "notes",
    ],
}

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "artifacts",
    "coverage",
    "dist",
    "node_modules",
}

FORBIDDEN_PATH_PARTS = {
    "10-raw",
    "20-working",
    "holdout",
    "private",
    "real-data",
    "validation-private",
}

SECRET_PATTERNS = {
    "CHAVE_PRIVADA": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "TOKEN_GITHUB": re.compile(r"(?:gh[oprsu]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]{16,})"),
    "CHAVE_OPENAI": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "CHAVE_AWS": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "TELEFONE_BR": re.compile(
        r"(?<!\d)(?:\+?55[\s.-]*)?\(?[1-9][0-9]\)?[\s.-]*9[0-9]{4}[\s.-]*[0-9]{4}(?!\d)"
    ),
    "HASH_REAL": re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])"),
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)\n]+)\)")


@dataclass
class CheckResult:
    id: str
    label: str
    status: str
    summary: str
    errors: list[str]

    def public_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "label": self.label,
            "status": self.status,
            "summary": self.summary,
        }


def _result(
    check_id: str,
    label: str,
    errors: list[str],
    success_summary: str,
) -> CheckResult:
    return CheckResult(
        id=check_id,
        label=label,
        status="pass" if not errors else "fail",
        summary=success_summary if not errors else f"{len(errors)} falha(s)",
        errors=errors,
    )


def _repo_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_DIRECTORY_NAMES for part in relative_parts):
            continue
        yield path


def check_json_files(root: Path) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    json_files = sorted((root / "packages/test-fixtures").rglob("*.json"))
    expected_count = 0

    if not json_files:
        errors.append("JSON_AUSENTE: packages/test-fixtures")

    for path in json_files:
        relative = path.relative_to(root).as_posix()
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            location = (
                f"linha {exc.lineno}, coluna {exc.colno}"
                if isinstance(exc, json.JSONDecodeError)
                else "UTF-8 inválido"
            )
            errors.append(f"JSON_INVALIDO: {relative}: {location}")
            continue

        if not isinstance(parsed, dict):
            errors.append(f"JSON_RAIZ_INVALIDA: {relative}: objeto esperado")
        if path.name.endswith(".expected.json"):
            expected_count += 1

    return (
        _result(
            "json",
            "JSONs sintéticos",
            errors,
            f"{len(json_files)} JSON(s) válido(s)",
        ),
        {"jsonFiles": len(json_files), "expectedManifests": expected_count},
    )


def _safe_fixture_path(root: Path, relative: str) -> Path | None:
    fixture_root = (root / "packages/test-fixtures").resolve()
    candidate = (fixture_root / relative).resolve()
    try:
        candidate.relative_to(fixture_root)
    except ValueError:
        return None
    return candidate


def _physical_line_count(text: str) -> int:
    if not text:
        return 0
    line_feeds = text.count("\n")
    return line_feeds if text.endswith("\n") else line_feeds + 1


def check_expected_manifests(root: Path) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    expected_dir = root / "packages/test-fixtures/expected"
    manifests = sorted(expected_dir.glob("*.expected.json"))
    physical_lines = 0

    for manifest_path in manifests:
        relative_manifest = manifest_path.relative_to(root).as_posix()
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            # O check de JSON já produz o diagnóstico detalhado.
            continue
        if not isinstance(manifest, dict):
            # O check de JSON já registra que a raiz não é um objeto.
            continue

        fixture_reference = manifest.get("fixture")
        if not isinstance(fixture_reference, str) or not fixture_reference:
            errors.append(f"FIXTURE_AUSENTE: {relative_manifest}")
            continue

        fixture_path = _safe_fixture_path(root, fixture_reference)
        if fixture_path is None:
            errors.append(f"FIXTURE_FORA_DA_RAIZ: {relative_manifest}")
            continue
        if not fixture_path.is_file():
            errors.append(f"FIXTURE_NAO_ENCONTRADA: {relative_manifest}")
            continue

        config_reference = manifest.get("config")
        if config_reference is not None:
            if not isinstance(config_reference, str) or not config_reference:
                errors.append(f"CONFIG_INVALIDA: {relative_manifest}")
            else:
                config_path = _safe_fixture_path(root, config_reference)
                if config_path is None or not config_path.is_file():
                    errors.append(f"CONFIG_NAO_ENCONTRADA: {relative_manifest}")

        try:
            fixture_text = fixture_path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            errors.append(f"FIXTURE_UTF8_INVALIDO: {relative_manifest}")
            continue

        actual_lines = _physical_line_count(fixture_text)
        physical_lines += actual_lines
        declared_lines = manifest.get("totalPhysicalLines")
        ledger = manifest.get("lineLedger")

        if (
            not isinstance(declared_lines, int)
            or isinstance(declared_lines, bool)
            or declared_lines < 0
        ):
            errors.append(f"TOTAL_LINHAS_INVALIDO: {relative_manifest}")
            continue
        if declared_lines != actual_lines:
            errors.append(
                f"TOTAL_LINHAS_DIVERGENTE: {relative_manifest}: "
                f"declarado={declared_lines}, arquivo={actual_lines}"
            )

        if not isinstance(ledger, list):
            errors.append(f"LEDGER_INVALIDO: {relative_manifest}")
            continue
        if len(ledger) != declared_lines:
            errors.append(
                f"LEDGER_TAMANHO_DIVERGENTE: {relative_manifest}: "
                f"ledger={len(ledger)}, declarado={declared_lines}"
            )

        for expected_number, entry in enumerate(ledger, start=1):
            if not isinstance(entry, dict):
                errors.append(
                    f"LEDGER_ENTRADA_INVALIDA: {relative_manifest}: "
                    f"posição={expected_number}"
                )
                continue
            if entry.get("line") != expected_number:
                errors.append(
                    f"LEDGER_SEQUENCIA_INVALIDA: {relative_manifest}: "
                    f"posição={expected_number}"
                )
            classification = entry.get("classification")
            if not isinstance(classification, str) or not classification:
                errors.append(
                    f"LEDGER_CLASSIFICACAO_INVALIDA: {relative_manifest}: "
                    f"linha={expected_number}"
                )

    if not manifests:
        errors.append("MANIFESTO_AUSENTE: packages/test-fixtures/expected")

    return (
        _result(
            "fixtures",
            "Fixtures e line ledger",
            errors,
            f"{len(manifests)} manifesto(s), {physical_lines} linha(s)",
        ),
        {
            "fixtureManifests": len(manifests),
            "physicalLines": physical_lines,
        },
    )


def check_csv_files(root: Path) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    csv_files = sorted(
        path
        for path in root.rglob("*.csv")
        if not any(
            part in IGNORED_DIRECTORY_NAMES for part in path.relative_to(root).parts
        )
    )
    covered = 0
    pending = 0

    for required_relative in EXPECTED_CSV_HEADERS:
        if not (root / required_relative).is_file():
            errors.append(f"CSV_OBRIGATORIO_AUSENTE: {required_relative}")

    for path in csv_files:
        relative = path.relative_to(root).as_posix()
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.reader(handle, strict=True))
        except (UnicodeDecodeError, csv.Error) as exc:
            errors.append(f"CSV_INVALIDO: {relative}: {type(exc).__name__}")
            continue

        if not rows:
            errors.append(f"CSV_SEM_CABECALHO: {relative}")
            continue
        header = rows[0]
        if not header or any(not cell.strip() for cell in header):
            errors.append(f"CSV_CABECALHO_INVALIDO: {relative}")
        if len(set(header)) != len(header):
            errors.append(f"CSV_CABECALHO_DUPLICADO: {relative}")

        expected_header = EXPECTED_CSV_HEADERS.get(relative)
        if expected_header is not None and header != expected_header:
            errors.append(f"CSV_CABECALHO_DIVERGENTE: {relative}")

        for row_number, row in enumerate(rows[1:], start=2):
            if len(row) != len(header):
                errors.append(
                    f"CSV_LARGURA_INVALIDA: {relative}: linha={row_number}"
                )

        if relative == "packages/test-fixtures/coverage-matrix.csv" and header:
            try:
                status_index = header.index("current_status")
            except ValueError:
                status_index = -1
            if status_index >= 0:
                for row in rows[1:]:
                    if len(row) <= status_index:
                        continue
                    if row[status_index] == "COVERED_SYNTHETIC":
                        covered += 1
                    else:
                        pending += 1

    return (
        _result(
            "csv",
            "CSVs documentais",
            errors,
            f"{len(csv_files)} CSV(s) válido(s)",
        ),
        {
            "csvFiles": len(csv_files),
            "coveredSyntheticCases": covered,
            "pendingSyntheticCases": pending,
        },
    )


def _markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def check_markdown_links(root: Path) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    markdown_files = sorted(
        path for path in _repo_files(root) if path.suffix.lower() == ".md"
    )
    checked_links = 0

    for markdown_path in markdown_files:
        relative_markdown = markdown_path.relative_to(root).as_posix()
        try:
            content = markdown_path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            errors.append(f"MARKDOWN_UTF8_INVALIDO: {relative_markdown}")
            continue

        for match in MARKDOWN_LINK.finditer(content):
            target = _markdown_target(match.group(1))
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith("#"):
                continue

            decoded_path = unquote(parsed.path)
            if not decoded_path:
                continue
            checked_links += 1
            if decoded_path.startswith("/"):
                candidate = (root / decoded_path.lstrip("/")).resolve()
            else:
                candidate = (markdown_path.parent / decoded_path).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                errors.append(f"LINK_FORA_DA_RAIZ: {relative_markdown}")
                continue
            if not candidate.exists():
                errors.append(
                    f"LINK_LOCAL_QUEBRADO: {relative_markdown}: {decoded_path}"
                )

    return (
        _result(
            "markdown",
            "Links Markdown locais",
            errors,
            f"{len(markdown_files)} arquivo(s), {checked_links} link(s)",
        ),
        {"markdownFiles": len(markdown_files), "localMarkdownLinks": checked_links},
    )


def check_privacy_and_secrets(root: Path) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    scanned_files = 0

    for path in _repo_files(root):
        relative = path.relative_to(root)
        lowered_parts = {part.lower() for part in relative.parts}
        relative_text = relative.as_posix()

        if lowered_parts & FORBIDDEN_PATH_PARTS:
            errors.append(f"CAMINHO_PRIVADO: {relative_text}")
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            errors.append(f"ARQUIVO_DE_SEGREDO: {relative_text}")
            continue
        if path.suffix.lower() in {".key", ".pem"}:
            errors.append(f"ARQUIVO_DE_CHAVE: {relative_text}")
            continue
        if relative_text.endswith((".real.txt", ".raw.txt", "-original.txt")):
            errors.append(f"ARQUIVO_REAL_PROIBIDO: {relative_text}")
            continue

        try:
            content = path.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        scanned_files += 1
        for pattern_name, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(content):
                line_number = content.count("\n", 0, match.start()) + 1
                errors.append(
                    f"CONTEUDO_SENSIVEL_{pattern_name}: "
                    f"{relative_text}: linha={line_number}"
                )

    return (
        _result(
            "privacy",
            "Privacidade e segredos",
            errors,
            f"{scanned_files} arquivo(s) verificado(s)",
        ),
        {"privacyScannedFiles": scanned_files},
    )


def check_git_diff(root: Path, diff_base: str | None) -> tuple[CheckResult, dict[str, int]]:
    errors: list[str] = []
    targets = [f"{diff_base}...HEAD", "HEAD"] if diff_base else ["HEAD"]

    for target in targets:
        completed = subprocess.run(
            ["git", "diff", "--check", target],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode == 0:
            continue
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        errors.extend(f"DIFF_INVALIDO: {line}" for line in lines)
        if not lines:
            errors.append(f"DIFF_INVALIDO: git diff --check falhou ({target})")

    return (
        _result("diff", "Integridade do diff", errors, "git diff --check limpo"),
        {},
    )


def validate_repository(
    root: Path,
    *,
    diff_base: str | None = None,
    run_git: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    root = root.resolve()
    checks: list[CheckResult] = []
    counts: dict[str, int] = {}

    for checker in (
        check_json_files,
        check_expected_manifests,
        check_csv_files,
        check_markdown_links,
        check_privacy_and_secrets,
    ):
        result, result_counts = checker(root)
        checks.append(result)
        counts.update(result_counts)

    if run_git:
        result, result_counts = check_git_diff(root, diff_base)
        checks.append(result)
        counts.update(result_counts)

    errors = [error for check in checks for error in check.errors]
    report = {
        "schemaVersion": "radar.quality/v1",
        "generatedAtUtc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "status": "pass" if not errors else "fail",
        "counts": counts,
        "checks": [check.public_dict() for check in checks],
    }
    return report, errors


def _write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Raiz do repositório",
    )
    parser.add_argument("--report", type=Path, help="Destino do relatório agregado")
    parser.add_argument(
        "--diff-base",
        help="Commit base para executar git diff --check BASE...HEAD",
    )
    args = parser.parse_args()

    report, errors = validate_repository(
        args.root,
        diff_base=args.diff_base,
        run_git=True,
    )

    if args.report:
        _write_report(args.report, report)

    for check in report["checks"]:
        marker = "PASS" if check["status"] == "pass" else "FAIL"
        print(f"[{marker}] {check['label']}: {check['summary']}")
    for error in errors:
        print(f"  - {error}", file=sys.stderr)

    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
