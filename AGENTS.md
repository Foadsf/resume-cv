# Repository Guidelines

## Project Structure & Module Organization

This repository is a variant-based resume/CV document system, not an application codebase. The root contains shared documentation, licensing, evidence data, and validation tools. `template/` holds the original master LaTeX and AsciiDoc sources: `resume-onepage.*` and `cv-full.*`. `data/` contains claim and vocabulary gates. `tools/` contains lightweight Python validators. The variant folders are ready-to-build outputs for specific role families:

- `v1-systems-rd/` for systems, R&D, and engineering leadership roles.
- `v2-software/` for .NET/C# developer and software architect roles.
- `v3-program-mgr/` for program and project management roles.
- `v4-mechanical-lead/` for lead mechanical and precision tooling roles.
- `v5-mechatronics-systems/` for mechatronics, integration, and validation roles.

Each variant contains `resume.tex`, `cv.tex`, matching `.adoc` files, and `build.cmd`.

## Build, Test, and Development Commands

Build LaTeX PDFs from a variant directory:

```cmd
cd v1-systems-rd
build.cmd
```

`build.cmd` runs `pdflatex` twice for each `.tex` file and removes auxiliary files. Build AsciiDoc PDFs manually when needed:

```cmd
asciidoctor-pdf resume.adoc
asciidoctor-pdf cv.adoc
```

Prerequisites are MiKTeX or TeX Live with `pdflatex` on `PATH`; AsciiDoc PDF output requires `asciidoctor-pdf`.
Run `build_all.cmd` from the root to validate wording and build all maintained variants. Run validators directly with `python tools\detect_cv_slop.py <variant>` and `python tools\validate_claims.py <variant>`.

## Coding Style & Naming Conventions

Keep file names stable: template files use descriptive names, while variant files use `resume.*` and `cv.*`. Preserve variant naming as `vN-short-target`, for example `v4-mechanical-lead`. In LaTeX, keep commands and section formatting consistent with nearby content. In AsciiDoc, prefer concise headings and simple lists. Do not commit transient LaTeX build artifacts such as `.aux`, `.log`, `.out`, or `.toc`.

## Validation Guidelines

There is no unit test suite, but there are content gates. Validate changes with `detect_cv_slop.py`, `validate_claims.py`, and by building every affected variant. Review generated PDFs for layout regressions, overfull lines, broken links, and page count changes. When adding high-impact bullets, update `data/claims.yml` first.

## Commit & Pull Request Guidelines

The repository uses concise Conventional Commit-style messages, for example `feat: variant-based resume/CV system`. Use `feat:`, `fix:`, or `docs:` as appropriate. Pull requests should summarize the target variant(s), list build commands run, and note whether generated PDFs changed.

## Security & Configuration Tips

Resume and CV content is personal data. Avoid adding private contact details, unreleased employer information, or local machine paths unless they are explicitly intended for publication.
