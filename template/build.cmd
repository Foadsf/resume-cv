@echo off
REM Build PDFs from template .tex files
REM Requires: MiKTeX or TeX Live with pdflatex on PATH

echo Building resume-onepage.pdf ...
pdflatex -interaction=nonstopmode resume-onepage.tex >nul 2>&1
pdflatex -interaction=nonstopmode resume-onepage.tex >nul 2>&1

echo Building cv-full.pdf ...
pdflatex -interaction=nonstopmode cv-full.tex >nul 2>&1
pdflatex -interaction=nonstopmode cv-full.tex >nul 2>&1

echo Done. Cleaning auxiliary files ...
del /q *.aux *.log *.out *.fls *.fdb_latexmk 2>nul

echo.
dir /b *.pdf 2>nul
