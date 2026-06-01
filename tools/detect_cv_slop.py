#!/usr/bin/env python3
"""Detect vague or inflated resume/CV wording.

The gate is intentionally conservative: it fails on known-bad phrases and
warns on weak bullet patterns that should be reviewed by a human.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".tex", ".adoc", ".md"}


def load_json_yaml(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
        elif path.is_dir():
            files.extend(
                p
                for p in path.rglob("*")
                if p.is_file()
                and p.suffix.lower() in TEXT_EXTENSIONS
                and ".git" not in p.parts
            )
    return sorted(set(files))


def bullet_text(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith(r"\item "):
        return stripped[6:].strip()
    if stripped.startswith("- "):
        return stripped[2:].strip()
    if stripped.startswith("* "):
        return stripped[2:].strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[ROOT / "v1-systems-rd", ROOT / "v2-software", ROOT / "v3-program-mgr"],
        help="Files or directories to scan.",
    )
    args = parser.parse_args()

    blocklist = load_json_yaml(ROOT / "data" / "vocabulary_blocklist.yml")
    forbidden = [p.lower() for p in blocklist["forbidden_phrases"]]
    weak_verbs = [p.lower() for p in blocklist["weak_verbs"]]

    failures: list[str] = []
    warnings: list[str] = []

    for path in iter_text_files(args.paths):
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()

        for phrase in forbidden:
            if phrase in lower:
                failures.append(f"{rel}: forbidden phrase: {phrase}")

        for idx, line in enumerate(text.splitlines(), start=1):
            bullet = bullet_text(line)
            if not bullet:
                continue
            normalized = re.sub(r"\s+", " ", bullet).lower()
            if normalized.startswith("patent:"):
                continue
            if len(normalized.split()) < 7:
                warnings.append(f"{rel}:{idx}: very short bullet: {bullet}")
            if any(normalized.startswith(verb) for verb in weak_verbs):
                warnings.append(f"{rel}:{idx}: weak opening verb: {bullet}")
            has_project_or_object = bool(
                re.search(
                    r"\b(EXE|EXE5000|NXE|NXT|YieldStar|QTool|qualification tooling|qualification-tooling|wafer stage|wafer-stage|E-pin|SCFS|Cable Slab|PneuAct|PneuARMM|PanoSurg|MURAB|RFI|Research Funding Initiative|Surface Treatment|Safety PLC|MBSE|FEM/CAE|CAD|PDR|CDR|PIR|TPD|PMI|MRI compatible|MRI-compatible|pneumatic|bellows|force decoupler|force-decoupler)\b",
                    bullet,
                    re.IGNORECASE,
                )
            )
            has_method_or_outcome = bool(
                re.search(
                    r"\b(using|via|through|validated|improved|coordinating|including|connecting|bridged|mapped|introduced|identified|standardized|interpreted|authored|worked across|contributed|screened|translated|resolved)\b",
                    normalized,
                )
            )
            if len(normalized.split()) > 12 and not (has_project_or_object or has_method_or_outcome):
                warnings.append(f"{rel}:{idx}: generic-looking bullet: {bullet}")

    # Check for missing compound-adjective hyphens in running text
    UNHYPHENATED = re.compile(
        r"(?<!\")(?<!``)\b(MRI|CAD|review|tolerance) (compatible|facing|ready|sensitive)\b",
        re.IGNORECASE,
    )
    for path in iter_text_files(args.paths):
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        for idx, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1
        ):
            # Skip publication/patent title lines
            if any(t in line for t in ['``', '"', "Introducing PneuAct", "Mechanism Design", "Dynamic Modeling", "Primary Design"]):
                continue
            m = UNHYPHENATED.search(line)
            if m:
                warnings.append(f"{rel}:{idx}: missing hyphen in compound adjective: {m.group()}")

    # Check that every resume file has an Education section
    for path in iter_text_files(args.paths):
        if "resume" not in path.name:
            continue
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "education" not in text:
            failures.append(f"{rel}: resume is missing Education section")

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
