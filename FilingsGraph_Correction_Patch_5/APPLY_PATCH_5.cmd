@echo off
setlocal EnableExtensions

set "PATCH_DIR=%~dp0"
for %%I in ("%PATCH_DIR%..") do set "PARENT_DIR=%%~fI"

if exist "%CD%\src\filingsgraph" (
  set "ROOT=%CD%"
) else if exist "%PARENT_DIR%\src\filingsgraph" (
  set "ROOT=%PARENT_DIR%"
) else (
  echo ERROR: Run this from the FilingsGraph project root, or keep the Patch 5 folder directly under the project root.
  exit /b 1
)

pushd "%ROOT%"

echo [1/7] Verifying the frozen 17-file core before Patch 5...
python -m scripts.check_v6_freeze
if errorlevel 1 (popd & exit /b 1)

echo [2/7] Backing up pre-Patch-5 specialized files...
set "BACKUP=%ROOT%\reports\baseline\patch4_specialized_diagnostic\pre_patch5_code"
if not exist "%BACKUP%" mkdir "%BACKUP%"
if exist "src\filingsgraph\risk_topics.py" copy /Y "src\filingsgraph\risk_topics.py" "%BACKUP%\risk_topics.py" >nul
if exist "src\filingsgraph\graph\extraction.py" copy /Y "src\filingsgraph\graph\extraction.py" "%BACKUP%\graph_extraction.py" >nul
if exist "src\filingsgraph\temporal\risk_diff.py" copy /Y "src\filingsgraph\temporal\risk_diff.py" "%BACKUP%\temporal_risk_diff.py" >nul
if exist "src\filingsgraph\llm\grounding.py" copy /Y "src\filingsgraph\llm\grounding.py" "%BACKUP%\llm_grounding.py" >nul
if exist "src\filingsgraph\agents\nodes.py" copy /Y "src\filingsgraph\agents\nodes.py" "%BACKUP%\agent_nodes.py" >nul
if exist "scripts\build_graph.py" copy /Y "scripts\build_graph.py" "%BACKUP%\build_graph.py" >nul
if exist "scripts\evaluate_grounding.py" copy /Y "scripts\evaluate_grounding.py" "%BACKUP%\evaluate_grounding.py" >nul

echo [3/7] Applying Patch 5 specialized-layer files...
xcopy "%PATCH_DIR%patch_files\*" "%ROOT%\" /E /I /Y >nul
if errorlevel 1 (popd & exit /b 1)

echo [4/7] Compiling Python files...
python -m compileall -q src scripts app tests
if errorlevel 1 (popd & exit /b 1)

echo [5/7] Running complete tests...
pytest -q
if errorlevel 1 (popd & exit /b 1)

echo [6/7] Running grounding verifier self-test...
python -m scripts.evaluate_grounding
if errorlevel 1 (popd & exit /b 1)

echo [7/7] Confirming frozen core is unchanged...
python -m scripts.check_v6_freeze
if errorlevel 1 (popd & exit /b 1)

popd
echo.
echo PATCH 5 APPLIED SUCCESSFULLY.
echo Frozen retrieval/XBRL/router/chunking files were not changed.
echo Next: rebuild only the graph, regenerate temporal predictions, run Patch-5 diagnostic, then run live grounding.
endlocal
