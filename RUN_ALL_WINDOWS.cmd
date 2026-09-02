@echo off
setlocal
cd /d %~dp0
if not exist .venv\Scripts\python.exe (
  echo ERROR: .venv does not exist. Run the setup commands in docs\WINDOWS_RUNBOOK.md first.
  exit /b 2
)
call .venv\Scripts\activate.bat
python -m scripts.check_environment || exit /b 1
python -m scripts.validate_sec_access || exit /b 1
python -m scripts.run_pipeline --stage all || exit /b 1
pytest -q || exit /b 1
python -m scripts.export_final_results || exit /b 1
echo.
echo FilingsGraph full pipeline completed. See reports\final\summary.json
endlocal
