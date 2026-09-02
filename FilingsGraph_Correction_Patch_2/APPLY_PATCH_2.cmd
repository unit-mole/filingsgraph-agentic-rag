@echo off
setlocal EnableExtensions
set "PATCH_DIR=%~dp0"

rem Support either extraction directly into filingsgraph or into a Patch_2 subfolder.
if exist "%PATCH_DIR%src\filingsgraph" (
  set "ROOT=%PATCH_DIR%"
) else (
  for %%I in ("%PATCH_DIR%..") do set "ROOT=%%~fI\"
)

if not exist "%ROOT%src\filingsgraph" (
  echo ERROR: Could not locate the filingsgraph project root.
  echo Extract this patch inside the filingsgraph folder, then run APPLY_PATCH_2.cmd.
  exit /b 1
)

set "BACKUP=%ROOT%reports\baseline\initial_full_run\pre_patch2"

echo [1/4] Backing up pre-Patch-2 files...
if not exist "%BACKUP%" mkdir "%BACKUP%"
if not exist "%BACKUP%\src\filingsgraph\agents" mkdir "%BACKUP%\src\filingsgraph\agents"
if not exist "%BACKUP%\src\filingsgraph\retrieval" mkdir "%BACKUP%\src\filingsgraph\retrieval"
if not exist "%BACKUP%\src\filingsgraph\evaluation" mkdir "%BACKUP%\src\filingsgraph\evaluation"
if not exist "%BACKUP%\scripts" mkdir "%BACKUP%\scripts"
copy /Y "%ROOT%src\filingsgraph\agents\router.py" "%BACKUP%\src\filingsgraph\agents\router.py" >nul
copy /Y "%ROOT%src\filingsgraph\agents\planner.py" "%BACKUP%\src\filingsgraph\agents\planner.py" >nul
copy /Y "%ROOT%src\filingsgraph\agents\nodes.py" "%BACKUP%\src\filingsgraph\agents\nodes.py" >nul
copy /Y "%ROOT%src\filingsgraph\retrieval\filters.py" "%BACKUP%\src\filingsgraph\retrieval\filters.py" >nul
copy /Y "%ROOT%src\filingsgraph\retrieval\dense.py" "%BACKUP%\src\filingsgraph\retrieval\dense.py" >nul
copy /Y "%ROOT%src\filingsgraph\evaluation\runner.py" "%BACKUP%\src\filingsgraph\evaluation\runner.py" >nul
copy /Y "%ROOT%scripts\evaluate_retrieval.py" "%BACKUP%\scripts\evaluate_retrieval.py" >nul
copy /Y "%ROOT%scripts\tune_reranker.py" "%BACKUP%\scripts\tune_reranker.py" >nul

echo [2/4] Applying Patch 2 files...
xcopy "%PATCH_DIR%patch_files\*" "%ROOT%" /E /I /Y /Q >nul
if errorlevel 1 (
  echo ERROR: Patch file copy failed.
  exit /b 1
)

pushd "%ROOT%"
echo [3/4] Compiling Python files...
python -m compileall -q src scripts tests
if errorlevel 1 (
  popd
  echo ERROR: Python compilation failed.
  exit /b 1
)

echo [4/4] Running complete tests...
pytest -q
if errorlevel 1 (
  popd
  echo ERROR: Tests failed. Restore from %BACKUP% if needed.
  exit /b 1
)
popd

echo.
echo PATCH 2 APPLIED SUCCESSFULLY.
echo Next: re-run DEV router, DEV retrieval, and reranker tuning. No SEC redownload or re-index is required.
endlocal
