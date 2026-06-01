@echo off
setlocal

REM Validate wording and evidence hygiene before building PDFs.
python tools\detect_cv_slop.py v1-systems-rd v2-software v3-program-mgr v4-mechanical-lead v5-mechatronics-systems
if errorlevel 1 exit /b 1

python tools\validate_claims.py v1-systems-rd v2-software v3-program-mgr v4-mechanical-lead v5-mechatronics-systems
if errorlevel 1 exit /b 1

for %%D in (v1-systems-rd v2-software v3-program-mgr v4-mechanical-lead v5-mechatronics-systems) do (
  if exist "%%D\build.cmd" (
    echo.
    echo Building %%D ...
    pushd "%%D"
    call build.cmd
    if errorlevel 1 (
      popd
      exit /b 1
    )
    popd
  )
)

echo.
echo All variants built.
