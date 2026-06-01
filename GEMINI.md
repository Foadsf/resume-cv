# Project Overview

This repository is a "code-based" document generation project containing the source code for a variant-based resume and Curriculum Vitae (CV) system for Foad S. Farimani, PhD. The project leverages **LaTeX** and **AsciiDoc** to produce PDFs tailored for three distinct professional role families:
1. **v1-systems-rd:** Systems Architect, R&D Manager, and Engineering Lead.
2. **v2-software:** .NET/C# Developer and Software Architect.
3. **v3-program-mgr:** Program Manager and Project Manager.

## Building and Running

### LaTeX (PDF Generation)
The project utilizes `pdflatex` to compile the resumes and CVs. A Windows batch script (`build.cmd`) is provided in each variant subdirectory to automate the build and clean-up processes.

**Prerequisites:** [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/) must be installed, and `pdflatex` must be accessible on your system's PATH.

**Commands:**
Navigate to the desired variant directory and execute the build script:
```cmd
cd v1-systems-rd
build.cmd
```
*Note: The script runs `pdflatex` twice to ensure all document cross-references are resolved properly, and automatically cleans up auxiliary build files (like `.aux`, `.log`, `.out`, etc.).*

### AsciiDoc
To build the AsciiDoc versions of the documents into PDFs, the `asciidoctor-pdf` Ruby gem is required.

**Commands:**
Navigate to the targeted directory and run:
```cmd
asciidoctor-pdf resume.adoc
asciidoctor-pdf cv.adoc
```

## Development Conventions

- **Master Templates:** The `/template` directory contains the master source files (`resume-onepage.tex/adoc` and `cv-full.tex/adoc`). These master files use `[V1]`, `[V2]`, and `[V3]` comment blocks to outline the content differences between the roles.
- **Variant Instantiation:** The three variant folders (`v1-systems-rd/`, `v2-software/`, `v3-program-mgr/`) act as ready-to-compile instances. When modifying core content, updates should ideally originate in the `template/` files and then be manually propagated or adapted to the respective `vX-*` target folders to maintain consistency across the variants.
- **Clean Builds:** Always ensure that `build.cmd` or equivalent logic is used to delete temporary auxiliary files so that the repository remains clean and unpolluted with intermediate compilation artifacts.