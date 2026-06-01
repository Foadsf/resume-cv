@echo off
setlocal
REM Build both styled AsciiDoc PDFs and LaTeX PDFs.
REM Outputs: resume-onepage.pdf/cv-full.pdf from AsciiDoc, resume-onepage-tex.pdf/cv-full-tex.pdf from LaTeX.

set "MIKTEX_BIN=%USERPROFILE%\scoop\apps\miktex\current\texmfs\install\miktex\bin\x64"
if exist "%MIKTEX_BIN%\pdflatex.exe" set "PATH=%MIKTEX_BIN%;%PATH%"
set "PDFLATEX=pdflatex"
if exist "%MIKTEX_BIN%\pdflatex.exe" set "PDFLATEX=%MIKTEX_BIN%\pdflatex.exe"

"%PDFLATEX%" --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: pdflatex was not found on PATH. Install MiKTeX/TeX Live, or run: scoop install miktex
  exit /b 1
)

ruby -S asciidoctor-pdf --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: asciidoctor-pdf was not found on PATH.
  exit /b 1
)
echo Building resume-onepage.pdf from AsciiDoc ...
ruby -S asciidoctor-pdf -o resume-onepage.tmp.pdf -a pdf-theme=%~dp0..\theme\resume-theme.yml resume-onepage.adoc
if errorlevel 1 exit /b 1
move /Y resume-onepage.tmp.pdf resume-onepage.pdf >nul
if errorlevel 1 exit /b 1
echo Building cv-full.pdf from AsciiDoc ...
ruby -S asciidoctor-pdf -o cv-full.tmp.pdf -a pdf-theme=%~dp0..\theme\cv-theme.yml cv-full.adoc
if errorlevel 1 exit /b 1
move /Y cv-full.tmp.pdf cv-full.pdf >nul
if errorlevel 1 exit /b 1

call :build_tex resume-onepage-tex resume-onepage.tex resume-onepage-tex.pdf
if errorlevel 1 exit /b 1
call :build_tex cv-full-tex cv-full.tex cv-full-tex.pdf
if errorlevel 1 exit /b 1

echo Done. Cleaning auxiliary files ...
del /q *.aux *.log *.out *.fls *.fdb_latexmk *.toc *.build.log 2>nul

echo.
dir /b *.pdf 2>nul
exit /b 0

:build_tex
set "JOB=%~1"
set "SRC=%~2"
set "OUT=%~3"
set "BUILD_LOG=%JOB%.build.log"
echo Building %OUT% from LaTeX ...
del /q "%OUT%" "%BUILD_LOG%" 2>nul
"%PDFLATEX%" -interaction=nonstopmode -halt-on-error -jobname=%JOB% "%SRC%" > "%BUILD_LOG%" 2>&1
if errorlevel 1 (
  echo ERROR: LaTeX failed while building %OUT%.
  type "%BUILD_LOG%"
  exit /b 1
)
"%PDFLATEX%" -interaction=nonstopmode -halt-on-error -jobname=%JOB% "%SRC%" >> "%BUILD_LOG%" 2>&1
if errorlevel 1 (
  echo ERROR: LaTeX failed while building %OUT%.
  type "%BUILD_LOG%"
  exit /b 1
)
if not exist "%OUT%" (
  echo ERROR: LaTeX did not create %OUT%.
  type "%BUILD_LOG%"
  exit /b 1
)
exit /b 0
