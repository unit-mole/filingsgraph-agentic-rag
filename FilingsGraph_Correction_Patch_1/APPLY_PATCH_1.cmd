@echo off
setlocal
set "PATCH=%~dp0"
for %%I in ("%PATCH%..") do set "ROOT=%%~fI"

if not exist "%ROOT%\pyproject.toml" (
  echo ERROR: Patch folder must be extracted directly inside the filingsgraph project root.
  echo Expected: ^<filingsgraph^>\FilingsGraph_Correction_Patch_1\APPLY_PATCH_1.cmd
  exit /b 1
)

echo [1/4] Backing up pre-patch source and benchmark...
set "BACKUP=%ROOT%\reports\baseline\initial_full_run\pre_patch1"
if not exist "%BACKUP%" mkdir "%BACKUP%"
xcopy "%ROOT%\src" "%BACKUP%\src" /E /I /Y >nul
xcopy "%ROOT%\scripts" "%BACKUP%\scripts" /E /I /Y >nul
xcopy "%ROOT%\configs" "%BACKUP%\configs" /E /I /Y >nul
xcopy "%ROOT%\tests" "%BACKUP%\tests" /E /I /Y >nul
if exist "%ROOT%\data\evaluation" xcopy "%ROOT%\data\evaluation" "%BACKUP%\evaluation_v1" /E /I /Y >nul

echo [2/4] Applying Patch 1 files...
xcopy "%PATCH%patch_files\src" "%ROOT%\src" /E /I /Y >nul
xcopy "%PATCH%patch_files\scripts" "%ROOT%\scripts" /E /I /Y >nul
xcopy "%PATCH%patch_files\configs" "%ROOT%\configs" /E /I /Y >nul
xcopy "%PATCH%patch_files\tests" "%ROOT%\tests" /E /I /Y >nul

echo [3/4] Compiling Python files...
cd /d "%ROOT%"
python -m compileall -q src scripts tests
if errorlevel 1 exit /b 1

echo [4/4] Running focused Patch 1 tests...
pytest -q tests\unit\test_parsing.py tests\unit\test_agent.py tests\unit\test_xbrl.py
if errorlevel 1 exit /b 1

echo.
echo PATCH 1 APPLIED SUCCESSFULLY.
echo Next: run the commands in PATCH1_README.md from the filingsgraph root.
exit /b 0
