# Resume & CV — Foad S. Farimani, PhD

Variant-based resume and CV system in LaTeX and AsciiDoc. The repository now combines hand-edited role variants with an evidence ledger and quality gates that keep claims precise, public-safe, and free of generic AI wording.

## Variants

| Folder | Target Roles | Emphasis |
|--------|-------------|----------|
| `v1-systems-rd/` | System Architect, R&D Manager, Engineering Lead | PhD research, ASML/NTS systems work, grants, surgical robotics |
| `v2-software/` | .NET/C# Developer, Software Architect | C#, Python, open-source portfolio, Stack Overflow |
| `v3-program-mgr/` | Program Manager, Project Manager | Cross-functional leadership, grant acquisition, delivery |
| `v4-mechanical-lead/` | Lead Mechanical Engineer, Precision Mechanics Lead, Tooling Lead | VDL Cable Slab, YieldStar mechanics, NXE3800 heat shields, E-pin fatigue |
| `v5-mechatronics-systems/` | Mechatronics System Engineer, Test/Validation Engineer, HIL/Test Architect | QTools, Safety PLC Emulator, SCFS, pneumatic robotics |

## Structure

```
data/              ← Claim ledger, variant map, vocabulary gates
tools/             ← Validation scripts for slop and evidence hygiene
template/          ← Master templates with [V1]/[V2]/[V3] comment blocks
v1-systems-rd/     ← Ready-to-compile Systems/R&D Lead variant
v2-software/       ← Ready-to-compile Software Engineer variant
v3-program-mgr/    ← Ready-to-compile Program Manager variant
v4-mechanical-lead/← Ready-to-compile Lead Mechanical Engineer variant
v5-mechatronics-systems/ ← Ready-to-compile Mechatronics/System Integration variant
```

Each folder contains:
- `resume.tex` / `resume.adoc` — One-page resume
- `cv.tex` / `cv.adoc` — Full curriculum vitae
- `build.cmd` — Windows batch script to build styled PDFs

## Building

Each variant build creates both styled AsciiDoc PDFs and LaTeX PDFs. The AsciiDoc themes embed Latin Modern Roman fonts from `theme/fonts/`, matching the default LaTeX look while keeping the resume/CV color system.

```cmd
cd v1-systems-rd
build.cmd
```

Outputs per variant:
- `resume.pdf` / `cv.pdf` from AsciiDoc
- `resume-tex.pdf` / `cv-tex.pdf` from LaTeX

Validate wording and build all maintained variants:

```cmd
build_all.cmd
```

Run quality gates without building PDFs:

```cmd
python tools\detect_cv_slop.py v4-mechanical-lead v5-mechatronics-systems
python tools\validate_claims.py v4-mechanical-lead v5-mechatronics-systems
```

Recommended Windows setup with Scoop:

```powershell
scoop install miktex poppler
gem install asciidoctor-pdf
```

Alternative package managers:

```powershell
winget install MiKTeX.MiKTeX
winget install oschwartz10612.Poppler
choco install miktex.install poppler -y
```

## Evidence and Quality Model

`data/claims.yml` maps strong claims to evidence sources, confidence levels, and allowed variants. `data/vocabulary_blocklist.yml` blocks inflated phrases such as "groundbreaking" or "synergy". Add new claims before adding new high-impact bullets, especially metrics, ownership verbs, or customer/program claims.

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
