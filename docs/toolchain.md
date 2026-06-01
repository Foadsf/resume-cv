# PDF Toolchain

The repository builds styled AsciiDoc PDFs and LaTeX PDFs side by side. The AsciiDoc theme embeds Latin Modern Roman from `theme/fonts/`, matching the default LaTeX look.

## Recommended Install

```powershell
scoop install miktex poppler
gem install asciidoctor-pdf
```

`miktex` provides LaTeX engines and Latin Modern fonts. `poppler` provides `pdfinfo`, `pdftotext`, and `pdffonts` for closed-loop checks.

## Alternatives

```powershell
winget install MiKTeX.MiKTeX
winget install oschwartz10612.Poppler
```

```powershell
choco install miktex.install poppler -y
```

## Build Outputs

Build every maintained variant:

```cmd
build_all.cmd
```

Each variant emits:

- `resume.pdf` and `cv.pdf` from AsciiDoc
- `resume-tex.pdf` and `cv-tex.pdf` from LaTeX

Template outputs use `resume-onepage.pdf`, `cv-full.pdf`, `resume-onepage-tex.pdf`, and `cv-full-tex.pdf`.

## Verification

```cmd
pdfinfo v1-systems-rd\resume.pdf
pdftotext v1-systems-rd\resume.pdf -
pdffonts v1-systems-rd\resume.pdf
```
