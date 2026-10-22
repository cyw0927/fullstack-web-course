#Requires -Version 5.1
# RAG Solar 특강 STEP 1~5: 강사 원본 다운로드 + Python venv + dependencies
# Windows PowerShell | 인자 없이 실행하면 다운로드/압축해제/설치까지 수행합니다.
$ErrorActionPreference = "Stop"
$projectPath = $PSScriptRoot
$sourceUrl = "https://raw.githubusercontent.com/GilbertMoon/policy_rag_assistant/044f9d930c7c5b01bec07c2581a61b08b2bd136f/starter-kit-20261022T062047Z-1-001.zip"
$zipName = "starter-kit-20261022T062047Z-1-001.zip"
$expectedSize = 318392
$expectedGitBlobSha = "1ad7b50a3f261c649595249cca7836a954d32c4d"
$downloads = Join-Path $projectPath ".downloads"
$zipPath = Join-Path $downloads $zipName
$extractPath = Join-Path $projectPath "starter-kit"

Write-Host "=== Upstage Solar / RAG 특강 STEP 1~5 ===" -ForegroundColor Cyan
Write-Host "강사 출처: https://github.com/GilbertMoon/policy_rag_assistant"
Write-Host "저장 폴더: $projectPath"

# STEP 1-3: 강사 배포 ZIP을 확인된 커밋에서 다운로드합니다.
New-Item -ItemType Directory -Force -Path $downloads | Out-Null
if (-not (Test-Path -LiteralPath $zipPath)) {
    Write-Host "[1] 강사 Starter Kit ZIP 다운로드..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $sourceUrl -OutFile $zipPath -UseBasicParsing
} else {
    Write-Host "[1] 다운로드한 ZIP이 있어 무결성만 다시 확인합니다."
}

# 잘못된 링크/파일이 내려와도 설치하지 않도록 크기와 Git blob SHA를 확인합니다.
$fileSize = (Get-Item -LiteralPath $zipPath).Length
if ($fileSize -ne $expectedSize) {
    throw "ZIP 파일 크기가 다릅니다 (실제: $fileSize, 예상: $expectedSize). 파일을 확인하세요: $zipPath"
}
$actualBlobSha = (& git hash-object -- $zipPath).Trim()
if ($LASTEXITCODE -ne 0 -or $actualBlobSha -ne $expectedGitBlobSha) {
    throw "강사 ZIP 무결성 검증에 실패했습니다. 예상 Git SHA: $expectedGitBlobSha / 실제: $actualBlobSha"
}
Write-Host "[2] 강사 원본 ZIP 무결성 확인 완료." -ForegroundColor Green

# 기존 파일은 절대로 삭제하거나 덮어쓰지 않습니다.
if (-not (Test-Path -LiteralPath $extractPath)) {
    Write-Host "[3] Starter Kit 압축 해제..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $extractPath | Out-Null
    Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath
} else {
    Write-Host "[3] 기존 starter-kit 폴더를 보존합니다."
}

# ZIP 안에 폴더가 한 겹 더 있어도 실제 실습 루트를 찾습니다.
$fetchScripts = @(Get-ChildItem -LiteralPath $extractPath -Recurse -File -Filter "fetch_ordinances.py")
if ($fetchScripts.Count -ne 1) {
    throw "강의 Starter Kit의 fetch_ordinances.py를 정확히 하나 찾지 못했습니다. 압축 구조를 확인하세요: $extractPath"
}
$kitRoot = $fetchScripts[0].Directory.FullName

$requiredFiles = @(
    "requirements.txt", "config.py", "fetch_ordinances.py", "parse_annex.py",
    "build_index.py", "rag.py", "app.py", "check.py", "demo.py",
    "sample_questions.json", "upstage.py"
)
$missing = @($requiredFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $kitRoot $_)) })
if ($missing.Count -gt 0) {
    throw "강사 Starter Kit 필수 파일이 부족합니다: $($missing -join ', ') (확인 위치: $kitRoot)"
}
Write-Host "Starter Kit 확인: $kitRoot" -ForegroundColor Green

# STEP 4: 원본 Starter Kit 폴더에만 독립 Python 가상환경 생성
Write-Host "[4] Python 가상환경(.venv) 생성..." -ForegroundColor Cyan
Push-Location $kitRoot
try {
    python --version
    if ($LASTEXITCODE -ne 0) { throw "Python 실행 실패. Python 설치 및 PATH 설정을 확인하세요." }

    if (-not (Test-Path -LiteralPath ".venv\Scripts\python.exe")) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "가상환경 생성 실패." }
    }

    $venvPython = Join-Path $kitRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $venvPython)) {
        throw "가상환경 Python을 찾지 못했습니다: $venvPython"
    }

    # STEP 5: 앞서 만들어 둔 임시 패키지 목록이 아닌 강사 원본 requirements 사용
    Write-Host "[5] 강사 원본 requirements.txt 패키지 설치..." -ForegroundColor Cyan
    & $venvPython -m pip install -r (Join-Path $kitRoot "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "패키지 설치 실패. 위의 오류 내용을 확인하세요." }

    Write-Host ""
    Write-Host "STEP 1~5 설치 완료!" -ForegroundColor Green
    Write-Host "실제 실습 위치: $kitRoot"
    Write-Host "이후 VS Code에서 위 실습 위치를 열면 됩니다."
    Write-Host "6번 이후의 Upstage API Key는 .env에만 넣고 GitHub에 올리지 마세요."
} finally {
    Pop-Location
}
