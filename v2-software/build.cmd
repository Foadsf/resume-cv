@echo off
setlocal
REM Build both styled AsciiDoc PDFs and LaTeX PDFs.
REM Outputs: resume.pdf/cv.pdf from AsciiDoc, resume-tex.pdf/cv-tex.pdf from LaTeX.

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
echo Building resume.pdf from AsciiDoc ...
ruby -S asciidoctor-pdf -o resume.tmp.pdf -a pdf-theme=%~dp0..\theme\resume-theme.yml resume.adoc
if errorlevel 1 exit /b 1
move /Y resume.tmp.pdf resume.pdf >nul
if errorlevel 1 exit /b 1
echo Building cv.pdf from AsciiDoc ...
ruby -S asciidoctor-pdf -o cv.tmp.pdf -a pdf-theme=%~dp0..\theme\cv-theme.yml cv.adoc
if errorlevel 1 exit /b 1
move /Y cv.tmp.pdf cv.pdf >nul
if errorlevel 1 exit /b 1

call :build_tex resume-tex resume.tex resume-tex.pdf
if errorlevel 1 exit /b 1
call :build_tex cv-tex cv.tex cv-tex.pdf
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
