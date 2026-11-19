param([switch]$Offline, [string]$PythonVersion = '3.12')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & py "-$PythonVersion" -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Install Python $PythonVersion (64-bit) first, then rerun." }
}
$pythonExe = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if ($Offline) {
    $tag = $PythonVersion.Replace('.', '')
    $wheels = Join-Path (Get-Location) "offline_wheels\py$tag"
    & $pythonExe -m pip install --no-index --find-links $wheels -r requirements-lock.txt
} else {
    & $pythonExe -m pip install -r requirements-lock.txt
}
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
& $pythonExe -m pytest -q --junitxml results\local-tests.xml
if ($LASTEXITCODE -ne 0) { throw 'Tests failed; do not claim verified results.' }
& $pythonExe -m evaluation.run --verify
if ($LASTEXITCODE -ne 0) { throw 'Reproduction mismatch; inspect the reported path.' }
Write-Host 'All checks passed. Start the demo with:'
Write-Host '.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000'
Write-Host 'Then open http://127.0.0.1:8000/app/ or /docs'
