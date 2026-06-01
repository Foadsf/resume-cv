# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A variant-based resume/CV document system producing role-targeted PDFs from LaTeX and AsciiDoc sources. Each `vN-*` folder is a self-contained, buildable variant tailored to a specific job family. `template/` holds the master sources with `[V1]`/`[V2]`/`[V3]` comment blocks marking variant-specific sections.

## Build Commands

Build a single variant (default: AsciiDoc with themed PDF output):
```cmd
cd v1-systems-rd && build.cmd
```

Build from LaTeX instead:
```cmd
set BUILD_ENGINE=latex
cd v1-systems-rd && build.cmd
```

Validate wording + build all variants:
```cmd
build_all.cmd
```

Run quality gates without building:
```cmd
python tools\detect_cv_slop.py v1-systems-rd v2-software v3-program-mgr v4-mechanical-lead v5-mechatronics-systems
python tools\validate_claims.py v4-mechanical-lead v5-mechatronics-systems
```

Verify PDF output:
```cmd
pdfinfo v1-systems-rd\resume.pdf
pdftotext v1-systems-rd\resume.pdf -
```

Prerequisites: `asciidoctor-pdf` (Ruby gem), `miktex`/`pdflatex` (for LaTeX mode), `poppler` (for PDF inspection).

## Architecture

**Data layer** (`data/`): JSON files treated as YAML by the Python tools.
- `claims.yml` — evidence ledger mapping claims to confidence levels, allowed variants, and source documents. Every metric or strong verb in a bullet must trace to a claim here.
- `variants.yml` — variant registry with target roles and lead evidence per variant. Includes planned variants (v6–v8) not yet implemented.
- `vocabulary_blocklist.yml` — forbidden phrases, weak opening verbs, and overclaim verbs requiring evidence.
- `vocabulary_allowlist.yml` — approved technical terms (semiconductor equipment domain).

**Quality gates** (`tools/`): Two Python validators that `build_all.cmd` runs before building.
- `detect_cv_slop.py` — fails on forbidden phrases, warns on short/weak/generic bullets, detects missing compound-adjective hyphens (e.g. "MRI compatible" → "MRI-compatible"), and fails if any resume is missing an Education section. Scans `.tex`, `.adoc`, `.md` files.
- `validate_claims.py` — fails on forbidden phrases, warns on unlinked metrics and overclaim verbs missing evidence mappings. Uses claim markers (n-gram matching) to verify bullets tie back to `claims.yml`.

**Theme** (`theme/`): `resume-theme.yml` and `cv-theme.yml` are asciidoctor-pdf theme files. Resume uses tighter margins (0.31in) and smaller font (7.85pt) for one-page density. CV uses standard margins and 9.1pt. Both embed Latin Modern Roman from `theme/fonts/`.

**Build system**: Each variant's `build.cmd` detects `BUILD_ENGINE` env var. Default path runs `asciidoctor-pdf` with the appropriate theme. LaTeX path runs `pdflatex` twice and cleans aux files. `build_all.cmd` runs both validators first, then iterates all variant folders.

## Content Rules

- **Claims-first workflow**: add/update a claim in `data/claims.yml` before writing a bullet with a metric, ownership verb, or customer/program reference. Run both validators after editing.
- **Bullet pattern**: `[Action] [specific object] using [method] to achieve [outcome]`. See `docs/writing-style-guide.md`.
- **Evidence levels**: `verified` (safe for resume), `probable` (conservative wording), `needs-confirmation` (keep out of public resumes), `private/internal` (never publish).
- **Vocabulary**: never use forbidden phrases from `vocabulary_blocklist.yml`. Don't open bullets with weak verbs (`helped`, `worked on`, `involved in`, `participated in`, `responsible for`).
- **One-page resumes must stay one page.** Current role: max 4 bullets. Previous: max 3. CVs may be longer but favor case studies over exhaustive lists.
- **Variant naming**: `vN-short-target` (e.g., `v4-mechanical-lead`). File names inside variants are always `resume.*` and `cv.*`.
- **Compound adjectives**: hyphenate before nouns — `MRI-compatible`, `review-ready`, `tolerance-sensitive`, `CAD-facing`. The slop detector enforces this.
- **Publication/patent titles**: never alter. Copy exactly as published. If IEEE uses "MRI-Compatible", keep it.
- **.tex/.adoc sync**: every variant has both sources; they must match in content. The `.adoc` is the default build path and source of truth.
- **No AI meta-language**: never write phrases like "evidence spans", "adoption claims", "contribution scope should remain" — these are internal authoring notes, not resume content. The forbidden-phrases list blocks common offenders.
- **Every resume must include "Dutch citizen"** in the contact line and an **Education section**. The slop detector enforces Education.

## Commit Style

Conventional Commits: `feat:`, `fix:`, `docs:`. PR summaries should name affected variants, build commands run, and whether PDFs changed.

## Sensitive Content

Resume/CV content is personal data. Do not add private contact details, unreleased employer information, or confidential program codes unless explicitly approved for publication. Do not disclose evidence source paths (which point to local portfolio files) in any public output.
