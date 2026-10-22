# Windows PowerShell: RAG 특강 기본 환경 준비
# 이 스크립트는 기존 .env를 덮어쓰지 않습니다.
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    Write-Host "[1/4] Python virtual environment" -ForegroundColor Cyan
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Python 가상환경 생성 실패. python --version을 확인하세요." }

    Write-Host "[2/4] Dependencies" -ForegroundColor Cyan
    & ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "패키지 설치 실패. 인터넷 연결과 Python 버전을 확인하세요." }

    Write-Host "[3/4] .env template" -ForegroundColor Cyan
    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host ".env 파일을 만들었습니다. API 키는 직접 입력해야 합니다."
    } else {
        Write-Host "기존 .env 파일을 보존했습니다."
    }

    Write-Host "[4/4] Environment check" -ForegroundColor Cyan
    & ".\.venv\Scripts\python.exe" verify_environment.py
    if ($LASTEXITCODE -ne 0) { throw "환경 점검 스크립트 실행 실패." }

    Write-Host "기본 준비 절차 완료. Starter Kit 코드는 강사 배포본이 필요합니다." -ForegroundColor Green
} finally {
    Pop-Location
}
