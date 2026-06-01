#!/usr/bin/env python3
"""Validate evidence-backed CV/resume claims.

This script reads JSON-compatible YAML files from data/ and scans variant
documents for unsupported high-risk wording. It is not a semantic proof system;
it is a practical guardrail against accidental overclaiming.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_EXTENSIONS = {".tex", ".adoc"}
METRIC_RE = re.compile(
    r"(\b\d+(?:\.\d+)?\s*(?:%|x)\b|\b\d+\+\b|EUR\s*\d|\\texteuro\{\}\d)",
    re.IGNORECASE,
)


def load_json_yaml(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_variant_docs(paths: list[Path]) -> list[Path]:
    docs: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in DOC_EXTENSIONS:
            docs.append(path)
        elif path.is_dir():
            docs.extend(p for p in path.rglob("*") if p.suffix.lower() in DOC_EXTENSIONS)
    return sorted(set(docs))


def variant_id_for(path: Path) -> str | None:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return None
    return rel.parts[0] if rel.parts and rel.parts[0].startswith("v") else None


def claim_markers(claim: dict) -> list[str]:
    text = claim["public_claim"]
    words = re.findall(r"[A-Za-z0-9:+#/.]+", text)
    markers: list[str] = []
    for size in (5, 4, 3):
        for i in range(0, max(0, len(words) - size + 1)):
            phrase = " ".join(words[i : i + size])
            if any(ch.isdigit() for ch in phrase) or any(
                key.lower() in phrase.lower()
                for key in ["Cable", "YieldStar", "E-pin", "QTool", "Surface", "MURAB", "SCFS", "RFI"]
            ):
                markers.append(phrase.lower())
    return markers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("v")],
        help="Variant files or folders to scan.",
    )
    args = parser.parse_args()

    claims = load_json_yaml(ROOT / "data" / "claims.yml")["claims"]
    blocklist = load_json_yaml(ROOT / "data" / "vocabulary_blocklist.yml")
    forbidden = [p.lower() for p in blocklist["forbidden_phrases"]]
    overclaim = [p.lower() for p in blocklist["overclaim_verbs_requiring_evidence"]]

    markers_by_variant: dict[str, list[str]] = {}
    all_markers: list[str] = []
    for claim in claims:
        markers = claim_markers(claim)
        all_markers.extend(markers)
        for variant in claim["allowed_variants"]:
            markers_by_variant.setdefault(variant, []).extend(markers)

    failures: list[str] = []
    warnings: list[str] = []

    for path in iter_variant_docs(args.paths):
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        variant = variant_id_for(path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()

        for phrase in forbidden:
            if phrase in lower:
                failures.append(f"{rel}: forbidden phrase: {phrase}")

        allowed_markers = markers_by_variant.get(variant or "", []) + all_markers
        for idx, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped.startswith((r"\item ", "- ", "* ")):
                continue
            normalized = re.sub(r"\s+", " ", stripped).lower()

            if METRIC_RE.search(stripped) and not any(marker in normalized for marker in allowed_markers):
                warnings.append(f"{rel}:{idx}: metric should be tied to a claim id: {stripped}")

            if any(re.search(rf"\b{re.escape(verb)}\b", normalized) for verb in overclaim):
                if not any(marker in normalized for marker in allowed_markers):
                    warnings.append(f"{rel}:{idx}: overclaim verb needs evidence mapping: {stripped}")

    for item in warnings:
        print(f"WARN: {item}")
    for item in failures:
        print(f"FAIL: {item}")

    if failures:
        print(f"\nResult: FAIL ({len(failures)} failures, {len(warnings)} warnings)")
        return 1
    print(f"Result: PASS ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
