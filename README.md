# Resume & CV — Foad S. Farimani, PhD

Variant-based resume and CV system in LaTeX and AsciiDoc, targeting three role families.

## Variants

| Folder | Target Roles | Emphasis |
|--------|-------------|----------|
| `v1-systems-rd/` | System Architect, R&D Manager, Engineering Lead | PhD research, ASML/NTS systems work, grants, surgical robotics |
| `v2-software/` | .NET/C# Developer, Software Architect | C#, Python, open-source portfolio, Stack Overflow |
| `v3-program-mgr/` | Program Manager, Project Manager | Cross-functional leadership, grant acquisition, delivery |

## Structure

```
template/          ← Master templates with [V1]/[V2]/[V3] comment blocks
v1-systems-rd/     ← Ready-to-compile Systems/R&D Lead variant
v2-software/       ← Ready-to-compile Software Engineer variant
v3-program-mgr/    ← Ready-to-compile Program Manager variant
```

Each folder contains:
- `resume.tex` / `resume.adoc` — One-page resume
- `cv.tex` / `cv.adoc` — Full curriculum vitae
- `build.cmd` — Windows batch script to compile LaTeX → PDF

## Building

**Prerequisites:** [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/) with `pdflatex` on PATH.

```cmd
cd v1-systems-rd
build.cmd
```

For AsciiDoc → PDF, install [Asciidoctor PDF](https://docs.asciidoctor.org/pdf-converter/latest/):
```cmd
asciidoctor-pdf resume.adoc
asciidoctor-pdf cv.adoc
```

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
