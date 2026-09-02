@echo off
setlocal EnableExtensions

set "PATCH_DIR=%~dp0"
for %%I in ("%PATCH_DIR%..") do set "PARENT_DIR=%%~fI"

if exist "%CD%\src\filingsgraph" (
  set "ROOT=%CD%"
) else if exist "%PARENT_DIR%\src\filingsgraph" (
  set "ROOT=%PARENT_DIR%"
) else (
  echo ERROR: Run this from the FilingsGraph project root, or keep the patch folder directly under the project root.
  exit /b 1
)

echo [1/5] Backing up pre-Patch-3 files...
set "BACKUP=%ROOT%\reports\baseline\pre_patch3_code"
if not exist "%BACKUP%" mkdir "%BACKUP%"
if exist "%ROOT%\src\filingsgraph\llm\local_provider.py" copy /Y "%ROOT%\src\filingsgraph\llm\local_provider.py" "%BACKUP%\local_provider.py" >nul
if exist "%ROOT%\src\filingsgraph\llm\prompts.py" copy /Y "%ROOT%\src\filingsgraph\llm\prompts.py" "%BACKUP%\prompts.py" >nul
if exist "%ROOT%\src\filingsgraph\verification\citations.py" copy /Y "%ROOT%\src\filingsgraph\verification\citations.py" "%BACKUP%\citations.py" >nul
if exist "%ROOT%\app\runtime.py" copy /Y "%ROOT%\app\runtime.py" "%BACKUP%\runtime.py" >nul
if exist "%ROOT%\scripts\evaluate_grounding.py" copy /Y "%ROOT%\scripts\evaluate_grounding.py" "%BACKUP%\evaluate_grounding.py" >nul
if exist "%ROOT%\scripts\evaluate_temporal.py" copy /Y "%ROOT%\scripts\evaluate_temporal.py" "%BACKUP%\evaluate_temporal.py" >nul
if exist "%ROOT%\scripts\evaluate_graph.py" copy /Y "%ROOT%\scripts\evaluate_graph.py" "%BACKUP%\evaluate_graph.py" >nul

echo [2/5] Applying Patch 3 files...
xcopy "%PATCH_DIR%patch_files\*" "%ROOT%\" /E /I /Y >nul
if errorlevel 1 exit /b 1

echo [3/5] Compiling Python files...
pushd "%ROOT%"
python -m compileall -q src scripts app tests
if errorlevel 1 (popd & exit /b 1)

echo [4/5] Running complete tests...
pytest -q
if errorlevel 1 (popd & exit /b 1)

echo [5/5] Verifying Patch 3 self-test grounding...
python -m scripts.evaluate_grounding
if errorlevel 1 (popd & exit /b 1)
popd

echo.
echo PATCH 3 APPLIED SUCCESSFULLY.
echo Next: freeze V6, run live grounding, export human-review gold sheets, review them, then score Temporal/Graph gold.
endlocal
