@echo off
REM Build PDFs from .tex files
REM Requires: MiKTeX or TeX Live with pdflatex on PATH

echo Building resume.pdf ...
pdflatex -interaction=nonstopmode resume.tex >nul 2>&1
pdflatex -interaction=nonstopmode resume.tex >nul 2>&1

echo Building cv.pdf ...
pdflatex -interaction=nonstopmode cv.tex >nul 2>&1
pdflatex -interaction=nonstopmode cv.tex >nul 2>&1

echo Done. Cleaning auxiliary files ...
del /q *.aux *.log *.out *.fls *.fdb_latexmk 2>nul

echo.
dir /b *.pdf 2>nul
