#Requires -Version 5.1
# PowerShell 5.1 compatible: ASCII-only script, no UTF-8 BOM dependency.
$ErrorActionPreference = "Stop"
$projectPath = $PSScriptRoot
$sourceUrl = "https://raw.githubusercontent.com/GilbertMoon/policy_rag_assistant/044f9d930c7c5b01bec07c2581a61b08b2bd136f/starter-kit-20261022T062047Z-1-001.zip"
$zipName = "starter-kit-20261022T062047Z-1-001.zip"
$expectedSize = 318392
$expectedGitBlobSha = "1ad7b50a3f261c649595249cca7836a954d32c4d"
$downloads = Join-Path $projectPath ".downloads"
$zipPath = Join-Path $downloads $zipName
$extractPath = Join-Path $projectPath "starter-kit"

Write-Host "=== Solar RAG lecture: Steps 1-5 ===" -ForegroundColor Cyan
Write-Host "Setup folder: $projectPath"

# Step 1: Download the instructor's ZIP from a fixed GitHub commit.
New-Item -ItemType Directory -Force -Path $downloads | Out-Null
if (-not (Test-Path -LiteralPath $zipPath)) {
    Write-Host "[1] Downloading the instructor ZIP..."
    Invoke-WebRequest -Uri $sourceUrl -OutFile $zipPath -UseBasicParsing
} else {
    Write-Host "[1] Existing ZIP found. Checking integrity..."
}

# Step 2: Confirm downloaded bytes match the original GitHub blob.
$actualSize = (Get-Item -LiteralPath $zipPath).Length
if ($actualSize -ne $expectedSize) {
    throw "ZIP size mismatch: expected $expectedSize, got $actualSize. File: $zipPath"
}
$actualSha = (& git hash-object -- $zipPath).Trim()
if ($LASTEXITCODE -ne 0 -or $actualSha -ne $expectedGitBlobSha) {
    throw "ZIP SHA mismatch: expected $expectedGitBlobSha, got $actualSha."
}
Write-Host "[2] ZIP integrity verified." -ForegroundColor Green

# Step 3: Extract once; never overwrite a prior extraction.
if (-not (Test-Path -LiteralPath $extractPath)) {
    Write-Host "[3] Extracting..."
    Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath
} else {
    Write-Host "[3] Existing starter-kit folder preserved."
}

# Locate the actual project root, including optional nested folders.
$matches = @(Get-ChildItem -LiteralPath $extractPath -Recurse -File -Filter "fetch_ordinances.py")
if ($matches.Count -ne 1) {
    throw "Expected exactly one fetch_ordinances.py; found $($matches.Count). Check: $extractPath"
}
$kitRoot = $matches[0].Directory.FullName
$requiredFiles = @(
    "requirements.txt", "config.py", "fetch_ordinances.py", "parse_annex.py",
    "build_index.py", "rag.py", "app.py", "check.py", "demo.py",
    "sample_questions.json", "upstage.py"
)
$missing = @($requiredFiles | Where-Object {
    -not (Test-Path -LiteralPath (Join-Path $kitRoot $_))
})
if ($missing.Count -gt 0) {
    throw "Starter Kit files missing: $($missing -join ', '). Folder: $kitRoot"
}
Write-Host "Official Starter Kit root: $kitRoot" -ForegroundColor Green

# Step 4: Create a private virtual environment in the real Starter Kit.
Push-Location -LiteralPath $kitRoot
try {
    Write-Host "[4] Checking Python and .venv..."
    python --version
    if ($LASTEXITCODE -ne 0) {
        throw "Python was not found. Check python --version."
    }
    $venvPython = Join-Path $kitRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $venvPython)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Python virtual environment creation failed."
        }
    }
    if (-not (Test-Path -LiteralPath $venvPython)) {
        throw "Virtual environment Python missing: $venvPython"
    }

    # Step 5: Use the instructor's requirements, NOT the provisional file.
    Write-Host "[5] Installing instructor requirements..."
    & $venvPython -m pip install -r (Join-Path $kitRoot "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        throw "pip install failed; review the errors above."
    }

    Write-Host ""
    Write-Host "SUCCESS: Lecture steps 1-5 installed." -ForegroundColor Green
    Write-Host "Open this Starter Kit folder in VS Code: $kitRoot"
    Write-Host "Store real API keys in a private .env file, never in GitHub."
} finally {
    Pop-Location
}
